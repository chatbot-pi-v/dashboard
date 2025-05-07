from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from concurrent.futures import ThreadPoolExecutor
from settings_folders import AUDIO_DIR
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

def exportar_chunk(i, chunk, base_nome):
    chunk_final_path = os.path.join(AUDIO_DIR, f"{base_nome}chunk{i}.wav")
    chunk.export(chunk_final_path, format="wav", parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"])
    return chunk_final_path

def dividir_audio_por_silencio(caminho_audio):
    audio = AudioSegment.from_file(caminho_audio)
    base_nome = os.path.splitext(os.path.basename(caminho_audio))[0]

    partes = split_on_silence(
        audio,
        min_silence_len=700,
        silence_thresh=audio.dBFS - 16,
        keep_silence=500
    )

    chunks = []
    tempo_acumulado = 0  # em milissegundos

    for i, chunk in enumerate(partes):
        duracao_ms = len(chunk)
        inicio = tempo_acumulado
        fim = tempo_acumulado + duracao_ms
        tempo_acumulado += duracao_ms

        chunk_final_path = os.path.join(AUDIO_DIR, f"{base_nome}chunk{i}.wav")
        chunk.export(chunk_final_path, format="wav", parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"])

        chunks.append({
            "path": chunk_final_path,
            "start": inicio / 1000,  # converter para segundos
            "end": fim / 1000
        })

    return chunks