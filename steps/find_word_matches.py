#-*- coding: utf-8 -*- 
########################################################################
#find_word_matches.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 27th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 find_word_matches.py <paths_to_scripts> <paths_to_asr_trans> <matches_output_dir>

#Description:

#This program find the word matches between the ASR transcriptions
#and the clean scripts. As an outcome,, this program produces
#CSV files with two columns: The first column have words of the
#script and the second column contains words of the ASR transcription

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import os

from utils.match_finder import match_finder

########################################################################
#Imput Parameters

FILE_SCRIPT_PATHS=sys.argv[1]
FILE_ASR_PATHS=sys.argv[2]
DIR_MATCHES_OUT=sys.argv[3]
DATA_PATHS=sys.argv[4]

########################################################################
#Load the paths of the clean scripts in memory
file_script_paths=open(FILE_SCRIPT_PATHS,'r')
HASH_SCRIPT_PATHS={}
for line in file_script_paths:
	line = line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	script_path=list_line[-1]
	HASH_SCRIPT_PATHS[fileID]=script_path
#ENDFOR
file_script_paths.close()
########################################################################
#Load the paths of the ASR Transcriptions in memory
file_asr_paths=open(FILE_ASR_PATHS,'r')
HASH_ASR_PATHS={}
for line in file_asr_paths:
	line = line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	asr_path=list_line[-1]
	HASH_ASR_PATHS[fileID]=asr_path
#ENDFOR
file_asr_paths.close()
########################################################################
#Create an output dir for the paths files
DIR_WORD_MATCHES_PATHS=os.path.join(DATA_PATHS,"word_matches_paths")
if not os.path.exists(DIR_WORD_MATCHES_PATHS):
	os.mkdir(DIR_WORD_MATCHES_PATHS)
#ENDIF
########################################################################
#Find the word matches
for file_id in HASH_SCRIPT_PATHS:
	script_path=HASH_SCRIPT_PATHS[file_id]
	asr_path=HASH_ASR_PATHS[file_id]
	match_dir=os.path.join(DIR_MATCHES_OUT,file_id)
	#Find the matches
	print("Finding Word Matches for: "+asr_path)
	HASH_TM_PATHS=match_finder(script_path,asr_path,match_dir)
	#--------------------------------------------------------------#
	#Register the TMs paths into a paths file
	#--------------------------------------------------------------#
	#Create the output paths file
	paths_file_name=os.path.join(DIR_WORD_MATCHES_PATHS,file_id+"_TMs.paths")
	paths_file_path=open(paths_file_name,'w')	
	for fileID in HASH_TM_PATHS:
		current_path=HASH_TM_PATHS[fileID]
		line_out=fileID+" "+current_path
		paths_file_path.write(line_out+"\n")
	#ENDFOR
	paths_file_path.close()
#ENDFOR
########################################################################

