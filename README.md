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
    - Python: 3.7/3.8
- **Audience**: Developers, Researchers
- **Origin:** [Mafia](http://hdl.handle.net/20.500.12537/215)

## Status
![Development](https://img.shields.io/badge/Development-darkviolet)

This project has a lot of 3rdparty dependencies that you need to get compiled and installed on your system. Also make sure to have CMake version > `3.18` installed to successfully compile all dependencies.

## System Requirements
- Operating System: Linux
- Training: GPU with at least 8GB of memory

## Prerequisites

Install Conda according to the instructions at https://docs.conda.io/projects/conda/en/latest/user-guide/install/.

To install CMake on your system, follow the instructions at https://cmake.org/install/. If your existing CMake version is lower than 3.18, you will need to update it. E.g., on Ubuntu since 20.04, you can use the following commands:


```bash
sudo apt remove --purge cmake
hash -r
sudo snap install cmake --classic
```
This uses the snap package manager to install the latest version of CMake.

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

The speech files have to be in the format RIFF/WAV at 16khz sample rate, 16bit, mono. **is this so ? ffmpeg seems to resample the input files **

It is expected that scripts and speech files to share a common root directory. Both have to have the same name but different extension: txt for the scripts and wav for the speech files. There can be any number of pairs of "script/speech files" as needed.


## Installation

#### Install KenLM
```bash
git clone --recursice https://github.com/kpu/kenlm.git && pushd kenlm
mkdir -p build && cd build
cmake ..
make -j 4
export KENLM_ROOT=`pwd`/bin
popd
```

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

#### Install NeMo
```bash
pip install git+https://github.com/NVIDIA/NeMo.git@r1.5.0#egg=nemo_toolkit[all]
git clone https://github.com/NVIDIA/NeMo.git
pushd NeMo/scripts/asr_language_modeling/ngram_lm
bash install_beamsearch_decoders.sh `pwd`/../../../..
popd
```

#### Test your installation
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

## Running MAFIA

After following the above installation steps, set the following environment variables:
- `INPUT_DATA` for the path to the speech input data
- `CUDA_VISIBLE_DEVICES` for the GPU's you want to use for training

Then run the script via:

```bash
sh mafia.h
```

---------------------------------------------------------------------
ACKNOWLEDGEMENTS
---------------------------------------------------------------------

This project was funded by the Language Technology Programme for 
Icelandic 2019-2023. The programme, which is managed and coordinated 
by Almannarómur, is funded by the Icelandic Ministry of Education, 
Science and Culture.

Questions:

- from where stems models/QuartzNet15x1SEP-IS.nemo ? How is this model trained ?
