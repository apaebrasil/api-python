import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def download_arquivo(url, destino):
    # Verifica se o arquivo já existe
    if not os.path.exists(destino):
        # Baixa o arquivo
        resposta_arquivo = requests.get(url)
        # Verifica se a requisição foi bem-sucedida (código de status 200)
        if resposta_arquivo.status_code == 200:
            # Abre o arquivo no modo de escrita em binário e escreve o conteúdo da resposta
            with open(destino, 'wb') as arquivo:
                arquivo.write(resposta_arquivo.content)
            print('Arquivo baixado com sucesso como', destino)
        else:
            print('Falha ao baixar o arquivo:', resposta_arquivo.status_code)
    else:
        print('O arquivo', destino, 'já existe, não é necessário baixá-lo novamente.')
        
# URL da página onde está o link do arquivo
url_pagina = 'https://www.gov.br/mds/pt-br/acoes-e-programas/suas/entidades-de-assistencia-social/certificacao-de-entidades-beneficentes-de-assistencia-social-cebas'

# Envia uma requisição GET para a URL da página
resposta_pagina = requests.get(url_pagina)

if resposta_pagina.status_code == 200:
    # Parseia o conteúdo HTML da página
    soup = BeautifulSoup(resposta_pagina.content, 'html.parser')
    
    # Encontra o link do arquivo na página
    tag_arquivo = soup.find('a', href='https://www.gov.br/mds/pt-br/acoes-e-programas/suas/entidades-de-assistencia-social/PROCESSOSCEBAS15.04.2024Site.xls')
    
    if tag_arquivo:
        link_arquivo = tag_arquivo['href']
        nome_arquivo = os.path.basename(link_arquivo)

        # Baixa o arquivo se ainda não existir
        download_arquivo(link_arquivo, nome_arquivo)
        
        # dados_excel = pd.read_excel(nome_arquivo)
        # print(dados_excel.head())
    else:
        print('Tag do arquivo não encontrada na página.')
else:
    print('Falha ao acessar a página:', resposta_pagina.status_code)
