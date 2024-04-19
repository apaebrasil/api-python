from flask import Flask, jsonify, request, Response
import re
import os
from init import *
import json
import jsonpickle
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
    # dados_filtrados = dadosCsv.query("CNPJ == '62.388.566/0001-90'")

    # dados_filtrados = dadosCsv.loc[indices_linha].query("`CNPJ` == @cnpj_alvo")

    # dados_filtrados = dadosCsv.query("CNPJ == '24.862.252/0001-98'")


    # if dados_filtrados.empty:
    #     return jsonify({'erro': 'CNPJ não encontrado.'}), 404
    
    # dados_excel.to_csv(index=True, encoding='utf-8')

    colunas = [
    'PROTOCOLO', 'ENTIDADE', 'CNPJ', 'MUNICIPIO', 'UF', 'DT_PROTOCOLO',
    'ORGAO_ORIGEM', 'DT_RECEBIMENTO_MDS', 'MOTIVO_RECEBIMENTO', 'TIPO_PROCESSO',
    'DT_CERTIFICACAO_ANTERIOR_INICIO', 'DT_CERTIFICACAO_ANTERIOR_FIM',
    'DT_PUBLICACAO_CERTIFICACAO_ANTERIOR_DOU', 'ORGAO_CERTIFICACAO_ANTERIOR',
    'ORGAO_ENCAMINHAMENTO', 'OFICIO_ENCAMINHAMENTO', 'DT_ENCAMINHAMENTO',
    'MOTIVO_ENCAMINHAMENTO', 'DT_RETORNO_MDS', 'OFICIO_RETORNO', 'PORTARIAS_SNAS',
    'DT_DECISAO_SNAS', 'DT_PUBICACAO_PORTARIA_SNAS_DOU', 'ITEM_PORTARIA_DECISAO_SNAS',
    'PROTOCOLO_RECURSO_SNAS', 'DT_PROTOCOLO_RECURSO_SNAS', 'PORTARIA_DECISAO_RECURSO_SNAS',
    'DT_PORTARIA_RECONSIDERACAO_SNAS', 'DT_PUBLICACAO_DOU_RECONSIDERACAO_SNAS',
    'PORTARIA_DECISAO_RECURSO_GM', 'DT_PORTARIA_DECISAO_RECURSO_GM',
    'DT_PUBLICACAO_DOU_PORTARIA_DECISAO_RECURSO_GM', 'FASE_PROCESSO',
    'DT_INICIO_CERTIFICACAO_ATUAL', 'DT_FIM_CERTIFICACAO_ATUAL'
    ]

    # dados_excel.to_csv(index=True, encoding='utf-8', header=True, sep="\t", columns=colunas, index_col=0)

    # dados = dados_excel.to_csv(index=True, encoding='utf-8', header=True, columns=colunas

    # jsonify(dados, mimetype='application/json')
    # dados_cnpj = dados_excel.query("CNPJ == '24.862.252/0001-98'")
    # dados_excel.to_dict(orient='records')[0]
    return dados_excel.to_json()

app.run(host='0.0.0.0', debug=True)