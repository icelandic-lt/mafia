#-*- coding: utf-8 -*- 
########################################################################
#clean_text.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 24th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 clean_text.py <paths_to_original_scripts>

#Description:

#This program cleans the text from the original podacast-scripts.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################
#Input parameters
FILE_ORG_SCRIPT_PATHS=sys.argv[1]
DIR_CLEAN_SCRIPTS=sys.argv[2]

########################################################################
#Function to clean text.
def clean_text(dirty_script_text):
	pattern_brackets=r'\[.*?\]+'
	#--------------------------------------------------------------#
	clean_script_text=dirty_script_text.lower()
	#--------------------------------------------------------------#
	clean_script_text=clean_script_text.replace("\n","#")
	clean_script_text=re.sub("\s+"," ",clean_script_text)
	clean_script_text=re.sub("# +","#",clean_script_text)
	clean_script_text=re.sub("#+","#",clean_script_text)
	clean_script_text=re.sub("# ","#",clean_script_text)
	clean_script_text=re.sub(" #","#",clean_script_text)
	#--------------------------------------------------------------#
	clean_script_text=clean_script_text.replace("–"," ")
	clean_script_text=clean_script_text.replace(":"," ")
	clean_script_text=clean_script_text.replace("-"," ")
	clean_script_text=clean_script_text.replace(","," ")
	clean_script_text=clean_script_text.replace("."," ")
	clean_script_text=clean_script_text.replace("_"," ")
	clean_script_text=clean_script_text.replace("„"," ")
	clean_script_text=clean_script_text.replace("“"," ")
	clean_script_text=clean_script_text.replace("?"," ")
	clean_script_text=clean_script_text.replace("("," ")
	clean_script_text=clean_script_text.replace(")"," ")
	#--------------------------------------------------------------#
	clean_script_text=re.sub(pattern_brackets," ",clean_script_text)
	clean_script_text=re.sub("\s+"," ",clean_script_text)
	clean_script_text=clean_script_text.strip()
	#--------------------------------------------------------------#
	clean_script_text=re.sub("# ","#",clean_script_text)
	clean_script_text=re.sub(" #","#",clean_script_text)
	clean_script_text=clean_script_text.replace("#","\n")
	#--------------------------------------------------------------#	
	return clean_script_text
#ENDDEF

########################################################################
#Create a file to register the paths of the clean scripts
DIR_PATHS=os.path.dirname(FILE_ORG_SCRIPT_PATHS)
CLEAN_SCRIPT_PATHS=os.path.join(DIR_PATHS,"clean_scripts.paths")
file_clean_script_paths=open(CLEAN_SCRIPT_PATHS,'w')

########################################################################
#Open every script file and clean it.
file_org_paths=open(FILE_ORG_SCRIPT_PATHS,'r')
for line in file_org_paths:
	#Get the path to the current script file
	line=line.replace("\n","")
	list_line=line.split(" ")
	dirty_script_path=list_line[-1]
	dirty_script_name=os.path.basename(dirty_script_path)
	#Get a path to the clean script file
	clean_script_path=os.path.join(DIR_CLEAN_SCRIPTS,dirty_script_name)
	#Read the current script file
	file_dirty_script=open(dirty_script_path,'r')
	#Read the text
	dirty_script_text=file_dirty_script.read()
	#Close the file
	file_dirty_script.close()
	#Create a file for the clean script file
	file_clean_script=open(clean_script_path,'w')
	#Clean the text
	print("Cleaning text of: "+dirty_script_name)
	clean_script_text=clean_text(dirty_script_text)
	#Save the path in a file
	fileID=clean_script_path.replace(".txt","")
	fileID=os.path.basename(fileID)
	file_clean_script_paths.write(fileID+" "+clean_script_path+"\n")
	#Write the clean text in the output file
	file_clean_script.write(clean_script_text)
	#Close the file
	file_clean_script.close()
#ENDFOR
file_org_paths.close()
file_clean_script_paths.close()

########################################################################

