import pyaudio
import wave

audio_format = pyaudio.paInt16
channels = 1
chunk_size = 1024
audio = pyaudio.PyAudio()

def record_audio(output_file, duration_in_seconds, sample_rate):
    audio_format = pyaudio.paInt16
    channels = 1
    chunk_size = 1024
    audio = pyaudio.PyAudio()
    input_device_index = 1
    stream = audio.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size,
                        input_device_index=input_device_index)

    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(audio.get_sample_size(audio_format))
        wav_file.setframerate(sample_rate)

        frames_recorded = 0
        elapsed_time = 0  # Add a variable to keep track of elapsed time
        while True:
            audio_data = stream.read(chunk_size)
            wav_file.writeframes(audio_data)
            frames_recorded += chunk_size

            elapsed_time += chunk_size / sample_rate  # Update elapsed time with each iteration

            if elapsed_time >= duration_in_seconds:
                elapsed_time = 0  # Reset elapsed time to 0
                break  # Remove the break statement to keep looping

    stream.stop_stream()
    stream.close()
    audio.terminate()