import os
import logging
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import RecognitionConfig

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sherger/Ace-sequencer.json"

def transcribe_audio(output_file, sample_rate):
    logging.basicConfig(level=logging.DEBUG)

    client = speech.SpeechClient()

    with open(output_file, 'rb') as audio_file:
        audio_data = audio_file.read()
        transcription_audio = speech.types.RecognitionAudio(content=audio_data)

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code='de-DE',
        audio_channel_count=1)

    response = client.recognize(config=config, audio=transcription_audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript