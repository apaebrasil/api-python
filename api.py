from flask import Flask, jsonify, request, Response
import re
from init import *
import json
from datetime import datetime
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# app.config['API_KEY'] = os.getenv("APIKEY")

def mascarar_cnpj(cnpj_desformatado):
    if not cnpj_desformatado:
        return None
    cnpj_formatado = re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', cnpj_desformatado)
    return cnpj_formatado

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

def consultar_dados_cnpj(dados_excel, cnpj):
    print('O CNPJ QUE VEIO FOI:', cnpj)
    if dados_excel is not None:
        # dados_cnpj = dados_excel.query(f"CNPJ == '62.388.566/0001-90'")
        # 62.388.566/0001-90  62388566000190
        # dados_cnpj = dados_excel[dados_excel['CNPJ'] == '59.573.030/0001-30']
        dados_cnpj = dados_excel.query(f"CNPJ == '{cnpj}'")
        print(dados_cnpj)
        # Converte o DataFrame em um dicionário
        
        if not dados_cnpj.empty:
            dados_cnpj = dados_cnpj.to_dict('index')
            return dados_cnpj
        else:
            print(f'CNPJ {cnpj} não encontrado.')
            return None
    else:
        print('Dados do Excel não disponíveis.')
        return None

app.run(host='0.0.0.0', debug=True, port=5000)