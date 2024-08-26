import os
import logging
import pyaudio
import wave
import time
import threading
import queue

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import RecognitionConfig

logging.basicConfig(level=logging.DEBUG)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sherger/Ace-sequencer.json"

audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk_size = 8192  # increased chunk size
audio = pyaudio.PyAudio()
input_device_index = 1


def record_and_transcribe(output_file, transcript_queue):
    # Record audio input for 10 seconds
    duration_in_seconds = 4

    stream = audio.open(format=audio_format, channels=channels, rate=sample_rate, input=True,
                        frames_per_buffer=chunk_size,
                        input_device_index=input_device_index)

    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(audio.get_sample_size(audio_format))
        wav_file.setframerate(sample_rate)

        frames_recorded = 0
        while True:
            audio_data = stream.read(chunk_size)
            wav_file.writeframes(audio_data)
            frames_recorded += chunk_size

            elapsed_time = frames_recorded / sample_rate
            if elapsed_time >= duration_in_seconds:
                break

    stream.stop_stream()
    stream.close()

    # Transcribe audio using the Google Cloud Speech-to-Text API
    client = speech.SpeechClient()

    with open(output_file, 'rb') as audio_file:
        audio_data = audio_file.read()
        transcription_audio = speech.types.RecognitionAudio(content=audio_data)

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code='de-DE',
        audio_channel_count=channels)

    response = client.recognize(config=config, audio=transcription_audio)

    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript

    # Put the transcript in the queue
    transcript_queue.put(transcript)


def main():
    # Create two output files for recording
    output_file_1 = "C:/Users/Sherger/output1.wav"
    output_file_2 = "C:/Users/Sherger/output2.wav"
    current_output_file = output_file_1
    next_output_file = output_file_2

    # Create a queue to hold the transcribed text
    transcript_queue = queue.Queue()

    while True:
        print("restart loop")
        # Start recording into the current output file
        recording_thread = threading.Thread(target=record_and_transcribe, args=(current_output_file, transcript_queue))
        recording_thread.start()

        # Wait for the recording thread to finish
        recording_thread.join()

        # Get the transcript from the queue
        transcript = transcript_queue.get()

        # Print the transcript
        print('Transcript: {}'.format(transcript))

        # Swap the output file names
        current_output_file, next_output_file = next_output_file, current_output_file

        # Wait for 1 second before starting the next recording
        time.sleep(1)


if __name__ == '__main__':
    main()
