#!/usr/bin/env bash
#--------------------------------------------------------------------#
# MAFIA (Match-Finder Aligner)
#--------------------------------------------------------------------#
set -eo pipefail

this_script="mafia.sh"
echo " "
echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo "INFO ($this_script): MAFIA (Match-Finder Aligner)"
date
echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo " "

#
# Check necessary variables
#
if [ -z "$KENLM_ROOT" ]; then
    echo "ERROR ($this_script): KENLM_ROOT is not set"
    exit 1
fi

if [ -z "$INPUT_DATA" ]; then
    echo "ERROR ($this_script): INPUT_DATA is not set. Please set the path to the audio recording directory."
    exit 1
fi

if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
    CUDA_VISIBLE_DEVICES="0"
    echo "No CUDA_VISIBLE_DEVICES set, using default: $CUDA_VISIBLE_DEVICES"
fi


#--------------------------------------------------------------------#
#System Paths
#--------------------------------------------------------------------#

STEPS="steps"
MODELS="models"
DATA="data"
PATHS="paths"
SEGMENTS="segments"

#--------------------------------------------------------------------#
#CONTROL PANEL
#--------------------------------------------------------------------#

CUDA_DEVICE_ORDER="PCI_BUS_ID"

nj_decode=16

from_stage=0
to_stage=8

#--------------------------------------------------------------------#
#Setting up important paths and variables
#--------------------------------------------------------------------#

NEMO_MODEL=$MODELS/QuartzNet15x1SEP-IS.nemo
LANGUAGE_MODEL=$MODELS/3GRAM_ARPA_MODEL.lm

#--------------------------------------------------------------------#
#Exit immediately in case of error.

#--------------------------------------------------------------------#
#Create data directory
#--------------------------------------------------------------------#
current_stage=0
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Create data directory"
    echo "-----------------------------------"
    
    mkdir -p "paths"
    python3 $STEPS/find_data_paths.py $INPUT_DATA $PATHS
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Text Pre-Processing
#--------------------------------------------------------------------#
current_stage=1
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Text Pre-Processing"
    echo "-----------------------------------"
    
    mkdir -p $DATA
    mkdir -p $DATA/clean_scripts
    python3 $STEPS/clean_text.py $PATHS/original_scripts.paths $DATA/clean_scripts
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Segment-Timestamps
#--------------------------------------------------------------------#
current_stage=2
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Segment-Timestamps"
    echo "-----------------------------------"
    
    mkdir -p $DATA/segments_csvs
    python3 $STEPS/create_segment_csvs.py $PATHS/original_audio.paths $DATA/segments_csvs
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Segment the Audio
#--------------------------------------------------------------------#
current_stage=3
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Segment the Audio"
    echo "-----------------------------------"
    
    mkdir -p $SEGMENTS
    python3 $STEPS/segment_audio.py $PATHS/original_audio.paths $PATHS/segments_csvs.paths $SEGMENTS
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Create Language Model
#--------------------------------------------------------------------#
current_stage=4
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Create Language Model"
    echo "-----------------------------------"
    
    python3 $STEPS/create_lm.py $PATHS/clean_scripts.paths $DATA $LANGUAGE_MODEL
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Transcribe the Segments
#--------------------------------------------------------------------#
current_stage=5
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Transcribe the Segments"
    echo "-----------------------------------"

    mkdir -p $DATA/asr_transcriptions
    mkdir -p $DATA/asr_logits
    python3 $STEPS/transcribe_segments.py $nj_decode $PATHS/segments_paths $NEMO_MODEL $LANGUAGE_MODEL $DATA/asr_transcriptions $DATA/asr_logits $PATHS
    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Find Word Matches
#--------------------------------------------------------------------#
current_stage=6
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Find Word Matches"
    echo "-----------------------------------"

    mkdir -p $DATA/word_matches
    python3 $STEPS/find_word_matches.py $PATHS/clean_scripts.paths $PATHS/asr_transcriptions.paths $DATA/word_matches $PATHS

    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#DTW Aligment
#--------------------------------------------------------------------#
current_stage=7
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: DTW Aligment"
    echo "-----------------------------------"

    mkdir -p $DATA/final_transcriptions
    python3 $STEPS/dtw_aligment.py $PATHS/word_matches_paths $PATHS/asr_transcriptions.paths $PATHS/final_transcriptions.paths $DATA/final_transcriptions

    
    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
#Generate Results File
#--------------------------------------------------------------------#
current_stage=8
if  [ $current_stage -ge $from_stage ] && [ $current_stage -le $to_stage ]; then
    echo "-----------------------------------"
    echo "Stage $current_stage: Generate Results File"
    echo "-----------------------------------"

    python3 $STEPS/generate_results_file.py $PATHS/final_transcriptions.paths

    echo " "
    echo "INFO ($this_script): Stage $current_stage Done!"
    echo " "
fi

#--------------------------------------------------------------------#
echo " "
echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo "INFO ($this_script): All Stages Done Successfully!"
date
echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo " "
#--------------------------------------------------------------------#

