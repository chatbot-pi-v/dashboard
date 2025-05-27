from milvus.milvus_img import insert_images_into_milvus
from milvus.milvus_init import initialize_milvus
from transformLinkInMP3.main import download_to_mp3
from audioToTextWhisper.main import run_transcription
import time
from settings_folders import AUDIO_DIR, DOCS_DIR, IMG_DIR, PDF_DIR
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

start_time = time.time()

DOCS_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    print("Iniciando o upload dos arquivos")

    pasta = request.form.get('caminho')
    print(f"Caminho: {pasta}")

    files = request.files.getlist('files')

    citacoes = request.form.getlist('citacoes')

    if not files:
        return {"error": "Nenhum arquivo enviado"}, 400

    os.makedirs(pasta, exist_ok=True)

    for i in range(len(files)):
        file = files[i]
        citacao = citacoes[i] if i < len(citacoes) else ''
        
        if file.filename == '':
            continue
        
        caminho = f"{pasta}/{file.filename}"
        file.save(caminho)
        print(f"Arquivo salvo: {file.filename}, Citação: {citacao}")

        if pasta == "../../docs/images":
            insert_images_into_milvus(citacao)
            return {"message": "Todos os arquivos foram recebidos com sucesso!"}

        runApp(citacao)

    return {"message": "Todos os arquivos foram recebidos com sucesso!"}

# @app.route('/uploadfile', methods=['POST'])
# def upload_file(caminho):
#     print("Iniciando o upload dos arquivos")

#     files = request.files.getlist('files')
#     citacoes = request.form.getlist('citacoes')

#     if not files:
#         return {"error": "Nenhum arquivo enviado"}, 400

#     os.makedirs("./docs/audio", exist_ok=True)

#     for i in range(len(files)):
#         file = files[i]
#         citacao = citacoes[i] if i < len(citacoes) else ''
        
#         if file.filename == '':
#             continue
        
#         caminho = f"./docs/audio/{file.filename}"
#         file.save(caminho)
#         print(f"Arquivo salvo: {file.filename}, Citação: {citacao}")

#         runApp(citacao)

#     return {"message": "Todos os arquivos foram recebidos com sucesso!"}


@app.route('/uploadlink', methods=['POST'])
def receber_json():
    dados = request.get_json()
    
    if isinstance(dados, list):
        for item in dados:
            link = item.get("link")
            quote = item.get("quote")
            
            if link and quote:
                print(f"Link: {link} | Citação: {quote}")
                
                download_to_mp3(link)
                runApp(quote) 
    else:
        link = dados.get("link")
        quote = dados.get("quote")

        if link and quote:
            print(f"Link único: {link} | Citação: {quote}")
            download_to_mp3(link)
            runApp(quote)

    return {'message': 'Dados recebidos com sucesso'}, 200

def runApp(quote):
    run_transcription()
    initialize_milvus(quote)
    
    
if __name__ == '__main__':
    print("Running in 127.0.0.1:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
