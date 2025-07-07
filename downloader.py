# downloader.py
import yt_dlp
import os

def download_video(url: str, output_path: str = "temp") -> str:
    """
    Baixa um vídeo do YouTube ou TikTok.

    Args:
        url (str): O URL do vídeo.
        output_path (str): O diretório para salvar o vídeo.

    Returns:
        str: O caminho para o arquivo de vídeo baixado.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)