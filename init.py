import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def consultar_dados_cnpj(dados_excel, cnpj):
    if dados_excel is not None:
        # Filtra os dados pelo CNPJ informado
        dados_cnpj = dados_excel[dados_excel['CNPJ'] == cnpj]

        # Converte o DataFrame em um dicionário
        if not dados_cnpj.empty:
            dados_cnpj = dados_cnpj.to_dict(orient='records')[0]
            return dados_cnpj
        else:
            print(f'CNPJ {cnpj} não encontrado.')
            return None
    else:
        print('Dados do Excel não disponíveis.')
        return None

def ler_arquivo_excel(arquivo_destino):
    """
    Lê o arquivo Excel e retorna os dados como um DataFrame.

    Args:
        arquivo_destino (str): Caminho para o arquivo Excel.

    Returns:
        pandas.DataFrame: DataFrame contendo os dados do Excel, ou None se o arquivo não for encontrado ou não puder ser lido.
    """
    try:
        # Lê o arquivo Excel usando o Pandas
        dados_excel = pd.read_excel(arquivo_destino, skiprows=4)
        return dados_excel
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f'Erro ao ler o arquivo Excel: {e}')
        return None

def download_arquivo(url, destino):
    """
    Baixa um arquivo para o destino especificado, substituindo o arquivo existente se houver.

    Args:
        url (str): URL do arquivo.
        destino (str): Caminho para o destino do arquivo.

    Returns:
        bool: True se o download foi bem-sucedido, False caso contrário.
    """
    try:
        # Verifica se o arquivo já existe
        if os.path.exists(destino):
            # Deleta o arquivo existente
            print(f"Excluindo arquivo existente: {destino}")
            os.remove(destino)
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
    # 
    # Tenta encontrar o elemento usando o seletor CSS do XPath
    elemento = soup.select_one("#parent-fieldname-text > p.callout > strong > a")

    # Encontra o link do arquivo na página
    # tag_arquivo = soup.find('a', href='https://www.gov.br/mds/pt-br/acoes-e-programas/suas/entidades-de-assistencia-social/copy2_of_PROCESSOSCEBAS15.04.2024Site.xls')

    if elemento:
        link_arquivo = elemento['href']
        nome_arquivo = os.path.basename(link_arquivo)
        print(f'Link do arquivo encontrado: {link_arquivo}')
        print(f'Nome do arquivo: {nome_arquivo}')

        # Caminho completo do arquivo
        arquivo_destino = os.path.join(diretorio_destino, nome_arquivo)

        # Baixa o arquivo se ainda não existir
        download_arquivo(link_arquivo, arquivo_destino)
        if os.path.exists(arquivo_destino):
            # Lê o arquivo Excel (opcional)
            dados_excel = pd.read_excel(arquivo_destino, skiprows=4)

            dados_cnpj = dados_excel.query("CNPJ == '24.862.252/0001-98'")
            print(dados_cnpj)

            # cnpjs_para_consultar = ['62.388.566/0001-90', '03.380.445/0001-32', '30.412.616/0001-30']
            # dados_cnpjs = dados_excel[dados_excel['CNPJ'].isin(cnpjs_para_consultar)]
        else:
            print('Falha ao salvar o arquivo.')
    else:
        print('Tag do arquivo não encontrada na página.')
else:
    print('Falha ao acessar a página:', resposta_pagina.status_code)
