import sys
import wave
from pathlib import Path

result_dir  = Path(sys.argv[1])

track_names = [
    "bass.wav",
    "drums.wav",
    "other.wav",
    "vocals.wav",
]

for track_name in track_names:
    track_path = result_dir / track_name

    if not track_path.is_file():
        print("Missing:",track_name)
        continue

    with wave.open(str(track_path),"rb") as audio:
        channels = audio.getnchannels()
        sample_rate  = audio.getframerate()
        frames = audio.getnframes()
        duration = frames / sample_rate

    print(
        track_name,
        "| channels:", channels,
        "| sample rate:", sample_rate,
        "| duration:", duration,
    )

    



