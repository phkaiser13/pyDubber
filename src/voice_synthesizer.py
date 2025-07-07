# voice_synthesizer.py
from TTS.api import TTS
from pydub import AudioSegment
import torch


def synthesize_dubbed_audio(original_audio_path: str, translated_segments: list, output_path: str = "temp") -> str:
    """
    Cria um áudio dublado usando clonagem de voz para cada locutor.

    Args:
        original_audio_path (str): Caminho para o áudio original (para extrair vozes).
        translated_segments (list): Segmentos com texto traduzido e informações do locutor.
        output_path (str): Diretório para salvar os arquivos de áudio gerados.

    Returns:
        str: Caminho para o arquivo de áudio final dublado.
    """
    print("Iniciando síntese de voz com clonagem...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts_model = "tts_models/multilingual/multi-dataset/xtts_v2"
    tts = TTS(tts_model).to(device)

    original_audio = AudioSegment.from_wav(original_audio_path)
    final_dubbed_audio = AudioSegment.silent(duration=len(original_audio))

    # Extrai um clipe de referência para cada locutor
    speaker_references = {}
    for segment in translated_segments:
        speaker = segment['speaker']
        if speaker not in speaker_references and speaker != "UNKNOWN":
            # Extrai um clipe de 5 segundos da primeira fala do locutor
            start_ms = segment['start'] * 1000
            end_ms = min(segment['end'] * 1000, start_ms + 5000)
            reference_clip = original_audio[start_ms:end_ms]
            ref_path = os.path.join(output_path, f"ref_{speaker}.wav")
            reference_clip.export(ref_path, format="wav")
            speaker_references[speaker] = ref_path
            print(f"Clipe de referência criado para {speaker} em {ref_path}")

    # Sintetiza e monta o áudio final
    for i, segment in enumerate(translated_segments):
        speaker = segment['speaker']
        if speaker == "UNKNOWN" or 'translated_text' not in segment:
            continue

        print(f"Sintetizando segmento {i + 1}/{len(translated_segments)} para {speaker}...")

        segment_audio_path = os.path.join(output_path, f"segment_{i}.wav")

        tts.tts_to_file(
            text=segment['translated_text'],
            speaker_wav=speaker_references[speaker],
            language="pt",  # Defina o idioma do texto traduzido
            file_path=segment_audio_path
        )

        # Carrega o segmento sintetizado e o insere na faixa de áudio final
        segment_audio = AudioSegment.from_wav(segment_audio_path)
        final_dubbed_audio = final_dubbed_audio.overlay(segment_audio, position=segment['start'] * 1000)

    dubbed_audio_path = os.path.join(output_path, "dubbed_audio.wav")
    final_dubbed_audio.export(dubbed_audio_path, format="wav")
    print(f"Áudio dublado final criado em: {dubbed_audio_path}")

    return dubbed_audio_path
    ```


---

#### **7. `main.py`**

O
orquestrador
que
une
tudo.

```python
# main.py
import os
from src.downloader import download_video
from src.video_processor import extract_audio, replace_audio
from src.transcriber import transcribe_and_diarize
from src.translator import translate_text_segments
from voice_synthesizer import synthesize_dubbed_audio


def main():
    """
    Função principal para orquestrar o processo de dublagem.
    """
    # --- Configuração ---
    # É crucial configurar estas variáveis de ambiente no seu sistema
    # ou defini-las diretamente aqui (menos seguro).
    HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
    # GOOGLE_APPLICATION_CREDENTIALS deve apontar para o seu arquivo JSON.

    if not HUGGING_FACE_TOKEN or not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "ERRO: As variáveis de ambiente HUGGING_FACE_TOKEN e GOOGLE_APPLICATION_CREDENTIALS devem ser configuradas.")
        return

    temp_dir = "temp"
    output_dir = "output"

    # --- Início do Processo ---
    video_url = input("Por favor, insira o URL do vídeo do YouTube ou TikTok: ")
    target_language = input("Insira o código do idioma de destino (ex: pt-BR, es, fr): ")

    try:
        # 1. Download do Vídeo
        print("\n--- Etapa 1: Baixando o vídeo ---")
        video_path = download_video(video_url, temp_dir)
        print(f"Vídeo baixado em: {video_path}")

        # 2. Extração de Áudio
        print("\n--- Etapa 2: Extraindo o áudio ---")
        audio_path = extract_audio(video_path, temp_dir)
        print(f"Áudio extraído em: {audio_path}")

        # 3. Transcrição e Diarização
        print("\n--- Etapa 3: Transcrevendo e identificando locutores ---")
        transcribed_segments = transcribe_and_diarize(audio_path, HUGGING_FACE_TOKEN)
        print(f"Transcrição concluída com {len(transcribed_segments)} segmentos.")

        # 4. Tradução
        print("\n--- Etapa 4: Traduzindo o texto ---")
        translated_segments = translate_text_segments(transcribed_segments, target_language)
        print("Tradução concluída.")

        # 5. Síntese de Voz
        print("\n--- Etapa 5: Sintetizando o áudio dublado ---")
        dubbed_audio_path = synthesize_dubbed_audio(audio_path, translated_segments, temp_dir)
        print("Síntese de voz concluída.")

        # 6. Substituição do Áudio
        print("\n--- Etapa 6: Montando o vídeo final ---")
        final_video_path = replace_audio(video_path, dubbed_audio_path, output_dir)
        print(f"PROCESSO CONCLUÍDO! O vídeo dublado está em: {final_video_path}")

    except Exception as e:
        print(f"\nOcorreu um erro durante o processo: {e}")

    finally:
        # Limpeza dos arquivos temporários
        if os.path.exists(temp_dir):
            # shutil.rmtree(temp_dir)
            print(f"Arquivos temporários mantidos em '{temp_dir}' para depuração.")


if __name__ == "__main__":
    main()