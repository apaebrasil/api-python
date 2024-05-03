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
    
    dados = dados_excel.query(f"CNPJ == '{cnpj_formatado}'")
    
    formatted_data = []
    for row in dados.to_dict("records"):
        row['DT_PROTOCOLO'] =  formatar_se_valido(row['DT_PROTOCOLO'])
        row['DT_INICIO_CERTIFICACAO_ATUAL'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_CERTIFICACAO_ANTERIOR_FIM'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_FIM_CERTIFICACAO_ATUAL'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_FIM'])        
        row['DT_CERTIFICACAO_ANTERIOR_INICIO'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_DECISAO_SNAS'] =  formatar_se_valido(row['DT_DECISAO_SNAS'])
        row['DT_PUBICACAO_PORTARIA_SNAS_DOU'] =  formatar_se_valido(row['DT_PUBICACAO_PORTARIA_SNAS_DOU'])
        formatted_data.append(row)
    
    response = Response(
        response=json.dumps(formatted_data),
        status=200,
        mimetype='application/json'
    )                
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
        
        
    dados= dados_excel.query(f"DT_FIM_CERTIFICACAO_ATUAL >= '{dt_inicio}'")
    dados= dados.query(f"DT_FIM_CERTIFICACAO_ATUAL <= '{dt_fim}'")
            
    dados = dados.iloc[row_start_data:row_start_data+qtd_rows_data]    
    
    if(status != "None" and status != ""):
        dados= dados.query(f"FASE_PROCESSO == '{status}'")                        
    formatted_data = []
    for row in dados.to_dict('records'):
        row['DT_PROTOCOLO'] =  formatar_se_valido(row['DT_PROTOCOLO'])
        row['DT_INICIO_CERTIFICACAO_ATUAL'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_CERTIFICACAO_ANTERIOR_FIM'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_FIM_CERTIFICACAO_ATUAL'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_FIM'])        
        row['DT_CERTIFICACAO_ANTERIOR_INICIO'] =  formatar_se_valido(row['DT_CERTIFICACAO_ANTERIOR_INICIO'])
        row['DT_DECISAO_SNAS'] =  formatar_se_valido(row['DT_DECISAO_SNAS'])
        row['DT_PUBICACAO_PORTARIA_SNAS_DOU'] =  formatar_se_valido(row['DT_PUBICACAO_PORTARIA_SNAS_DOU'])
        formatted_data.append(row)
        
    
    
    response = Response(
        response=json.dumps(formatted_data),
        status=200,
        mimetype='application/json'
    )

    return response

def formatar_se_valido(timestamp):
    if not pd.isna(timestamp) and not isinstance(timestamp, str):  # Verifica se não é ausente
        return timestamp.strftime('%Y-%m-%d')  # Formatar se válido
    else:
        return "" 
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=False)