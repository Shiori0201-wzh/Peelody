# Peelody

**Peelody** is a local music source separation application built with Python and [Demucs](https://github.com/adefossez/demucs).

Peelody V1.1 provides both a command-line interface (CLI) and a graphical user interface (GUI). It accepts WAV and MP3 audio and separates a mixed track into four stems:

- `vocals.wav` — vocals
- `drums.wav` — drums and percussion
- `bass.wav` — bass
- `other.wav` — other musical components

The application runs source separation locally using a compatible NVIDIA GPU and CUDA-enabled PyTorch.

## Features

- **Four-stem separation** using pretrained Demucs models.
- **WAV and MP3 input** with file existence and extension validation.
- **Two model options in the GUI:**
  - `htdemucs` — the default standard model.
  - `htdemucs_ft` — an optional fine-tuned model.
- **CUDA acceleration** for local GPU inference.
- **Command-line interface** for scripted or terminal-based use.
- **Tkinter GUI** for interactive audio selection and separation.
- **Background task execution** to keep the GUI responsive during separation.
- **Task status and error reporting** through the GUI.
- **Default and custom output directories.**
- **One-click access** to the generated result directory.
- **Output organization** that helps prevent collisions between different inputs with the same filename.

The GUI uses `htdemucs` by default. Users can select `htdemucs_ft` when they want to try the fine-tuned model. The fine-tuned model may improve some stems but does not guarantee better results for every song or instrument.

## Tested Environment

The development and testing environment includes:

| Component | Tested configuration |
|---|---|
| Operating system | Windows 11, 64-bit |
| Python | 3.13.6 |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU, 8 GB |
| PyTorch | 2.14.0+cu132 |
| CUDA runtime used by PyTorch | 13.2 |
| Demucs | 4.1.0 |
| NumPy | 2.5.3 |
| Virtual environment | `.venv/` |

These are the versions recorded for the tested development environment. Other environments may require adjustments to Python, PyTorch, CUDA, or package versions.

The current separation implementation explicitly selects CUDA. A compatible NVIDIA GPU and working CUDA-enabled PyTorch installation are therefore required for the tested workflow.

## Project Structure

```text
Peelody/
├── .gitignore
├── LICENSE
├── README.md
├── SOURCES.md
├── TEST_RECORD.md
├── V11_MODEL_EVALUATION.md
├── requirements.txt
├── peelody.py
├── peelody_gui.py
├── check_outputs.py
├── env_check.py
└── inspect_wav.py
```

Important files:

| File | Purpose |
|---|---|
| `peelody.py` | Core separation logic and CLI entry point |
| `peelody_gui.py` | Tkinter graphical interface |
| `requirements.txt` | Pinned Python dependency versions |
| `TEST_RECORD.md` | Verified functional and regression tests |
| `V11_MODEL_EVALUATION.md` | V1.1 model comparison and quality evaluation |
| `SOURCES.md` | Third-party source and license notes |
| `check_outputs.py` | Output validation helper |
| `env_check.py` | Python environment inspection helper |
| `inspect_wav.py` | WAV file property inspection helper |
| `LICENSE` | MIT license for the Peelody source code |

The following local directories are intentionally excluded from Git:

```text
.venv/
samples/
outputs/
```

They contain the local virtual environment, test material, and generated separation results, respectively.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Shiori0201-wzh/Peelody.git
cd Peelody
```

If the repository has already been cloned, enter the existing project directory instead.

### 2. Create a virtual environment

The recorded development environment uses Python 3.13.6.

```powershell
py -3.13 -m venv .venv
```

### 3. Install dependencies

The dependency file pins the versions used in the tested environment.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu132
```

Installation may take some time because PyTorch and its CUDA-enabled packages are large.

If package installation fails, check the Python version, package availability, network connection, and compatibility of the requested PyTorch build before changing the pinned dependencies.

### 4. Verify GPU availability

Run:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA unavailable')"
```

The tested machine returned a result similar to:

```text
True
NVIDIA GeForce RTX 5060 Laptop GPU
```

If CUDA is unavailable, the current GPU separation workflow may fail. Verify the NVIDIA driver and PyTorch installation before running Peelody.

## Run the CLI

The CLI currently supports two command forms.

### Default output directory

```powershell
.\.venv\Scripts\python.exe peelody.py ".\samples\example.wav"
```

When no custom output directory is provided, results are stored under the project's `outputs/` directory.

### Custom output directory

```powershell
.\.venv\Scripts\python.exe peelody.py ".\samples\example.wav" ".\my_results"
```

The second argument specifies the output root directory. It is optional and is interpreted relative to the current working directory when a relative path is supplied.

**CLI model selection:** the current CLI uses `htdemucs` by default. Selecting `htdemucs_ft` is currently supported through the GUI, not through a separate CLI model argument.

### CLI output

A successful run produces terminal output similar to:

```text
Input accepted: ...
Starting separation...
Separation finished.
Output directory: ...
```

If input validation or separation fails, the program prints an error and exits with a nonzero status.

## Run the GUI

Start the graphical interface with:

```powershell
.\.venv\Scripts\python.exe peelody_gui.py
```

The GUI supports the following workflow:

1. Select a WAV or MP3 input file.
2. Choose the default output directory or specify a custom output root.
3. Select the separation model.
4. Optionally check the input file.
5. Start separation.
6. Wait for the task result.
7. Open the result directory when separation succeeds.

### Model selection

The GUI provides two options:

| Model | Description |
|---|---|
| `htdemucs` | Standard model; selected by default |
| `htdemucs_ft` | Fine-tuned model; optional alternative |

The selected model is passed from the GUI to the background worker and then to the shared separation function.

The model selector and relevant controls are disabled while a task is running. Task results are communicated back to the GUI through a thread-safe queue, and GUI widgets are updated by the main thread.

The application also prevents the user from closing the window through the normal window-close action while a separation task is running.

### Output directory controls

- **Choose output directory:** selects a custom output root.
- **Restore default:** clears the custom output setting and returns to the default `outputs/` root.
- **Open result directory:** opens the actual result folder after a successful task.

The output root selected by the user is different from the final result directory returned after separation.

## Output Structure

Peelody builds a job directory using the input file's parent directory name and filename stem:

```text
<parent folder name> - <input filename without extension>
```

For example, an input at:

```text
samples\example.wav
```

produces a job directory named:

```text
samples - example
```

With the default model and default output root, the output structure is:

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

When the GUI uses `htdemucs_ft`, the model directory becomes:

```text
htdemucs_ft/
```

The full path therefore follows this pattern:

```text
<output root>/
└── <job name>/
    └── <model name>/
        └── <input filename stem>/
            ├── bass.wav
            ├── drums.wav
            ├── other.wav
            └── vocals.wav
```

When a custom output root is supplied, only the output root changes. The job name, model directory, and final stem directory retain the same organization.

Including the input's parent folder name in the job name helps avoid collisions between different songs that share a filename such as `mixture.wav`.

## Input Validation and Error Handling

Peelody currently accepts:

```text
.wav
.mp3
```

The validation step checks that the input file exists and has a supported extension.

### Missing input file

Example:

```powershell
.\.venv\Scripts\python.exe peelody.py ".\samples\missing.wav"
```

Expected error:

```text
Error: input file does not exist.
```

### Unsupported extension

Example:

```powershell
.\.venv\Scripts\python.exe peelody.py ".\README.md"
```

Expected error:

```text
Error: Peelody V1 only supports WAV and MP3.
```

### Separation failure

A file may exist and have a supported extension but still contain invalid or unreadable audio.

In this case, Peelody reports:

```text
Input accepted: ...
Starting separation...
Error: audio separation failed.
```

The core function wraps a failed Demucs subprocess execution in a `RuntimeError`. The CLI catches the error, prints a concise message, and exits with status code `1`.

The GUI catches task exceptions in the worker, sends an error result through the queue, and displays the failure message.

The simplified CLI output suppresses Demucs standard output and standard error during normal execution. This keeps routine output concise but also means detailed Demucs diagnostics are not displayed by default.

## Model Evaluation

V1.1 includes exploratory comparisons between `htdemucs` and `htdemucs_ft` using two 7-second excerpts from MUSDB18-7-WAV:

- Al James - Schoolboy Facination
- AM Contra - Heart Peripheral

The evaluation used subjective A/B listening, SI-SDR comparisons, a repeated experiment on one excerpt, and a limited runtime comparison.

### Main observations

- The fine-tuned model improved the perceived continuity and recovery of some sounds in the `other` stem on both tested excerpts.
- SI-SDR results for `other` improved in both excerpts.
- The `drums` and `bass` results varied between excerpts. Improvements to one stem did not guarantee improvements to all other stems.
- `htdemucs` with `--shifts 2` produced only small SI-SDR gains in the tested excerpt, with no obvious subjective improvement.

### SI-SDR changes

The following table reports the SI-SDR change of `htdemucs_ft` relative to `htdemucs`, in dB.

| Stem | Al James | AM Contra, first run | AM Contra, repeated run |
|---|---:|---:|---:|
| Vocals | +0.09 | +0.28 | +0.14 |
| Drums | +0.43 | -0.27 | -0.21 |
| Bass | -0.35 | +0.17 | +0.25 |
| Other | +0.18 | +2.
