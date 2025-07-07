# translator.py
from google.cloud import translate_v2 as translate
import os


def translate_text_segments(segments: list, target_language: str = "pt-BR") -> list:
    """
    Traduz o texto em uma lista de segmentos.

    Args:
        segments (list): Lista de segmentos da transcrição.
        target_language (str): Código do idioma de destino (ex: 'pt-BR', 'es', 'fr').

    Returns:
        list: A mesma lista de segmentos com o campo 'text' traduzido.
    """
    # Certifique-se de que a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS está configurada
    # com o caminho para o seu arquivo JSON de credenciais.
    print(f"Traduzindo texto para {target_language}...")
    translate_client = translate.Client()

    for segment in segments:
        if isinstance(segment['text'], bytes):
            text_to_translate = segment['text'].decode("utf-8")
        else:
            text_to_translate = segment['text']

        result = translate_client.translate(text_to_translate, target_language=target_language)
        segment['translated_text'] = result['translatedText']
        print(f"Original: {segment['text']} -> Traduzido: {segment['translated_text']}")

    return segments