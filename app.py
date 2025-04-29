from milvus.milvus_init import initialize_milvus
from transformLinkInMP3.main import download_to_mp3
from audioToTextWhisper.main import run_transcription
import time
from settings_folders import AUDIO_DIR, DOCS_DIR, PDF_DIR
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

start_time = time.time()

DOCS_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    print("Iniciando o upload do arquivo")
    if 'file' not in request.files:
        return {"error": "Nenhum arquivo enviado"}, 400

    file = request.files['file']
    print(file)
    if file.filename == '':
        return {"error": "Nome do arquivo vazio"}, 400

    # Opcional: salvar o arquivo
    file.save(f"./docs/audio/{file.filename}")
    
    runApp("maluzinha")
    
    return {"filename": file.filename, "message": "Arquivo recebido com sucesso!"}

@app.route('/uploadlink', methods=['POST'])
def receber_json():
    dados = request.get_json()

    url = dados.get("link")
    quote = dados.get("quote")

    download_to_mp3(url)

    runApp(quote)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"O tempo de execução foi: {execution_time} segundos")

    return jsonify({
        "mensagem": "Arquivo transcrito com sucesso",
        "execution_time_seconds": int(execution_time)
        }), 200

def runApp(quote):
    run_transcription()
    initialize_milvus(quote)
    
    
if __name__ == '__main__':
    print("Running in 127.0.0.1:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
