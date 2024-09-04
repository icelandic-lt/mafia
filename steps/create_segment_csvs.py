#-*- coding: utf-8 -*- 
########################################################################
#create_segment_csvs.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 25th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 create_segment_csvs.py <audio_paths_file> <output_dir>

#Description:

#This script uses inaSpeechSegmenter to create segments timestamps
#in CSV format.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
#import re
import os

########################################################################
#Imput parameters

AUDIO_PATHS_FILE=sys.argv[1]
CSV_DIR=sys.argv[2]

########################################################################
#Create a file of paths for the CSVs

file_path=os.path.dirname(AUDIO_PATHS_FILE)
file_path=os.path.join(file_path,"segments_csvs.paths")
file_csvs_paths=open(file_path,'w')

########################################################################

file_audio = open(AUDIO_PATHS_FILE,'r')

for line in file_audio:
	line=line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	audio_path=list_line[-1]	
	command="ina_speech_segmenter.py -i "+audio_path+" -e \'csv\' -g false -o "+CSV_DIR
	current_csv_path=os.path.join(CSV_DIR,fileID+".csv")
	line_out=fileID+" "+current_csv_path
	file_csvs_paths.write(line_out+"\n")
	print("Creating CSV file: "+current_csv_path)
	os.system(command)  #******** UNCOMMENT THIS *************#
#ENDFOR

file_audio.close()
file_csvs_paths.close()
########################################################################

