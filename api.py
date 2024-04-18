from flask import Flask, jsonify, request
import re
import os
from init import *

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
    # dados_cnpj = dados.query("CNPJ == 'cnpj_formatado'")


    if not cnpj_formatado:
        # CNPJ inválido
        return jsonify({'erro': 'CNPJ inválido.'}), 400
    
    
    # filtrar pelo cnpj no DataFrame, passar o cnpj que vem na requisição para esse que está fixo
    dados_filtrados = dados_excel.query("CNPJ == '62.388.566/0001-90'")
    


    # if dados_filtrados.empty:
    #     return jsonify({'erro': 'CNPJ não encontrado.'}), 404
    
    dados_json = dados_filtrados.to_json()

    return dados_json

app.run(host='0.0.0.0', debug=True)