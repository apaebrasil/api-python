from flask import Flask, jsonify, request
from init import ler_arquivo_excel, consultar_dados_cnpj
import re
import os

app = Flask(__name__)

# arquivo_destino = os.path.join(diretorio_destino, nome_arquivo)
# dados_excel = ler_arquivo_excel(arquivo_destino)

def mascarar_cnpj(cnpj_desformatado):
    if cnpj_desformatado:
        # Remove caracteres não numéricos
        cnpj_sem_caracteres = re.sub(r"[^\d]", "", cnpj_desformatado)

        # Adiciona máscara
        if len(cnpj_sem_caracteres) == 14:
            return f"{cnpj_sem_caracteres[:2]}.{cnpj_sem_caracteres[2:5]}.{cnpj_sem_caracteres[5:8]}/{cnpj_sem_caracteres[8:10]}-{cnpj_sem_caracteres[10:14]}"
        else:
            print(f"CNPJ inválido: {cnpj_desformatado}")
            return None
    else:
        return None


@app.route('/')
def homepage():
    return 'Homepage'

@app.route('/api', methods=['GET'])
def api():
    return 'Page Api'

@app.route('/api/cebas', methods=['GET'])
def cebas():
    cnpj_desformatado = request.args.get('cnpj')
    cnpj_formatado = mascarar_cnpj(cnpj_desformatado)


    if not cnpj_formatado:
        # CNPJ inválido
        return jsonify({'erro': 'CNPJ inválido.'}), 400
    
    diretorio_destino = './excel/'
    nome_arquivo = 'PROCESSOSCEBAS15.04.2024Site.xls'

    # Consulta os dados pelo CNPJ
    # dados_cnpj = consultar_dados_cnpj(dados_excel, cnpj_formatado, diretorio_destino, nome_arquivo)
    
    # if cnpj_formatado:
    #     return jsonify(dados_cnpj)
    # else:
    #     return jsonify({'erro': 'CNPJ não encontrado.'})

    return cnpj_formatado
app.run(host='0.0.0.0', debug=True)