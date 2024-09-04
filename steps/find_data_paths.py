#-*- coding: utf-8 -*- 
########################################################################
#template_ENG_python3.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 24th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 find_data_paths.py <podcasts_folder>


#Description:

#This script generates lists with paths to the input data.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import os

########################################################################
#Input parameters

CORPUS_IN_DIR=sys.argv[1]
DATA_PATHS=sys.argv[2]

########################################################################

HASH_TEXT={}
HASH_WAVS={}
LIST_FILEIDS=[]

for root, dirs, files in os.walk(CORPUS_IN_DIR):
	for filename in files:
		path_to_file=os.path.join(root,filename)
		name=os.path.basename(path_to_file)
		if name.endswith(".txt"):
			fileID=name.replace(".txt","")
			HASH_TEXT[fileID]=path_to_file
		elif name.endswith(".wav"):
			fileID=name.replace(".wav","")
			HASH_WAVS[fileID]=path_to_file
			LIST_FILEIDS.append(fileID)
		#ENDIF
	#ENDFOR
#ENDFOR
LIST_FILEIDS.sort()

########################################################################
#Create output files.

file_txt=open(os.path.join(DATA_PATHS,"original_scripts.paths"),'w')
file_wav=open(os.path.join(DATA_PATHS,"original_audio.paths"),'w')

########################################################################
#Print output files

for fileID in LIST_FILEIDS:
	if (fileID in HASH_TEXT) and (fileID in HASH_WAVS):
		text_file=HASH_TEXT[fileID]
		line_out=fileID+" "+text_file
		file_txt.write(line_out+"\n")
		
		wav_file=HASH_WAVS[fileID]
		line_out=fileID+" "+wav_file
		file_wav.write(line_out+"\n")
	#ENDIF
#ENDFOR

########################################################################
#Close the opened files
file_txt.close()
file_wav.close()

