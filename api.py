from flask import Flask, jsonify, request, Response, render_template
import re
from init import *
import json
from datetime import datetime
from flask_cors import CORS, cross_origin
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__, template_folder='./')
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['API_KEY'] = os.getenv("APIKEY")
cors = CORS(app)

def mascarar_cnpj(cnpj_desformatado):
    if not cnpj_desformatado:
        return None
    cnpj_formatado = re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', cnpj_desformatado)
    return cnpj_formatado

@app.route('/')
@cross_origin()
def homepage():
    return 'Homepage'


@app.route('/api', methods=['GET'])
def api():
    return render_template('index.html')

@app.route('/api/cebas', methods=['GET'])
@cross_origin()
def cebasCnpj():
    cnpj_desformatado = request.args.get('cnpj')
    cnpj_formatado = mascarar_cnpj(cnpj_desformatado)            
    result = consultar_dados_cnpj(dados_excel, cnpj_formatado)
    timestamp_str = str(result)
    
    a = 'Timestamp'
    b = 'nan'
    c= 'NaT'
    d="("
    e=")"
    f=" 00:00:00"
    g='\"' 
    timestamp_str = str(result).replace(a,'').replace(b,"''").replace(c,"''").replace(d,'').replace(e,'').replace(f,'').replace(g,'')
    
    response = Response(
        response=json.dumps(timestamp_str, ensure_ascii=False).encode('utf8'),
        status=200,
        mimetype='application/json'
    )
    # return jsonify(timestamp_str)
    return response


@app.route('/api/cebas/all', methods=['GET'])
@cross_origin()
def consultarTodosDados():
    # dados_cnpj = dados_cnpj.to_dict('index')

    dadosDescolunados = dados_excel

    result = dadosDescolunados.to_dict('records')
    timestamp_str = str(result)
    
    response = Response(
        response=json.dumps(timestamp_str),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/cebas/getcount', methods=['GET'])
@cross_origin()
def getCount():
    dadosDescolunados = dados_excel
    numero_linhas = dadosDescolunados.index.size

    data = {
        "total_lines": numero_linhas
    }
    return data

@app.route('/api/cebas/getlink', methods=['GET'])
@cross_origin()
def getLinkCebas():

    data = {
        "link": link_arquivo
    }

    return jsonify(data)

@app.route('/api/cebas/paginado', methods=['GET'])
@cross_origin()
def getCebasPaginada():

    row_start = request.args.get('row_start')
    qtd_rows = request.args.get('qtd_rows')
    status = str(request.args.get('status'))
    dt_inicio = str(request.args.get('dt_inicio'))
    dt_fim = str(request.args.get('dt_fim'))
    

    row_start_data = int(row_start)
    qtd_rows_data = int(qtd_rows)
        
    a = 'Timestamp'
    b = 'nan'
    c= 'NaT'
    d="("
    e=")"
    f=" 00:00:00"
    g='\"'
    
        
    dados= dados_excel.query(f"DT_FIM_CERTIFICACAO_ATUAL >= '{dt_inicio}'")
    dados= dados.query(f"DT_FIM_CERTIFICACAO_ATUAL <= '{dt_fim}'")
            
    dados = dados.iloc[row_start_data:row_start_data+qtd_rows_data]    
    
    if(status != "None" and status != ""):
        dados= dados.query(f"FASE_PROCESSO == '{status}'")                        

    result = dados.to_dict('records')
    timestamp_str = str(result).replace(a,'').replace(b,"''").replace(c,"''").replace(d,'').replace(e,'').replace(f,'').replace(g, '')

    response = Response(
        response=json.dumps(timestamp_str),
        status=200,
        mimetype='application/json'
    )

    return response

def consultar_dados_cnpj(dados_excel, cnpj):
    print('O CNPJ QUE VEIO FOI:', cnpj)
    if dados_excel is not None:
        # dados_cnpj = dados_excel.query(f"CNPJ == '62.388.566/0001-90'")
        # 62.388.566/0001-90  62388566000190
        # dados_cnpj = dados_excel[dados_excel['CNPJ'] == '59.573.030/0001-30']
        dados_cnpj = dados_excel.query(f"CNPJ == '{cnpj}'")
        # Converte o DataFrame em um dicionário
        if not dados_cnpj.empty:
            dados_cnpj = dados_cnpj.to_dict('records')
            return dados_cnpj
        else:
            print(f'CNPJ {cnpj} não encontrado.')
            return None
    else:
        print('Dados do Excel não disponíveis.')
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)