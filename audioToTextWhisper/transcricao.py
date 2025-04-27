import requests
from audioToTextWhisper.settings import API_URL, HEADERS

def transcrever_audio(caminho_audio):
    with open(caminho_audio, "rb") as f:
        audio_data = f.read()

    headers = HEADERS.copy()
    headers["Content-Type"] = "audio/wav"

    response = requests.post(API_URL, headers=headers, data=audio_data)

    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print(f"Erro ao transcrever {caminho_audio}: {response.status_code}")
        print("Resposta:", response.text)
        return None
