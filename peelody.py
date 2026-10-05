import sys
import subprocess
from pathlib import Path


def validate_input(audio_arg):
    input_path = Path(audio_arg)

    if not input_path.is_file():
        print("Error: input file does not exist.")
        sys.exit(1)

    if input_path.suffix.lower() not in {".wav", ".mp3"}:
        print("Error: Peelody V1 only supports WAV and MP3.")
        sys.exit(1)
    return input_path


def run_separation(input_path,custom_output_dir):
    project_dir = Path(__file__).resolve().parent
    
    track_name = input_path.parent.name
    job_name = f"{track_name} - {input_path.stem}"
    
    if custom_output_dir is None:
        output_dir = project_dir/"outputs"/job_name
    else:
        output_dir = custom_output_dir/job_name

    command = [
        sys.executable,
        "-m",
        "demucs",
        "-n",
        "htdemucs",
        "-d",
        "cuda",
        "-o",
        str(output_dir),
        str(input_path),
    ]
    print("Starting separation...")

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
)
    except subprocess.CalledProcessError:
        print("Error: audio separation failed.")
        sys.exit(1)

    result_dir = output_dir / "htdemucs" / input_path.stem
    return  result_dir


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Usage: python peelody.py <audio_file> [<output_dir>]")
        print("<audio_file> （必填）")
        print("<output_dir> （选填）")
        sys.exit(1)

    input_path = validate_input(sys.argv[1])

    if len(sys.argv) == 3:
        custom_output_dir = Path(sys.argv[2])
    else:
        custom_output_dir = None

    print("Input accepted:", input_path.resolve())

    result_dir = run_separation(input_path,custom_output_dir)

    print("Separation finished.")
    print("Output directory:", result_dir)


if __name__ == "__main__":
    main()