from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import subprocess
# from audioToTextWhisper.settings import AUDIO_DIR
from settings_folders import AUDIO_DIR, PDF_DIR

def dividir_audio_por_silencio(caminho_audio):
    audio = AudioSegment.from_file(caminho_audio)
    base_nome = os.path.splitext(os.path.basename(caminho_audio))[0]
    chunks = []

    partes = split_on_silence(
        audio,
        min_silence_len=700,
        silence_thresh=audio.dBFS - 16,
        keep_silence=500
    )

    for i, chunk in enumerate(partes):

        print(f"dividindo chuck parte {i + 1}")

        chunk_temp_path = os.path.join(AUDIO_DIR, f"{base_nome}_chunk_{i}.mp3").replace("\\", "/")
        chunk_final_path = os.path.join(AUDIO_DIR, f"{base_nome}_chunk_{i}.wav").replace("\\", "/")

        chunk.export(chunk_temp_path, format="mp3")

        subprocess.run([
            "ffmpeg", "-y",
            "-i", chunk_temp_path,
            "-ac", "1",
            "-ar", "16000",
            "-sample_fmt", "s16",
            chunk_final_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(chunk_temp_path)
        chunks.append(chunk_final_path)

    return chunks
