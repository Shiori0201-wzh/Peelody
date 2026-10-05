# Peelody

Peelody is a local audio source separation project developed with Python.

Peelody V1 accepts WAV or MP3 audio and separates it into four tracks:

- vocals
- drums
- bass
- other

The current version uses the pretrained `htdemucs` model from Demucs and performs separation locally with an NVIDIA CUDA GPU.

---

## Features

Peelody V1 currently supports:

- WAV input
- MP3 input
- Four-track source separation
  - `vocals.wav`
  - `drums.wav`
  - `bass.wav`
  - `other.wav`
- NVIDIA GPU acceleration through CUDA
- Input file existence checking
- Input extension checking
- Broken audio handling
- Default output directory
- Optional custom output directory
- Separate output folders for inputs with the same filename
- Simplified terminal output
- Fixed test records and dependency records

---

## Tested Environment

Peelody V1 has been tested in the following environment:

- OS: Windows 11 64-bit
- Python: 3.13.6
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU 8GB
- PyTorch: 2.14.0+cu132
- CUDA runtime used by PyTorch: 13.2
- NumPy: 2.5.3
- Demucs: 4.1.0
- Separation model: `htdemucs`

The current V1 explicitly uses CUDA for separation, so a compatible NVIDIA GPU is required.

---

## Project Structure

A typical Peelody project directory looks like this:

```text
Peelody/
├── .venv/
├── outputs/
├── samples/
├── .gitignore
├── README.md
├── SOURCES.md
├── TEST_RECORD.md
├── requirements.txt
├── peelody.py
├── check_outputs.py
├── env_check.py
└── inspect_wav.py
```

Important notes:

- `.venv/` contains the local Python virtual environment.
- `samples/` contains local test audio and is not included in Git.
- `outputs/` contains generated separated tracks and is not included in Git.
- `peelody.py` is the main Peelody program.
- `TEST_RECORD.md` contains verified test results.
- `SOURCES.md` contains third-party source and license notes.
- `requirements.txt` records the tested Python dependency versions.

---

## Setup

### 1. Create a virtual environment

Open PowerShell in the Peelody project directory:

```powershell
cd D:\Projects\Peelody
```

Create the virtual environment:

```powershell
py -3.13 -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the PowerShell prompt should contain:

```text
(.venv)
```

### 3. Install the tested dependencies

```powershell
python -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu132
```

The tested environment includes:

```text
demucs==4.1.0
numpy==2.5.3
torch==2.14.0+cu132
```

`requirements.txt` also contains the indirect dependencies installed in the tested virtual environment.

---

## Verify GPU Support

Before running Peelody, verify that PyTorch can access the NVIDIA GPU:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

The tested system produces output similar to:

```text
True
NVIDIA GeForce RTX 5060 Laptop GPU
```

If `torch.cuda.is_available()` returns `False`, the current Peelody V1 separation command will not work correctly because V1 explicitly uses CUDA.

---

## Run Peelody

Peelody supports two command forms.

### Default output directory

```powershell
python peelody.py "<audio_file>"
```

Example:

```powershell
python peelody.py ".\samples\example.wav"
```

When no output directory is provided, Peelody stores the result under the project's:

```text
outputs\
```

directory.

---

### Custom output directory

You can optionally provide a second argument:

```powershell
python peelody.py "<audio_file>" "<output_dir>"
```

Example:

```powershell
python peelody.py ".\samples\example.wav" ".\my_results"
```

In this case, Peelody stores the separated tracks under the specified output root instead of the default `outputs` directory.

If a relative custom output path is used, it is relative to the directory from which the command is executed.

---

## Supported Input Formats

Peelody V1 accepts:

```text
.wav
.mp3
```

Examples:

```powershell
python peelody.py ".\samples\song.wav"
```

```powershell
python peelody.py ".\samples\song.mp3"
```

Other file extensions are rejected before separation starts.

---

## Output Structure

Peelody creates a job directory using:

```text
<input parent folder name> - <input filename without extension>
```

For example, if the input is:

```text
samples\example.wav
```

the job name becomes:

```text
samples - example
```

With the default output root, the result structure is approximately:

```text
outputs/
└── samples - example/
    └── htdemucs/
        └── example/
            ├── bass.wav
            ├── drums.wav
            ├── other.wav
            └── vocals.wav
```

With a custom output root such as:

```text
my_results
```

the result becomes approximately:

```text
my_results/
└── samples - example/
    └── htdemucs/
        └── example/
            ├── bass.wav
            ├── drums.wav
            ├── other.wav
            └── vocals.wav
```

Using both the parent folder name and input filename helps prevent different files with the same filename from overwriting each other's results.

---

## Command-Line Usage

If no audio file is provided, Peelody displays usage information.

Valid forms:

```text
python peelody.py <audio_file>
```

```text
python peelody.py <audio_file> <output_dir>
```

`<audio_file>` is required.

`<output_dir>` is optional.

Too many command-line arguments are rejected.

---

## Error Handling

Peelody V1 currently handles several common errors.

### Input file does not exist

Example:

```powershell
python peelody.py ".\samples\missing.wav"
```

Result:

```text
Error: input file does not exist.
```

### Unsupported extension

Example:

```powershell
python peelody.py ".\example.txt"
```

Result:

```text
Error: Peelody V1 only supports WAV and MP3.
```

### Broken or unreadable audio

If a file exists and has a supported extension but cannot actually be processed as audio, Peelody reports:

```text
Error: audio separation failed.
```

Demucs internal traceback output is hidden in normal Peelody V1 usage.

---

## Terminal Output

A normal successful run looks approximately like:

```text
Input accepted: ...
Starting separation...
Separation finished.
Output directory: ...
```

A failed separation looks approximately like:

```text
Input accepted: ...
Starting separation...
Error: audio separation failed.
```

Peelody V1 intentionally hides the detailed Demucs terminal output to keep normal usage simple.

---

## Model Download

The `htdemucs` pretrained model files are downloaded automatically when the model is used for the first time.

Later runs can use the locally cached model files.

Internet access may therefore be required during the first model download.

---

## Testing

Peelody V1 has been tested with both WAV and MP3 input.

Testing includes:

- Valid WAV input
- Valid MP3 input
- Missing file
- Unsupported file extension
- Broken WAV file
- Four-track output generation
- Output file existence
- Output channel count
- Output sample rate
- Output duration
- Different inputs with the same filename
- Default output directory
- Custom output directory
- No command-line arguments
- Too many command-line arguments

Detailed verified test results are recorded in:

```text
TEST_RECORD.md
```

---

## Standard Test Material

A short MUSDB18 / SiSEC18-MUS sample was used as fixed local test material.

The tested standard sample includes Ground Truth tracks for:

- vocals
- drums
- bass
- other

The test audio itself is not included in the Git repository.

See:

```text
SOURCES.md
```

for source and license notes.

---

## Current Quality Observations

Current listening tests indicate:

- `vocals.wav` can be close to the Ground Truth on the tested sample.
- `bass.wav` showed no obvious major issue in the tested sample.
- `drums.wav` preserved the main drum content, but the Ground Truth sounded richer.
- `other.wav` showed the most obvious difference and had a somewhat discontinuous or stuttering artifact in the tested sample.

These are subjective listening observations.

No formal objective separation metric such as SDR or SI-SDR has been calculated yet.

Therefore, Peelody does not currently claim a numerical separation accuracy.

---

## Known Limitations

Peelody V1 currently has several limitations:

- Separation quality depends on the input audio.
- The `other` stem can contain noticeable separation artifacts.
- The model does not individually identify every instrument inside `other.wav`.
- The current V1 always uses CUDA and does not provide a CPU fallback.
- The current terminal interface does not display Demucs progress bars.
- V1 supports WAV and MP3 only.
- Objective source-separation metrics have not yet been integrated.
- More detailed instrument categories such as guitar or piano are not part of the required V1 output.

---

## Helper Scripts

### `env_check.py`

Used during environment verification.

It helps confirm which Python interpreter is currently running.

### `inspect_wav.py`

Used to inspect basic WAV properties such as:

- channels
- sample rate
- sample width
- frame count
- duration

### `check_outputs.py`

Used to check the generated output tracks, including:

- file existence
- channel count
- sample rate
- duration

These scripts are helper and testing tools and are not part of the main separation flow.

---

## Main Program Flow

The simplified Peelody V1 data flow is:

```text
Command-line arguments
        ↓
main()
        ↓
validate_input()
        ↓
input_path
        ↓
run_separation()
        ↓
Demucs / htdemucs
        ↓
PyTorch + CUDA
        ↓
RTX GPU
        ↓
bass / drums / other / vocals
        ↓
result_dir
```

The main responsibilities are:

- `main()` manages the overall execution order and optional output directory.
- `validate_input()` checks the input file.
- `run_separation()` runs Demucs and returns the result directory.

---

## Dependency and License Notes

Third-party source and license information is recorded separately in:

```text
SOURCES.md
```

Important distinctions are made between:

- Peelody source code
- Demucs software
- HTDemucs pretrained weights
- PyTorch
- Test datasets
- User-provided audio
- Generated separated audio

Do not assume that the license of one component automatically applies to another component.

---

## Repository Policy

The Git repository should contain source code and project documentation.

The following are intentionally excluded:

```text
.venv/
samples/
outputs/
```

Test audio, generated separated tracks, and the local virtual environment should not be committed to the repository.

---

## Project Status

Peelody V1 currently provides a working local four-track audio separation workflow with:

- WAV and MP3 input
- NVIDIA GPU acceleration
- four-track separation
- input validation
- basic error handling
- stable output organization
- optional custom output directory
- fixed testing records
- dependency records
- source and license notes
- Git-based version protection