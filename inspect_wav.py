import wave

file_path = "samples/MUSDB18-7-WAV/test/Al James - Schoolboy Facination/mixture.wav"

audio = wave.open(file_path, "rb")

channels = audio.getnchannels()
sample_rate = audio.getframerate()
sample_width = audio.getsampwidth()
frames = audio.getnframes()
duration = frames / sample_rate

print("Channels:", channels)
print("Sample rate:", sample_rate)
print("Sample width:", sample_width)
print("Frames:", frames)
print("Duration:", duration)

audio.close()
