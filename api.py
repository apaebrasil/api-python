from flask import Flask, jsonify, request, Response
import re
from init import *
import json
from datetime import datetime


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

teste = ['03.380.445/0001-32', '62.388.566/0001-90']

def mascarar_cnpj(cnpj_desformatado):
    if not cnpj_desformatado:
        return None
    # Remove caracteres não numéricos, exceto -, / e espaços
    cnpj_sem_caracteres = re.sub(r"[^\d\-/\s]", "", cnpj_desformatado)
    
    #Remove apenas caracteres não numéricos
    # cnpj_sem_caracteres = re.sub(r"[^\d]", "", cnpj_desformatado)

    # Valida tamanho do CNPJ
    if len(cnpj_sem_caracteres) != 14:
        return f"CNPJ inválido: {cnpj_desformatado}"
    
    # Formata CNPJ com máscara
    try:
        # Preenche com zeros à esquerda caso necessário
        cnpj_sem_caracteres = cnpj_sem_caracteres.zfill(14)
        return f"{cnpj_sem_caracteres[:2]}.{cnpj_sem_caracteres[2:5]}.{cnpj_sem_caracteres[5:8]}/{cnpj_sem_caracteres[8:10]}-{cnpj_sem_caracteres[10:14]}"
    except ValueError:
        return f"CNPJ inválido: {cnpj_desformatado}"
    
def consultar_dados_cnpj(dados_excel, cnpj):
    print('O CNPJ QUE VEIO FOI:', cnpj)
    if dados_excel is not None:
        # Filtra os dados pelo CNPJ informado
        # dados_cnpj = dados_excel[dados_excel['CNPJ'] == cnpj]
        
        # dados_cnpj = dados_excel.query(f"CNPJ == '62.388.566/0001-90'")
        
        dados_cnpj = dados_excel.query(f"CNPJ == '{teste[1]}'")

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
    
    print(cnpj_desformatado, cnpj_formatado)
    
    result = consultar_dados_cnpj(dados_excel, cnpj_formatado)
    timestamp_str = str(result)
    
    response = Response(
        response=json.dumps(timestamp_str, ensure_ascii=False).encode('utf8'),
        status=200,
        mimetype='application/json'
    )
    
    # return jsonify(timestamp_str)
    return response
app.run(debug=True)