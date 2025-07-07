# main.py
import downloader
import transcriber
import translator
import voice_synthesizer
import video_processor
import os
import shutil


def main():
    youtube_url = input("Por favor, insira a URL do vídeo do YouTube que você deseja dublar: ")

    temp_folder = "temp"

    try:
        # Passo 1: Download e extração de áudio
        original_video_path, original_audio_path = downloader.download_and_extract_audio(youtube_url, temp_folder)

        # Passo 2: Transcrição do áudio original
        original_text = transcriber.transcribe_audio(original_audio_path)

        # Passo 3: Tradução do texto
        translated_text = translator.translate_text(original_text, target_language='pt')

        # Passo 4: Síntese de voz com clonagem
        translated_audio_path = voice_synthesizer.synthesize_cloned_voice(
            text=translated_text,
            reference_audio_path=original_audio_path,
            output_path=temp_folder
        )

        # Passo 5: Combinação do vídeo com o novo áudio
        video_processor.combine_video_and_audio(original_video_path, translated_audio_path)

    except Exception as e:
        print(f"\nOcorreu um erro durante o processo: {e}")
    finally:
        # Limpa a pasta temporária
        if os.path.exists(temp_folder):
            print("Limpando arquivos temporários...")
            shutil.rmtree(temp_folder)


if __name__ == "__main__":
    main()