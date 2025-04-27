import subprocess
from settings_folders import AUDIO_DIR

def download_to_mp3(url: str):
    """
    Baixa o áudio de uma URL (YouTube, Spotify, Apple Music…) e converte para MP3.
    Requer o binário yt‑dlp instalado (pip ou standalone).
    """
    cmd = [
        "yt-dlp",
        url,
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",              # VBR ~245 kbps
        "--embed-thumbnail",
        "--output", str(AUDIO_DIR / "%(title)s.%(ext)s"),
    ]
    subprocess.run(cmd, check=True)

    print(f"Áudio salvo em: {AUDIO_DIR}")

