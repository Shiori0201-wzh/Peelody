Peelody
Peelody is a local music source separation application built with Python
and Demucs.
Peelody V1.1 provides a command-line interface (CLI) and a Tkinter
graphical user interface (GUI). It accepts WAV and MP3 audio and
separates a mixed track into four stems:
- vocals.wav --- vocals
- drums.wav --- drums and percussion
- bass.wav --- bass
- other.wav --- other musical components
Separation runs locally using a compatible NVIDIA GPU and CUDA-enabled
PyTorch.
Features
- Four-stem source separation.
- WAV and MP3 input validation.
- Two model options in the GUI: htdemucs (standard, default) and
  htdemucs_ft (optional fine-tuned model).
- CUDA acceleration.
- CLI support for terminal-based use.
- Tkinter GUI with background task execution, status reporting, and
  error handling.
- Default or custom output directory.
- One-click opening of the result directory.
- Organized output paths to help avoid filename collisions.
The fine-tuned model may improve some stems, but it does not guarantee
better results for every song or instrument.
Tested Environment
  Component                      Tested configuration
  Operating system               Windows 11, 64-bit
  Python                         3.13.6
  GPU                            NVIDIA GeForce RTX 5060 Laptop GPU, 8 GB
  PyTorch                        2.14.0+cu132
  CUDA runtime used by PyTorch   13.2
  Demucs                         4.1.0
  NumPy                          2.5.3
These are the versions recorded for the tested development environment.
Other environments may require compatible Python, PyTorch, CUDA, and
package versions. The current separation implementation explicitly
selects CUDA.
Project Structure
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
- peelody.py: core separation logic and CLI entry point.
- peelody_gui.py: Tkinter graphical interface.
- requirements.txt: pinned Python dependencies.
- TEST_RECORD.md: functional and regression test record.
- V11_MODEL_EVALUATION.md: V1.1 model comparison and quality
  evaluation.
- SOURCES.md: third-party source and license notes.
The local .venv/, samples/, and outputs/ directories are excluded
from Git. They contain the virtual environment, test audio, and
generated results.
Installation
1. Clone the repository
git clone https://github.com/Shiori0201-wzh/Peelody.git
cd Peelody
2. Create a virtual environment
The recorded development environment uses Python 3.13.6.
py -3.13 -m venv .venv
3. Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu132
4. Verify GPU availability
.\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA unavailable')"
The tested machine returned True and
NVIDIA GeForce RTX 5060 Laptop GPU. If CUDA is unavailable, verify the
NVIDIA driver and PyTorch installation.
Run the CLI
The CLI currently uses htdemucs by default and does not expose a
separate model-selection argument.
Default output directory
.\.venv\Scripts\python.exe peelody.py ".\samples\example.wav"
Results are stored under the project's outputs/ directory.
Custom output directory
.\.venv\Scripts\python.exe peelody.py ".\samples\example.wav" ".\my_results"
The second argument is optional. Relative paths are interpreted relative
to the current working directory.
A successful run produces output similar to:
Input accepted: ...
Starting separation...
Separation finished.
Output directory: ...
Run the GUI
.\.venv\Scripts\python.exe peelody_gui.py
The GUI lets users select an input file, choose a default or custom
output directory, select a model, check the input, start separation,
view the task result, and open the result directory.
  Model           Description
  htdemucs      Standard model; selected by default
  htdemucs_ft   Optional fine-tuned model
The GUI passes the selected model to the background worker and shared
separation function. Relevant controls are disabled while a task is
running. Task results are returned through a thread-safe queue, and GUI
widgets are updated by the main thread. The normal window-close action
is blocked while separation is running.
Output directory controls
- Choose output directory: selects a custom output root.
- Restore default: clears the custom path and returns to the
  default outputs/ root.
- Open result directory: opens the actual result folder after a
  successful task.
Output Structure
Peelody creates a job name from the input's parent folder and filename
stem. For example, samples\\example.wav produces samples - example.
<output root>/
└── <job name>/
    └── <model name>/
        └── <input filename stem>/
            ├── bass.wav
            ├── drums.wav
            ├── other.wav
            └── vocals.wav
The model directory is htdemucs/ or htdemucs_ft/, depending on the
selected model. Including the input's parent folder in the job name
helps avoid collisions between inputs with the same filename.
Input Validation and Error Handling
Supported extensions are .wav and .mp3. Peelody checks that the
input exists and has a supported extension before starting separation.
Missing input:
Error: input file does not exist.
Unsupported extension:
Error: Peelody V1 only supports WAV and MP3.
If a file exists and has a supported extension but cannot be processed,
the CLI reports:
Input accepted: ...
Starting separation...
Error: audio separation failed.
The CLI exits with status code 1 on validation or separation failure.
Demucs standard output and standard error are suppressed during normal
CLI execution, so detailed internal diagnostics are not shown by
default. The GUI reports task failures in its status area.
Model Evaluation
V1.1 includes exploratory comparisons between htdemucs and
htdemucs_ft using two 7-second MUSDB18-7-WAV excerpts:
- Al James - Schoolboy Facination
- AM Contra - Heart Peripheral
Subjective A/B listening found that the fine-tuned model improved the
perceived continuity and recovery of some sounds in the other stem on
both excerpts. Results for drums and bass varied. htdemucs with
--shifts 2 showed only small SI-SDR gains in the tested excerpt, with
no obvious subjective improvement.
SI-SDR change
The following values are the SI-SDR difference of htdemucs_ft relative
to htdemucs, in dB. Positive values indicate a higher score; negative
values indicate a lower score.
  Stem              Al James   AM Contra, first run   AM Contra, repeated run
  Vocals               +0.09                  +0.28                     +0.14
  Drums                +0.43                  -0.27                     -0.21
  Bass                 -0.35                  +0.17                     +0.25
  Other                +0.18                  +2.96                     +2.31
  Other (0--3s)        -0.01                  +4.27                     +3.84
One runtime test on the 7-second AM Contra excerpt measured 5.53 seconds
for htdemucs and 7.86 seconds for htdemucs_ft (about 42% longer in
that run). The measurement includes Python startup, model loading, and
separation, so it is not a general benchmark.
Limitations
- Only two 7-second excerpts were tested.
- Repeated experiments were limited, and time-shift inference can
  cause run-to-run variation.
- SI-SDR was calculated separately for the two stereo channels and the
  resulting dB values were averaged.
- Sample-level time-offset correction was not performed.
- Subjective listening and SI-SDR do not always agree.
- The results do not establish performance across full songs, diverse
  genres, or all instruments.
These are exploratory results, not a guarantee of improved quality. See
[V11_MODEL_EVALUATION.md](V11_MODEL_EVALUATION.md) for the recorded
experiments.
Model selection decision
The GUI provides two models:
- Standard: htdemucs, selected by default.
- Optional fine-tuned: htdemucs_ft.
The standard model remains the default because it is the established
baseline and was faster in the measured short-audio test. The fine-tuned
model is an alternative, especially for users who want to compare the
other stem. It is not universally superior. The CLI continues to use
htdemucs and has no separate model-selection argument.
Testing
Tests performed during development include:
- Valid WAV and MP3 input.
- Missing file, unsupported extension, and broken WAV handling.
- Four-stem output generation and basic output properties.
- Default and custom output directories.
- Different inputs sharing the same filename.
- GUI file selection, model selection, task status, error reporting,
  and result-directory opening.
- Real GUI separation with both htdemucs and htdemucs_ft.
- Control disabling and window responsiveness during a running task.
- CLI compatibility with one-argument and two-argument command forms.
- Mock tests for model parameter passing and rejection of unsupported
  model names.
- Python syntax checks using py_compile.
See [TEST_RECORD.md](TEST_RECORD.md) for the functional test history and
[V11_MODEL_EVALUATION.md](V11_MODEL_EVALUATION.md) for model evaluation
details. These tests are not exhaustive across all systems and audio.
Licensing and Third-Party Material
Peelody's source code is provided under the MIT License in
LICENSE.
Third-party software, pretrained model weights, and test audio have
separate licensing terms:
- Demucs: the project records Demucs 4.1.0 and its MIT license in
  [SOURCES.md](SOURCES.md).
- Pretrained weights: do not assume the Demucs software license
  automatically applies to the model weights. The recorded source
  notes say the license for the HTDemucs weights was not clearly
  specified on the model card. Re-check current terms before
  redistribution.
- MUSDB18-7-WAV: used locally for educational evaluation. The
  project source notes identify restrictions on commercial use without
  permission from the relevant copyright holders.
- Input and output audio: users are responsible for the rights and
  permissions applicable to their recordings and generated stems.
Model weights, local test audio, and generated outputs are not included
in this repository. See [SOURCES.md](SOURCES.md) for details.
Current Status
Peelody V1.1 provides a local four-stem separation workflow with a CLI,
a Tkinter GUI, two selectable GUI models, custom output paths, input
validation, background execution, and task-result reporting.
The current quality evaluation is exploratory. The fine-tuned model is
an optional alternative, not a universally superior replacement for the
standard model.
