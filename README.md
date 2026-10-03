\# Peelody



Peelody is a local audio source separation project.



Peelody V1 accepts WAV or MP3 audio and separates it into four tracks:



\- vocals

\- drums

\- bass

\- other



\## Environment



Tested environment:



\- Windows 11 64-bit

\- Python 3.13.6

\- NVIDIA GeForce RTX 5060 Laptop GPU 8GB

\- PyTorch 2.14.0 + CUDA 13.2

\- Demucs 4.1.0

\- Model: htdemucs



\## Setup



Create a virtual environment:



```powershell

py -3.13 -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install the tested dependencies:



```powershell

python -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu132

```



Verify that PyTorch can use the NVIDIA GPU:



```powershell

python -c "import torch; print(torch.cuda.is\_available()); print(torch.cuda.get\_device\_name(0))"

```



Expected result includes:



```text

True

NVIDIA GeForce RTX 5060 Laptop GPU

```



\## Run



Activate the virtual environment first.



Then run:



```powershell

python peelody.py "<audio\_file>"

```



Example:



```powershell

python peelody.py ".\\samples\\example.wav"

```



Peelody V1 supports:



\- `.wav`

\- `.mp3`



\## Output



Results are stored under:



```text

outputs\\<job\_name>\\htdemucs\\<input\_name>\\

```



The four output tracks are:



```text

bass.wav

drums.wav

other.wav

vocals.wav

```



\## Notes



The htdemucs model files are downloaded automatically when the model is used for the first time.



Separation quality depends on the input audio.



Known observations from current testing are recorded in `TEST\_RECORD.md`.



Test audio and generated output files are not included in the Git repository.

