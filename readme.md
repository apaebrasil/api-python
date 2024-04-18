# Gerar o requirements.txt 
    pip freeze > requirements.txt

# Instalar pacotes 
    pip install -r requirements.txt


62388566000190
62.388.566/0001-90


    # filtrar pelo cpf no excel
    # dados_cnpj = dados_excel.query("CNPJ == '24.862.252/0001-98'")
    print(dados_excel)

    # Converta o DataFrame para JSON
    # dados_json = dados_excel.to_json(orient='records', indent=4)

    # cnpjs_para_consultar = ['62.388.566/0001-90', '03.380.445/0001-32', '30.412.616/0001-30']
    # dados_cnpjs = dados_excel[dados_excel['CNPJ'].isin(cnpjs_para_consultar)]