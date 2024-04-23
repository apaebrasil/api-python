# Gerar o requirements.txt 
    pip freeze > requirements.txt

# Instalar pacotes 
    pip install -r requirements.txt

# Docker
    docker build --tag my-api .
    docker run --name app -p 5000:5000 my-api


    docker build -t apiapicebas/python:3.9 .
    docker container run --name teste -p 5000 apiapicebas/python:3.9
    docker login
    docker tag <imagem_id> <sua_conta>/<nome_image>:tag
    docker push <nome_da_sua_conta>/sua_imagem:tag


## CNPJ PARA TESTE
    62388566000190
    62.388.566/0001-90

    59.573.030/0001-30
    59573030000130

    16.212.078/0001-00
    16212078000100

    03380445000132
    03.380.445/0001-32

    # filtrar pelo cpf no excel
    
    # dados_cnpj = dados_excel.query("CNPJ == '24.862.252/0001-98'")
    print(dados_excel)

    # Converta o DataFrame para JSON
    # dados_json = dados_excel.to_json(orient='records', indent=4)

    # cnpjs_para_consultar = ['62.388.566/0001-90', '03.380.445/0001-32', '30.412.616/0001-30']
    # dados_cnpjs = dados_excel[dados_excel['CNPJ'].isin(cnpjs_para_consultar)]

    http://127.0.0.1:5000/api

Amazon EC2
Elastic 


docker build -t apiflaskcebas/python3.9 .
docker images
docker run -d -p 5000:5000 apiflaskcebas/python3.9