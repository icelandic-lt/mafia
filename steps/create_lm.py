#-*- coding: utf-8 -*- 
########################################################################
#create_lm.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 28th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 create_lm.py 

#Description:

#This script gathers the text of all the clean scripts and
#use it to create a trigram language model.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
#import re
import os

########################################################################
#Input Parameters

FILE_SCRIPTS_PATHS=sys.argv[1]
DATA_DIR=sys.argv[2]
LM_PATH=sys.argv[3]

########################################################################
#Create a file to store the text

text_file_path=os.path.join(DATA_DIR,"Text_for_LM.txt")
file_whole_text=open(text_file_path,'w')

########################################################################
#Join the text of all the scripts
file_scripts_paths=open(FILE_SCRIPTS_PATHS,'r')

for line in file_scripts_paths:
	#Get the script path
	line=line.replace("\n","")
	list_line=line.split(" ")
	script_path=list_line[-1]
	#Open the script file
	file_script=open(script_path,'r')
	#Put the text in a single file
	for line in file_script:
		file_whole_text.write(line)
	#ENDFOR
#ENDFOR

file_scripts_paths.close()
file_whole_text.close()

########################################################################
#Create the language model usin SRILM
#lm_path=os.path.join(DIR_LM_OUT,"3GRAM_MODEL.lm")
command_srilm="ngram-count -order 3 -unk -kndiscount -interpolate -text "+text_file_path+" -lm "+LM_PATH
print(command_srilm)
os.system(command_srilm)

########################################################################

