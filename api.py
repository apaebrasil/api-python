from flask import Flask, jsonify, request, Response
import re
import os
from init import dados_excel
import json
import datetime


app = Flask(__name__)

def mascarar_cnpj(cnpj_desformatado):
    if not cnpj_desformatado:
        return None
    # Remove caracteres não numéricos, exceto -, / e espaços
    cnpj_sem_caracteres = re.sub(r"[^\d\-/\s]", "", cnpj_desformatado)
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
    # if not cnpj_formatado:
    #     # CNPJ inválido
    #     return jsonify({'erro': 'CNPJ inválido.'}), 400
    # dados_cnpj = dados_excel.query("CNPJ == '62.388.566/0001-90'")

    dados_excel.loc[dados_excel["CNPJ"] == cnpj_desformatado]

    return dados_excel.to_json(orient='records', indent=5, force_ascii=True)

app.run(debug=True)