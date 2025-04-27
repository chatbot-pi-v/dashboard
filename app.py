from milvus.milvus_init import initialize_milvus
from transformLinkInMP3.main import download_to_mp3
from audioToTextWhisper.main import run_transcription
import time
from settings_folders import AUDIO_DIR, DOCS_DIR, PDF_DIR
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

start_time = time.time()

DOCS_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

@app.route('/upload', methods=['POST'])
def receber_json():
    dados = request.get_json()

    url = dados.get("link")
    quote = dados.get("quote")

    download_to_mp3(url)

    run_transcription()

    initialize_milvus(quote)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"O tempo de execução foi: {execution_time} segundos")

    return jsonify({
        "mensagem": "Arquivo transcrito com sucesso",
        "execution_time_seconds": int(execution_time)
        }), 200

if __name__ == '__main__':
    print("Running in 127.0.0.1:6000")
    app.run(host='0.0.0.0', port=6000, debug=True)
