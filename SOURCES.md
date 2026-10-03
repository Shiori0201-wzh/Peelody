\# Peelody V1 Sources and License Notes



\## 1. Demucs



\- Version: 4.1.0

\- Source: Official Demucs package on PyPI

\- Author/Maintainer: Alexandre Défossez

\- Purpose in Peelody: Local music source separation

\- License: MIT License

\- Note: This license information applies to the Demucs software package.



\## 2. HTDemucs Model Weights



\- Model: htdemucs

\- Source: adefossez/HTDemucs on Hugging Face

\- Weight file used by the current model: 955717e8.safetensors

\- Purpose in Peelody: Pretrained source-separation model

\- License: Not clearly specified on the current model card

\- Current use: Local learning and testing

\- Restriction: Do not assume that the Demucs MIT software license automatically applies to the pretrained model weights.

\- Before redistributing the model weights or using them in another release scenario, re-check the model's current license and terms.



\## 3. PyTorch



\- Version tested: 2.14.0+cu132

\- Source: Official PyTorch project / official PyTorch CUDA wheel index

\- Purpose in Peelody: GPU tensor computation and model execution

\- Main project license: BSD 3-Clause

\- Note: PyTorch distributions also contain third-party components with their own licenses.



\## 4. MUSDB18 / SiSEC18-MUS 7s Excerpts



\- Dataset used: MUSDB18-7-WAV

\- Source: SiSEC18-MUS 7s Excerpts, Zenodo

\- DOI: 10.5281/zenodo.3270814

\- Original dataset: MUSDB18

\- Purpose in Peelody: Fixed source-separation test material with Ground Truth stems

\- Current use: Local educational testing

\- Important restriction: MUSDB18 is provided for educational purposes and should not be used commercially without express permission from the relevant copyright holders.

\- Test audio is not included in the Peelody Git repository.



\## 5. Peelody Output Audio



\- Separated tracks are generated from user-provided input audio.

\- Creating separated stems does not automatically grant new rights to the underlying recording, composition, performance, or other protected material.

\- Peelody does not include test audio or generated output audio in the Git repository.



\## 6. Release Note



Before publishing Peelody source code, distributing model files, bundling datasets, or using the project commercially, re-check the current licenses and terms for:



\- Demucs

\- HTDemucs pretrained weights

\- PyTorch and bundled third-party components

\- Any test or user-provided audio

