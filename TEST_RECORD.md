\# Peelody V1 Test Record



\## 1. Environment



\- OS: Windows 11 64-bit

\- Python: 3.13.6

\- GPU: NVIDIA GeForce RTX 5060 Laptop GPU 8GB

\- PyTorch: 2.14.0+cu132

\- Demucs: 4.1.0

\- Model: htdemucs



\## 2. Standard WAV Sample



Sample:



`MUSDB18-7-WAV/test/Al James - Schoolboy Facination/mixture.wav`



Input properties:



\- Channels: 2

\- Sample rate: 44100 Hz

\- Sample width: 2 bytes

\- Frames: 308700

\- Duration: 7.0 s



Ground Truth tracks:



\- vocals.wav

\- drums.wav

\- bass.wav

\- other.wav



Result:



\- Four tracks generated successfully.

\- vocals: close to Ground Truth, no obvious accompaniment leakage.

\- bass: no obvious problem.

\- drums: main sound is close, but Ground Truth sounds richer.

\- other: noticeably different, with a somewhat discontinuous / stuttering sound.



\## 3. MP3 Test



Input:



`mp3\_test.mp3`



Result:



\- MP3 input accepted successfully.

\- Four WAV tracks generated successfully.

\- All four output tracks:

&#x20; - Channels: 2

&#x20; - Sample rate: 44100 Hz

&#x20; - Duration: about 158.119 s



\## 4. Error Tests



\- No argument -> PASS: usage message shown.

\- Missing file -> PASS: input file does not exist.

\- Unsupported extension -> PASS: only WAV and MP3 accepted.

\- Broken WAV -> PASS: separation failure detected.

\- Broken WAV does not incorrectly print "Separation finished.".

\- Demucs internal traceback is hidden from normal user output.



\## 5. Output Management



\- Outputs are stored under the Peelody project directory.

\- Running Peelody from another working directory does not change the output root.

\- Two different files named `mixture.wav` no longer overwrite each other.

\- Different inputs receive separate job directories.



\## 6. Current Known Limitations



\- Separation quality varies between stems.

\- `other.wav` showed the most obvious artifact in the standard sample.

\- Current quality observations are based mainly on listening and file properties.

\- No formal objective separation metric has been calculated yet.

