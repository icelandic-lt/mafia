# MAFIA (Match-Finder Aligner)

![Version](https://img.shields.io/badge/master-darkgreen)
![Python3](https://img.shields.io/badge/python-blue?logo=python&logoColor=white)
![CI Status](https://img.shields.io/badge/Build-[unavailable]-red)
![Docker](https://img.shields.io/badge/Docker-[unavailable]-red)

MAFIA is the acronym for Match-Finder Aligner. The MAFIA aligner is a software tool to automatically create an ASR corpus out of speech recordings accompanied by prompts corresponding to the spoken words. If the text of the prompts and the recorded words do not completely match, MAFIA will infer a transcription using automatic speech recognition.

## Overview

This repository has been created by the [Language and Voice Lab](https://lvl.ru.is/) at Reykjavík University and is part of the [Icelandic Language Technology Programme](https://github.com/icelandic-lt/icelandic-lt).

- **Category:** [ASR](https://github.com/icelandic-lt/icelandic-lt/blob/main/doc/asr.md)
- **Domain:** Server
- **Languages/Frameworks:** Python, Conda, PyTorch, NeMo, KenLM
- **Language Version/Dialect:**
    - Python: 3.7
- **Audience**: Developers, Researchers
- **Origin:** [Mafia](http://hdl.handle.net/20.500.12537/215)

## Status
![Experimental](https://img.shields.io/badge/Experimental-darkviolet)

This project has a lot of 3rdparty dependencies that you need to get compiled and installed on your system. Also make sure to have CMake version > `3.18` installed to successfully compile all dependencies. You can alternatively use Nvidia NeMo Docker containers for running this code to have less hassle for installation.<br>
Because some parts of the project use unmaintained 3rdparty projects like e.g. [OpenSeq2Seq](https://github.com/NVIDIA/OpenSeq2Seq), you need to use older dependencies to be compatible. This could be resolved in compiling the dependency [ctc_decoder](https://github.com/NVIDIA/OpenSeq2Seq/tree/master/decoders) oneself (e.g. use some alternative projects like [here](https://github.com/Slyne/ctc_decoder) and [here](https://github.com/parlance/ctcdecode)) or use the [PyTorch version](https://pytorch.org/audio/main/generated/torchaudio.models.decoder.ctc_decoder.html). But this is not implemented in this project.

## System Requirements
- Operating System: Linux
- Training: GPU with at least 8GB of memory

## Prerequisites

Install Conda according to the instructions at https://docs.conda.io/projects/conda/en/latest/user-guide/install/.

To install CMake on your system, follow the instructions at https://cmake.org/install/.

Please also make sure, you have the following system packages installed in your system:

- sox
- libsndfile1
- ffmpeg

For KenLM, we need to install the following packages:

- libboost-system-dev
- libboost-thread-dev 
- ibboost-program-options-dev
- libboost-test-dev
- libeigen3-dev
- zlib1g-dev
- libbz2-dev
- liblzma-dev

### Input data + format

The speech files have to be in the format RIFF/WAV at 16khz sample rate, 16bit, mono. It is expected that scripts and speech files share a common root directory. Both have to have the same name but different extensions: .txt for the scripts and .wav for the speech files. There can be any number of pairs of "script/speech files" as needed.

You can use the script [dl_dataset.py](dl_dataset.py) to download datasets from Huggingface. By default, the `raddromur` dataset is downloaded and files are extracted to your local directory `data_raddromur/`.

## Installation

#### Install KenLM
```bash
git clone --recursive https://github.com/kpu/kenlm.git && pushd kenlm
mkdir -p build && cd build
cmake ..
make -j 4
export KENLM_ROOT=`pwd`/bin
popd
```
#### NeMo

The following installation follows in most parts the official installation instructions for the NeMo toolkit. You can find the most recent installation instructions on [GitHub](https://github.com/NVIDIA/NeMo#install-nemo-framework).

#### Create a new Conda environment
```bash
conda create -n nemo_r150 python=3.7 anaconda
conda activate nemo_r150
```

#### Install Pytorch
```bash
conda install pytorch torchvision torchaudio cudatoolkit -c pytorch
pip install wget
pip install unidecode
```

#### Install Nvidia Apex
```bash
git clone https://github.com/NVIDIA/apex
pushd apex
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
popd
```
#### CMake
If your existing CMake version is lower than 3.18, you will need to update it. E.g., on Ubuntu since 20.04, you can use the following commands:

```bash
sudo apt remove --purge cmake
hash -r
sudo snap install cmake --classic
```
This uses the snap package manager to install the latest version of CMake. This step is necessary because in one of the above steps, CMake is reinstalled again. If you have already preinstalled CMake via snap beforehand, it might just be necessary to execute the following steps:

```bash
sudo apt remove --purge cmake
hash -r
```

#### Install NeMo
```bash
pip install git+https://github.com/NVIDIA/NeMo.git@r1.5.0#egg=nemo_toolkit[all]
git clone https://github.com/NVIDIA/NeMo.git
pushd NeMo/scripts/asr_language_modeling/ngram_lm
bash install_beamsearch_decoders.sh `pwd`/../../../..
popd
```

#### Test your NeMo installation
```bash
python
import nemo
import nemo.collections.asr as nemo_asr
```

If you get an error similar like this:
```
AttributeError: module 'numpy' has no attribute 'long'
```
This is due to a NumPy version incompatibility for NumPy `1.24.0` and above. Try to downgrade NumPy via the following command:
```bash
pip install numpy==1.23.0
```

#### Install inaSpeechSegmenter + jiwer
```bash
$ pip install inaSpeechSegmenter
$ pip install jiwer
```

#### NeMo Docker

You can alternatively use one of the prebuilt NeMo Docker containers available from Nvidia NGC, e.g.:

```bash
docker run --gpus all -it -v ./:/mafia --shm-size=8g -p 8888:8888 -p 6006:6006 \
  --ulimit memlock=-1 --ulimit stack=67108864 --device=/dev/snd nvcr.io/nvidia/nemo:24.05
```

These are big, but have all NeMo dependencies with appropriate versions installed and might be an easier jumpstart.
You need though to install some of the above dependencies inside the docker container as well:

```bash
apt-get update && apt install libboost-all-dev    # for KenLM
pip install unidecode inaSpeechSegmenter jiwer
cd /mafia
pushd kenlm/build/
cmake ..
make clean
make -j 4
popd
pushd NeMo/scripts/asr_language_modeling/ngram_lm
bash install_beamsearch_decoders.sh `pwd`/../../../..
popd
```
Please mind off that the last step needs Python 3.7 and therefore is not supported inside the NeMo containers. You have to find an alternative way to install the ctc_decoder dependency, e.g. via an alternative route outlined above.

## Running MAFIA

After following the above installation steps, set the following environment variables:
- `INPUT_DATA` for the path to the speech input data
- `KENLM_ROOT` for the path to the binary directory of KENLM, e.g. `\`pwd\`/kenlm/build/bin`
- `CUDA_VISIBLE_DEVICES` for the GPU ids you want to use in your system

Then run the script via:

```bash
bash mafia.h
```
Note that executing the script might need a very long time depending on the size of your dataset. It's therefore a good idea to first start testing with a small dataset. 

## Models

The Icelandic ASR model `models/QuartzNet15x1SEP.nemo` has been created via the NeMo recipe of the [samromur-asr](https://github.com/icelandic-lt/samromur-asr) project. MAFIA also uses [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter) to split the audio signal into homogeneous zones of speech, music and noise. Furthermore, a [KenLM](https://github.com/kpu/kenlm) 3gram language model is generated from the text prompts of the dataset.

## ACKNOWLEDGEMENTS

This project was funded by the Language Technology Programme for Icelandic 2019-2023. The programme, which is managed and coordinated by [Almannarómur](https://almannaromur.is/), is funded by the Icelandic Ministry of Education, Science and Culture.
