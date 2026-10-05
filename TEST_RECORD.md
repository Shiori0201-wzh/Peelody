# Peelody V1 Test Record

This document records tests that were actually performed during Peelody V1 development.

It does not claim results that were not measured.

---

## 1. Tested Environment

Peelody V1 was developed and tested on:

- OS: Windows 11 64-bit
- Python: 3.13.6
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU 8GB
- System RAM: 16 GB
- PyTorch: 2.14.0+cu132
- CUDA runtime used by PyTorch: 13.2
- NumPy: 2.5.3
- Demucs: 4.1.0
- Separation model: `htdemucs`

The Peelody Python virtual environment is located under:

```text
D:\Projects\Peelody\.venv
```

The Python interpreter used by Peelody was verified as:

```text
D:\Projects\Peelody\.venv\Scripts\python.exe
```

---

## 2. GPU Verification

PyTorch successfully detected the NVIDIA GPU.

Verified output included:

```text
Torch: 2.14.0+cu132
CUDA available: True
CUDA runtime: 13.2
GPU: NVIDIA GeForce RTX 5060 Laptop GPU
```

A real CUDA tensor operation was also performed.

Input tensor:

```text
[1.0, 2.0, 3.0]
```

GPU operation:

```text
x * 2
```

Verified output:

```text
Device: cuda:0
Result: [2.0, 4.0, 6.0]
```

Result:

- PyTorch installation -> PASS
- CUDA detection -> PASS
- RTX 5060 detection -> PASS
- Real GPU tensor computation -> PASS

---

## 3. Standard Test Dataset

The fixed source-separation test material was taken from:

```text
MUSDB18-7-WAV
```

The local archive used during development was:

```text
MUSDB18-7-WAV.zip
```

Verified archive size:

```text
932814752 bytes
```

Recorded SHA256:

```text
A32B8D6F530CA39D75954179149611927F28367F51134B68F3E2CDA963532FF6
```

The extracted dataset contains:

```text
train/
test/
```

The main fixed test track used during development was:

```text
MUSDB18-7-WAV/test/Al James - Schoolboy Facination/
```

Files verified inside that track directory:

```text
accompaniment.wav
bass.wav
drums.wav
mixture.wav
other.wav
vocals.wav
```

The following four files were used as Ground Truth stems:

```text
bass.wav
drums.wav
other.wav
vocals.wav
```

The model input was:

```text
mixture.wav
```

---

## 4. Standard WAV Input Properties

The fixed `mixture.wav` sample was inspected using Python's `wave` module.

Verified properties:

```text
Channels: 2
Sample rate: 44100
Sample width: 2
Frames: 308700
Duration: 7.0
```

Interpretation:

- Channels: 2
- Stereo audio
- Sample rate: 44100 Hz
- Sample width: 2 bytes per channel sample
- Sample width corresponds to 16-bit samples
- Frame count: 308700
- Duration: 7.0 seconds

The duration relationship was verified as:

```text
308700 / 44100 = 7.0 seconds
```

---

## 5. First Demucs Separation Test

The first direct Demucs test used:

```text
htdemucs
```

with:

```text
CUDA
```

The input was:

```text
Al James - Schoolboy Facination/mixture.wav
```

The separation completed successfully.

Generated model outputs:

```text
bass.wav
drums.wav
other.wav
vocals.wav
```

Result:

- Demucs model loading -> PASS
- CUDA model execution -> PASS
- Four-track generation -> PASS
- Output WAV creation -> PASS

---

## 6. Ground Truth Listening Comparison

The Demucs output was listened to and compared with the corresponding Ground Truth stems.

### vocals

Observation:

- Very close to the Ground Truth
- No obvious accompaniment leakage was heard

### bass

Observation:

- No obvious major problem was heard

### drums

Observation:

- Main drum sound was relatively close to the Ground Truth
- Ground Truth sounded richer
- The Ground Truth appeared to contain more detailed or varied percussion content

The exact missing drum components were not objectively identified.

### other

Observation:

- This stem showed the most obvious difference
- The separated output had a noticeable discontinuous or stuttering-like character

This was recorded as a likely model separation artifact or model limitation rather than immediately assuming an application-code failure.

---

## 7. Quality Evaluation Boundary

Current quality observations are mainly based on:

- Listening
- Output file existence
- File properties
- Comparison with available Ground Truth stems

No formal objective separation metric has been calculated yet.

The project has not calculated metrics such as:

```text
SDR
SI-SDR
```

Therefore Peelody V1 does not claim:

- A numerical accuracy
- A percentage improvement
- A formal objective separation score

---

## 8. WAV Input Test

A valid WAV input was successfully accepted by Peelody.

Verified flow:

```text
WAV input
→ input validation
→ Demucs
→ CUDA
→ four output stems
```

Result:

```text
PASS
```

---

## 9. MP3 Input Test

A real MP3 file was tested using:

```text
mp3_test.mp3
```

Peelody accepted the MP3 input and successfully completed separation.

Result:

```text
MP3 input accepted -> PASS
Four-track separation -> PASS
```

This demonstrated that MP3 support was not only allowed by the extension check, but actually worked in the tested environment.

---

## 10. MP3 Output Property Test

The four WAV outputs generated from `mp3_test.mp3` were inspected.

Verified results:

```text
bass.wav
channels: 2
sample rate: 44100
duration: 158.1191836734694
```

```text
drums.wav
channels: 2
sample rate: 44100
duration: 158.1191836734694
```

```text
other.wav
channels: 2
sample rate: 44100
duration: 158.1191836734694
```

```text
vocals.wav
channels: 2
sample rate: 44100
duration: 158.1191836734694
```

Result:

- `bass.wav` exists -> PASS
- `drums.wav` exists -> PASS
- `other.wav` exists -> PASS
- `vocals.wav` exists -> PASS
- All four tracks are stereo -> PASS
- All four tracks use 44100 Hz -> PASS
- All four tracks have matching duration -> PASS

---

## 11. No-Argument Test

Command:

```text
python peelody.py
```

Expected behavior:

- Do not start separation
- Print usage information

Verified result:

```text
Usage: python peelody.py <audio_file> [<output_dir>]
<audio_file> （必填）
<output_dir> （选填）
```

Result:

```text
PASS
```

---

## 12. Missing File Test

Command tested with a nonexistent WAV file.

Example:

```text
python peelody.py .\samples\missing.wav
```

Verified output:

```text
Error: input file does not exist.
```

Result:

```text
PASS
```

---

## 13. Unsupported Extension Test

An existing Python file was supplied as input:

```text
env_check.py
```

Verified output:

```text
Error: Peelody V1 only supports WAV and MP3.
```

Result:

```text
PASS
```

---

## 14. Broken WAV Test

A deliberately invalid WAV file was created:

```text
samples\broken.wav
```

Its content was plain text rather than valid audio.

The file:

- Existed
- Used the `.wav` extension
- Passed the basic path and extension checks
- Failed when Demucs attempted to process it

Peelody correctly detected the Demucs failure.

Verified final output:

```text
Error: audio separation failed.
```

The program did not incorrectly print:

```text
Separation finished.
```

Result:

```text
PASS
```

---

## 15. Simplified Error Output Test

Originally, a broken audio file caused Demucs to print a long internal traceback.

Peelody was changed to hide Demucs standard output and error output during normal execution.

After the change, broken audio produced a simplified result:

```text
Input accepted: ...
Starting separation...
Error: audio separation failed.
```

Normal successful separation produced:

```text
Input accepted: ...
Starting separation...
Separation finished.
Output directory: ...
```

Result:

```text
PASS
```

Decision:

Peelody V1 keeps the simplified terminal output.

Detailed Demucs progress bars and internal traceback are not shown during normal use.

---

## 16. Output Root Test

Peelody output was changed so that the default output root is based on the project directory rather than the current terminal directory.

Peelody was launched while PowerShell was located outside the project directory.

The result still went to:

```text
D:\Projects\Peelody\outputs
```

instead of creating an unexpected output directory under the current PowerShell location.

Result:

```text
PASS
```

---

## 17. Duplicate Filename Collision Test

Two different MUSDB18 songs both contained a file named:

```text
mixture.wav
```

Test inputs included:

```text
Al James - Schoolboy Facination\mixture.wav
```

and:

```text
AM Contra - Heart Peripheral\mixture.wav
```

Using only:

```text
input_path.stem
```

caused both inputs to use:

```text
mixture
```

as the same output directory name.

This was verified as a real overwrite/collision problem.

The output job name was changed to use:

```text
<input parent directory name> - <input stem>
```

Verified resulting job directories included:

```text
Al James - Schoolboy Facination - mixture
```

and:

```text
AM Contra - Heart Peripheral - mixture
```

Result:

```text
PASS
```

Different songs with the same input filename no longer use the same job directory in this tested case.

---

## 18. Main Program Structure Regression Test

Peelody was refactored into three main responsibilities:

```text
main()
validate_input()
run_separation()
```

Responsibilities:

### `main()`

- Handles command-line argument flow
- Controls overall execution order
- Reads the optional custom output directory

### `validate_input()`

- Converts the audio argument to `Path`
- Checks that the input file exists
- Checks that the extension is WAV or MP3
- Returns the validated `input_path`

### `run_separation()`

- Builds the output path
- Builds the Demucs command
- Executes Demucs
- Handles separation failure
- Returns the final `result_dir`

Regression testing after refactoring confirmed that previous behavior remained working.

Result:

```text
PASS
```

---

## 19. Program Data Flow

Verified simplified data flow:

```text
main()
  ↓
sys.argv
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
GPU source separation
  ↓
result_dir
  ↓
output WAV files
```

---

## 20. Final Independent Modification Test

### Feature

Optional custom output directory.

The feature was implemented as the final independent modification exercise.

Peelody now supports:

```text
python peelody.py <audio_file>
```

and:

```text
python peelody.py <audio_file> <output_dir>
```

`<audio_file>` is required.

`<output_dir>` is optional.

---

### Syntax Test

Command:

```text
python -m py_compile peelody.py
```

Verified result:

- No syntax error output
- Compilation check completed successfully

Result:

```text
PASS
```

---

### Default Output Directory Test

Command form:

```text
python peelody.py <audio_file>
```

Verified behavior:

- Separation completed successfully
- Default Peelody output root was used

Verified output path began with:

```text
D:\Projects\Peelody\outputs\
```

Result:

```text
PASS
```

---

### Custom Output Directory Test

Command form:

```text
python peelody.py <audio_file> ".\my_results"
```

Verified behavior:

- Separation completed successfully
- The supplied custom directory was used as the output root

Verified output path began with:

```text
my_results\
```

instead of the default:

```text
outputs\
```

Result:

```text
PASS
```

---

### No-Argument Test After Modification

Command:

```text
python peelody.py
```

Verified behavior:

- Program did not begin separation
- Usage information was displayed

Result:

```text
PASS
```

---

### Too-Many-Arguments Test

Command:

```text
python peelody.py a.wav out extra
```

Verified behavior:

- Program rejected the argument count
- Usage information was displayed
- Separation did not begin

Result:

```text
PASS
```

---

### Existing Collision Protection

The existing job naming logic remained:

```text
<input parent directory name> - <input stem>
```

The custom output directory feature did not remove this behavior.

Result:

```text
PASS
```

---

### Final Independent Modification Data Flow

When no custom output directory is supplied:

```text
main()
  ↓
custom_output_dir = None
  ↓
run_separation()
  ↓
project directory / outputs
  ↓
job_name
  ↓
Demucs output
```

When a custom output directory is supplied:

```text
main()
  ↓
Path(sys.argv[2])
  ↓
custom_output_dir
  ↓
run_separation()
  ↓
custom output root
  ↓
job_name
  ↓
Demucs output
```

Result:

```text
PASS
```

---

## 21. Git Version Protection

Peelody V1 has been placed under Git version control.

Verified historical commits include:

```text
7e757a1 Peelody V1 stable baseline
```

and:

```text
ecf1b74 Add V1 documentation and dependency records
```

The repository successfully preserved these commits even after the Windows Git application itself had to be reinstalled.

This demonstrated that:

```text
Git application installation
```

and:

```text
the project's .git repository history
```

are separate.

The local Git repository survived and the commit history remained readable after Git was reinstalled.

---

## 22. Files Excluded from Git

The following project content is intentionally excluded from Git:

```text
.venv/
samples/
outputs/
```

Reasons:

### `.venv/`

Contains the local Python virtual environment and installed dependencies.

These can be recreated from:

```text
requirements.txt
```

### `samples/`

Contains local test audio and dataset material.

Test audio is not part of the Peelody source repository.

### `outputs/`

Contains generated separated audio.

Generated output is not source code.

---

## 23. Helper Scripts

### `env_check.py`

Used to verify the Python environment and interpreter.

### `inspect_wav.py`

Used to inspect WAV properties including:

- Channels
- Sample rate
- Sample width
- Frame count
- Duration

### `check_outputs.py`

Used to verify generated output tracks including:

- File existence
- Channels
- Sample rate
- Duration

These helper scripts support testing and investigation.

They are not part of the main source-separation execution flow.

---

## 24. Current Known Limitations

Peelody V1 currently has the following known limitations:

- Separation quality depends on the input audio.
- `other.wav` showed the most noticeable artifact in the standard listening test.
- `other.wav` does not mean that every remaining instrument has been individually identified.
- The tested `drums.wav` output sounded less rich than the Ground Truth.
- Current V1 separation explicitly uses CUDA.
- No CPU fallback has been implemented.
- Only WAV and MP3 input are supported by the V1 input validation.
- The normal terminal interface does not display Demucs progress bars.
- No formal SDR or SI-SDR evaluation has been integrated.
- More detailed stems such as guitar or piano are not required V1 outputs.
- The current collision-prevention rule is practical for V1 but is not guaranteed to create a mathematically unique job ID for every possible file location.

---

## 25. Final V1 Verification Summary

The following capabilities have been actually verified:

| Test | Result |
|---|---|
| Python virtual environment | PASS |
| Correct Peelody Python interpreter | PASS |
| PyTorch installation | PASS |
| CUDA available | PASS |
| RTX 5060 GPU detected | PASS |
| Real GPU tensor operation | PASS |
| Demucs installation | PASS |
| HTDemucs model execution | PASS |
| WAV input | PASS |
| MP3 input | PASS |
| Four-track separation | PASS |
| `bass.wav` generated | PASS |
| `drums.wav` generated | PASS |
| `other.wav` generated | PASS |
| `vocals.wav` generated | PASS |
| Output properties checked | PASS |
| Missing file handling | PASS |
| Unsupported extension handling | PASS |
| Broken audio handling | PASS |
| Simplified user error output | PASS |
| Stable default output root | PASS |
| Same-filename collision mitigation | PASS |
| Optional custom output directory | PASS |
| No-argument handling | PASS |
| Too-many-arguments handling | PASS |
| Python syntax check | PASS |
| Git stable baseline | PASS |
| Dependency record | PASS |
| README | PASS |
| Source/license notes | PASS |

---

## 26. Evaluation Boundary

A successful V1 test means:

- The program runs in the tested environment.
- Supported inputs can be processed.
- Four output tracks are generated.
- Basic output properties are reasonable.
- Common invalid-input cases are handled.
- The project can be reproduced and maintained from recorded files.

It does not mean:

- Every song will separate perfectly.
- Every musical instrument can be individually identified.
- The model has a proven numerical accuracy.
- Generated stems are free from artifacts.
- Generated audio automatically has independent copyright or redistribution rights.

For source and license information, see:

```text
SOURCES.md
```

For installation and usage instructions, see:

```text
README.md
```