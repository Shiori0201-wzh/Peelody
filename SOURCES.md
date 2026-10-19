# Peelody V1.1 — Sources and License Notes

This document records the third-party software, pretrained models, test datasets, and generated audio associated with Peelody.

The license for Peelody's source code does not automatically apply to third-party software, pretrained model weights, test audio, or user-provided recordings.

## 1. Peelody Source Code

- **Repository:** https://github.com/Shiori0201-wzh/Peelody
- **License:** MIT License
- **License file:** `LICENSE`
- **Purpose:** Local four-stem music source separation using Demucs.

The MIT license applies to Peelody's source code as identified by the repository license. It does not grant additional rights to third-party model weights or audio datasets.

## 2. Demucs Software

- **Package:** `demucs`
- **Version recorded in the tested environment:** `4.1.0`
- **Official repository:** https://github.com/adefossez/demucs
- **Package index:** https://pypi.org/project/demucs/
- **License recorded by the project:** MIT License
- **Purpose:** Pretrained music source separation and generation of the four output stems.

The Demucs source repository contains its own license file. Refer to the license distributed with the version actually installed when redistributing or packaging the software.

## 3. Pretrained Model Weights

Peelody V1.1 supports two pretrained model identifiers in the GUI:

- `htdemucs` — standard model, selected by default.
- `htdemucs_ft` — optional fine-tuned model.

The model weights are loaded through Demucs and are not included in the Peelody source repository.

### 3.1 HTDemucs

- **Model identifier:** `htdemucs`
- **Previously recorded model source:** https://huggingface.co/adefossez/HTDemucs
- **Previously recorded weight filename:** `955717e8.safetensors`
- **Purpose:** Default four-stem separation model.
- **License status:** The project's previous review did not establish a clearly specified license for the recorded pretrained weights.

The filename above is retained from the project's development notes. The exact cached artifact and its source should be verified against the installed Demucs version before making redistribution claims.

Do not assume that the MIT license for Demucs software automatically applies to the pretrained weights.

### 3.2 HTDemucs Fine-Tuned

- **Model identifier:** `htdemucs_ft`
- **Upstream model configuration:** https://github.com/adefossez/demucs/blob/main/demucs/remote/htdemucs_ft.yaml
- **Purpose:** Optional fine-tuned model for comparative source separation.
- **License status:** The applicable terms for the exact pretrained artifacts used by the installed environment have not been independently established in this project record.

The upstream Demucs configuration describes the model using multiple component checkpoints. The exact artifacts fetched and cached by the installed Demucs version should be verified locally before recording definitive filenames or redistributing weights.

The fine-tuned model is available through the GUI as an alternative to `htdemucs`. It is not assumed to be universally superior.

### 3.3 Model Download and Redistribution

Demucs may download pretrained weights when a model is used for the first time. Subsequent runs may reuse locally cached files.

Peelody does not bundle pretrained weights in the Git repository.

Before redistributing model weights, packaging them with an application, or using them in a commercial release, verify the current terms associated with the exact model artifacts and their source.

## 4. PyTorch

- **Package:** `torch`
- **Version recorded in the tested environment:** `2.14.0+cu132`
- **Official website:** https://pytorch.org/
- **Source repository:** https://github.com/pytorch/pytorch
- **Main project license recorded:** BSD 3-Clause
- **Purpose:** Tensor computation, model execution, and GPU acceleration.

PyTorch distributions may include third-party components with separate licenses. Consult the notices and licensing information associated with the distribution used.

## 5. MUSDB18 / SiSEC18-MUS Test Excerpts

- **Dataset used:** `MUSDB18-7-WAV`
- **Dataset reference:** https://doi.org/10.5281/zenodo.3270814
- **Original dataset:** MUSDB18
- **Purpose:** Local educational evaluation using mixtures and corresponding reference stems.
- **Usage recorded by the project:** Local educational testing.

The two excerpts used in the V1.1 model comparison were:

- Al James - Schoolboy Facination
- AM Contra - Heart Peripheral

The excerpts were used to compare subjective listening results and calculate exploratory SI-SDR measurements.

The test audio is not included in the Peelody Git repository.

The project follows the restriction recorded in its original source notes: MUSDB18 material should not be used commercially without express permission from the relevant copyright holders. Verify the dataset's current terms before any additional use or redistribution.

## 6. User-Provided Audio and Generated Stems

Peelody generates separated audio from user-provided input recordings.

Creating separated stems does not automatically grant independent rights to the underlying recording, composition, performance, or other protected material.

Users are responsible for ensuring they have the necessary rights and permissions for the audio they process and for any use or distribution of the resulting stems.

Generated output audio is not included in the Git repository.

## 7. Release and Compliance Checklist

Before distributing Peelody, bundling model weights, publishing datasets, or using the application commercially, review the current terms for:

- [ ] Peelody source code and the repository MIT license.
- [ ] The installed Demucs package and its accompanying license.
- [ ] The exact `htdemucs` pretrained weight artifacts.
- [ ] The exact `htdemucs_ft` pretrained weight artifacts.
- [ ] PyTorch and its bundled third-party components.
- [ ] MUSDB18 / SiSEC18-MUS test material.
- [ ] Any user-provided audio included in examples or demonstrations.
- [ ] Any generated stems proposed for redistribution.

A software package license must not be treated as proof that all model weights and datasets can be redistributed under the same terms.

## 8. Related Project Documentation

- [README.md](README.md) — installation, CLI, GUI, and usage instructions.
- [TEST_RECORD.md](TEST_RECORD.md) — functional and regression test history.
- [V11_MODEL_EVALUATION.md](V11_MODEL_EVALUATION.md) — model comparisons, SI-SDR results, runtime observations, and evaluation limitations.
- [LICENSE](LICENSE) — license for Peelody source code.
