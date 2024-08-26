import os
import logging

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import RecognitionConfig

logging.basicConfig(level=logging.DEBUG)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sherger/Ace-sequencer.json"

client = speech.SpeechClient()

with open('C:/Users/Sherger/test.wav', 'rb') as audio_file:
    audio_data = audio_file.read()
    audio = speech.types.RecognitionAudio(dict(content=audio_data))

config = RecognitionConfig(
    encoding=RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=int("16000"),
    language_code='de-DE',
    audio_channel_count=2)
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
