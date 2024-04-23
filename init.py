import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def download_arquivo(url, destino):
    try:
        # Verifica se o arquivo já existe
        if os.path.exists(destino):
            # Deleta o arquivo existente
            print(f"Excluindo arquivo existente: {destino}")
            # os.remove(destino)
        # Baixa o arquivo
        resposta_arquivo = requests.get(url)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        if resposta_arquivo.status_code == 200:
            # Abre o arquivo no modo de escrita binário e escreve o conteúdo da resposta
            with open(destino, 'wb') as arquivo:
                arquivo.write(resposta_arquivo.content)

            # Verifica se o arquivo foi baixado com sucesso
            if os.path.exists(destino):
                print('Arquivo baixado com sucesso como', destino)
                return True
            else:
                print('Falha ao salvar o arquivo.')
                return False

        else:
            print('Falha ao baixar o arquivo:', resposta_arquivo.status_code)
            return False
        
    except Exception as e:
        print('Erro ao baixar o arquivo:', e)
        return False
    
# Diretório para salvar o arquivo
diretorio_destino = './excel/'

# Cria o diretório de destino se não existir
if not os.path.exists(diretorio_destino):
    os.makedirs(diretorio_destino)

# URL da página onde está o link do arquivo
url_pagina = 'https://www.gov.br/mds/pt-br/acoes-e-programas/suas/entidades-de-assistencia-social/certificacao-de-entidades-beneficentes-de-assistencia-social-cebas'

# Envia uma requisição GET para a URL da página
resposta_pagina = requests.get(url_pagina)

if resposta_pagina.status_code == 200:
    # Parseia o conteúdo HTML da página
    soup = BeautifulSoup(resposta_pagina.content, 'html.parser')

    # Tenta encontrar o elemento usando o seletor CSS do XPath
    elemento = soup.select_one("#parent-fieldname-text > p.callout > strong > a")


    if elemento:
        link_arquivo = elemento['href']
        nome_arquivo = os.path.basename(link_arquivo)
        print(f'Link do arquivo encontrado: {link_arquivo}')
        print(f'Nome do arquivo: {nome_arquivo}')

        # Caminho completo do arquivo
        arquivo_destino = os.path.join(diretorio_destino, nome_arquivo)

        # Baixa o arquivo se ainda não existir
        # download_arquivo(link_arquivo, arquivo_destino)
        
        if os.path.exists(arquivo_destino):

            colunas = [
            'PROTOCOLO', 'ENTIDADE', 'CNPJ', 'MUNICIPIO', 'UF', 'DT_PROTOCOLO',
            'TIPO_PROCESSO','DT_CERTIFICACAO_ANTERIOR_INICIO', 'DT_CERTIFICACAO_ANTERIOR_FIM',
            'PORTARIAS_SNAS','DT_DECISAO_SNAS', 'DT_PUBICACAO_PORTARIA_SNAS_DOU',
            'FASE_PROCESSO','DT_INICIO_CERTIFICACAO_ATUAL', 'DT_FIM_CERTIFICACAO_ATUAL'
            ]

            dados_excel = pd.read_excel(arquivo_destino, skiprows=4, usecols=colunas)

            # dadosCsv = dados_excel.to_csv(arquivo_destino, index=False, encoding='utf-8', sep=',') 
        else:
            print('Falha ao salvar o arquivo.')
    else:
        print('Tag do arquivo não encontrada na página.')
else:
    print('Falha ao acessar a página:', resposta_pagina.status_code)