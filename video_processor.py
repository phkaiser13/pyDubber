# video_processor.py
from moviepy.editor import VideoFileClip, AudioFileClip
import os


def extract_audio(video_path: str, output_path: str = "temp") -> str:
    """
    Extrai o áudio de um arquivo de vídeo e o salva como WAV.

    Args:
        video_path (str): Caminho para o arquivo de vídeo.
        output_path (str): Diretório para salvar o áudio.

    Returns:
        str: Caminho para o arquivo de áudio extraído (WAV).
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video_clip = VideoFileClip(video_path)
    audio_path = os.path.join(output_path, "original_audio.wav")
    video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # WAV para melhor qualidade
    video_clip.close()
    return audio_path


def replace_audio(video_path: str, new_audio_path: str, output_path: str = "output") -> str:
    """
    Substitui o áudio de um vídeo por um novo arquivo de áudio.

    Args:
        video_path (str): Caminho para o vídeo original.
        new_audio_path (str): Caminho para o novo áudio dublado.
        output_path (str): Diretório para salvar o vídeo final.

    Returns:
        str: Caminho para o vídeo final com o áudio dublado.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video_clip = VideoFileClip(video_path)
    dubbed_audio_clip = AudioFileClip(new_audio_path)

    # Garante que o áudio tenha a mesma duração do vídeo para evitar erros
    final_audio = dubbed_audio_clip.set_duration(video_clip.duration)

    final_video = video_clip.set_audio(final_audio)

    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    final_video_path = os.path.join(output_path, f"{base_filename}_dubbed.mp4")

    final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')

    video_clip.close()
    dubbed_audio_clip.close()

    return final_video_path