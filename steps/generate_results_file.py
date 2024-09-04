#-*- coding: utf-8 -*- 
########################################################################
#generate_results_file.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 29th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 generate_results_file.py

#Description:

#This script generate a CSV file with the results obtained by the
#MAFIA aligner.

#Notice: This program is intended for Python 3
########################################################################
#Imports
import sys
import os

########################################################################
#Input Parameters
FILE_FTRANS_PATHS=sys.argv[1]
########################################################################
#Open the Results file
file_results=open("RESULTS.csv","w")
print("Creating the Results File: RESULTS.csv")
########################################################################
#Iterate over the ftrans paths

#Open the file of final transcriptions
file_ftrans_paths=open(FILE_FTRANS_PATHS,'r')


#Write the header of the CSV Results file
header="podcast_id,segment_id,sentence_norm"
file_results.write(header+"\n")

for line in file_ftrans_paths:
	line=line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	ftrans_path=list_line[-1]
	#--------------------------------------------------------------#
	#Open the current ftrans file
	#--------------------------------------------------------------#
	ftrans_file=open(ftrans_path,'r')
	
	for linea in ftrans_file:
		linea=linea.replace("\n","")
		lista_linea=linea.split(" ")
		segment_id=lista_linea[0]
		lista_linea.pop(0)
		ftrans=" ".join(lista_linea)
		list_out=[fileID,segment_id,ftrans]
		line_out=",".join(list_out)
		file_results.write(line_out+"\n")
	#ENDFOR
	#--------------------------------------------------------------#
	#Close the current ftrans file
	#--------------------------------------------------------------#
	ftrans_file.close()
#ENDFOR
file_ftrans_paths.close()

########################################################################
#Close the Results file
file_results.close()
########################################################################

