# transcriber.py
from pyannote.audio import Pipeline
from faster_whisper import WhisperModel
import torch


def transcribe_and_diarize(audio_path: str, hf_token: str) -> list:
    """
    Realiza a diarização do locutor e a transcrição com timestamps.

    Args:
        audio_path (str): Caminho para o arquivo de áudio.
        hf_token (str): Token de acesso do Hugging Face para pyannote.

    Returns:
        list: Uma lista de dicionários, onde cada um contém 'start', 'end', 'speaker', e 'text'.
    """
    # 1. Diarização de Locutor com pyannote.audio
    print("Iniciando diarização de locutor...")
    diarization_pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )

    # Enviar para GPU se disponível
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    diarization_pipeline.to(device)

    diarization = diarization_pipeline(audio_path)

    # 2. Transcrição com faster-whisper
    print("Iniciando transcrição com Whisper...")
    model_size = "large-v3"  # ou "medium.en", "base", etc.
    whisper_model = WhisperModel(model_size, device="cuda" if torch.cuda.is_available() else "cpu",
                                 compute_type="float16" if torch.cuda.is_available() else "int8")

    segments, _ = whisper_model.transcribe(audio_path, word_timestamps=True)

    # 3. Combinar resultados
    print("Combinando resultados da diarização e transcrição...")
    transcribed_segments = []
    for segment in segments:
        for word in segment.words:
            # Encontra qual locutor estava falando no meio da palavra
            word_middle_time = word.start + (word.end - word.start) / 2
            try:
                speaker = diarization.crop(word.word).labels()[0]
            except IndexError:
                # Se não encontrar um locutor, pode ser silêncio ou sobreposição
                speaker = "UNKNOWN"

            # Agrupa palavras no mesmo segmento de locutor
            if transcribed_segments and transcribed_segments[-1]['speaker'] == speaker:
                transcribed_segments[-1]['text'] += " " + word.word
                transcribed_segments[-1]['end'] = word.end
            else:
                transcribed_segments.append({
                    'start': word.start,
                    'end': word.end,
                    'speaker': speaker,
                    'text': word.word
                })

    return transcribed_segments