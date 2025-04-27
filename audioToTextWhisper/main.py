import os
import time

from audioToTextWhisper.divisao_audio import dividir_audio_por_silencio
from audioToTextWhisper.transcricao import transcrever_audio
from audioToTextWhisper.gerar_pdf import salvar_pdf
from settings_folders import AUDIO_DIR, PDF_DIR

def run_transcription():
    for nome_audio in os.listdir(AUDIO_DIR):
        if nome_audio.lower().endswith((".mp3", ".wav", ".m4a")):
            caminho = os.path.join(AUDIO_DIR, nome_audio).replace("\\", "/")
            print(caminho)
            print(f"Processando: {nome_audio}")

            chunks = dividir_audio_por_silencio(caminho)
            transcricao_completa = ""

            for idx, chunk_path in enumerate(chunks):
                print(f"  Transcrevendo parte {idx + 1}/{len(chunks)}...")
                texto = transcrever_audio(chunk_path)
                if texto:
                    transcricao_completa += f"{texto}\n"
                else:
                    transcricao_completa += f"\n[Parte {idx + 1}] ERRO NA TRANSCRIÇÃO\n"
                os.remove(chunk_path)
                time.sleep(5)

            nome_pdf = os.path.splitext(nome_audio)[0] + ".pdf"
            caminho_pdf = os.path.join(PDF_DIR, nome_pdf)
            salvar_pdf(transcricao_completa, caminho_pdf)
            os.remove(caminho)
            print(f"PDF salvo: {nome_pdf}")

            
