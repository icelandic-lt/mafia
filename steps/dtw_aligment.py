#-*- coding: utf-8 -*- 
########################################################################
#dtw_aligment.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 28th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 dtw_aligment.py 

#Description:

#This program performs DTW aligment using the TM files generated
#in a previous step.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import os

from utils.matrix_handler import create_empty_vector
from utils.matrix_handler import create_matching_matrix
from utils.matrix_handler import define_search_area
from utils.matrix_handler import search_in_area
from utils.matrix_handler import find_gaps
from utils.matrix_handler import fill_the_gaps
from utils.matrix_handler import fill_leftovers

########################################################################
#Input Parameters

DIR_WORD_MATCHES_PATHS=sys.argv[1]
FILE_DEC_TRANS_PATHS=sys.argv[2]
FILE_FINAL_TRANS_PATHS=sys.argv[3]
DIR_FINAL_TRANS=sys.argv[4]

########################################################################
#Load in memory the transcriptions decoded by the ASR system
#At the same time, create a hash for the paths of the final 
#transcriptions.

file_dec_trans_paths=open(FILE_DEC_TRANS_PATHS,'r')

HASH_DEC_TRANS={}
HASH_FTRANS_FILES={}

for line in file_dec_trans_paths:
	#Get the paths and the fileIDs
	line=line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	dec_file_path=list_line[-1]	
	#Put the final trans path in the hash.
	path_ftrans_file=os.path.join(DIR_FINAL_TRANS,fileID+".ftrans")
	HASH_FTRANS_FILES[fileID]=path_ftrans_file
	#Put the Dec transcriptions in the hash
	current_dec_file=open(dec_file_path,'r')	
	for linea in current_dec_file:
		linea=linea.replace("\n","")
		lista_linea=linea.split(" ")
		clave=lista_linea[0]
		lista_linea.pop(0)
		trans=" ".join(lista_linea)
		HASH_DEC_TRANS[clave]=trans
	#ENDFOR
	current_dec_file.close()
#ENDFOR
#Close the file
file_dec_trans_paths.close()

########################################################################
#Put the paths of the TM files in a list

LIST_TMS_PATHS=[]

for root, dirs, files in os.walk(DIR_WORD_MATCHES_PATHS):
	for filename in files:
		path_to_file=os.path.join(root,filename)
		LIST_TMS_PATHS.append(path_to_file)
	#ENDFOR
#ENDFOR

########################################################################
#Iterate over the TM files

#Create the ftrans-paths file
trans_final_path=open(FILE_FINAL_TRANS_PATHS,'w')
LIST_TMS_PATHS.sort()
for tms_path in LIST_TMS_PATHS:
	#Open the current TM file
	tm_file=open(tms_path,'r')
	#Get the fileID
	fileID=os.path.basename(tms_path)
	fileID=fileID.replace("_TMs.paths","")
	#Create the ftrans file
	ftrans_path=HASH_FTRANS_FILES[fileID]
	trans_final_file=open(ftrans_path,'w')
	#Iterate over the TMs files
	HASH_RESULTS={}
	for line in tm_file:
		line=line.replace("\n","")
		list_line=line.split(" ")
		segment_key=list_line[0]
		path_TMs=list_line[-1]
		#------------------------------------------------------#
		#Load the TM file in memory
		#------------------------------------------------------#
		#Open the current TM file
		file_current_tms=open(path_TMs,'r')
		#------------------------------------------------------#
		#The TM file contains the words of the script (LISTA_REF)
		#and the transcription produced by the ASR system (LISTA_ASR)
		LISTA_REF=[]
		LISTA_ASR=[]
		#Read the lines of the TM file
		for linea in file_current_tms:
			linea=linea.replace("\n","")
			lista_linea=linea.split(",")
			word_ref=lista_linea[0]
			LISTA_REF.append(word_ref)
			word_asr=lista_linea[-1]
			if word_asr!=".":
				LISTA_ASR.append(word_asr)
			#ENDIF
		#ENDFOR
		#------------------------------------------------------#
		file_current_tms.close()
		#------------------------------------------------------#
		#Here we have to determine if the transcription in 
		#LISTA_ASR is the same as the one in HASH_DEC_TRANS.
		#In case negative, the final transcription will be 
		#taken from the HASH_DEC_TRANS.
		trans_from_lista=" ".join(LISTA_ASR)
		trans_from_hash=HASH_DEC_TRANS[segment_key]

		if trans_from_lista!=trans_from_hash:
			HASH_RESULTS[segment_key]=trans_from_hash
		else:
			#----------------------------------------------#
			#Valid conditions to perfom DTW 
			#----------------------------------------------#
			#The LISTA_REF has to be larger than the LISTA_ASR
			diference=len(LISTA_REF)-len(LISTA_ASR)
			if diference<2:
				LISTA_REF.insert(0,"@")
				LISTA_REF.append("@")
			#ENDIF
			#----------------------------------------------#
			#Get the fileID of the current TM File
			#----------------------------------------------#
			#tm_fileID=os.path.basename(path_TMs)
			#tm_fileID=tm_fileID.replace("_TMs.csv","")
			#----------------------------------------------#
			#Create a list (vector) with the result of the DTW process.
			#----------------------------------------------#
			LISTA_RES=create_empty_vector(LISTA_ASR)
			#----------------------------------------------#
			#Create the Matrix for the DTW	
			#----------------------------------------------#
			matriz=create_matching_matrix(LISTA_REF,LISTA_ASR)
			#----------------------------------------------#
			#Determine the searching area for this matrix
			hash_search_area=define_search_area(matriz)
			#----------------------------------------------#
			#The main algorithm starts here
			#----------------------------------------------#
			#1. Search in the search area only
			LISTA_RES=search_in_area(matriz, hash_search_area, LISTA_RES,LISTA_ASR)
			#----------------------------------------------#
			#2.1 Find the gaps of only 1 element.
			LISTA_GAPS=find_gaps(matriz)
			#----------------------------------------------#
			#2.2 Fill the gaps
			LISTA_RES=fill_the_gaps(LISTA_GAPS,LISTA_RES,LISTA_REF,LISTA_ASR)
			#----------------------------------------------#
			#3. Fill the remaining gaps
			LISTA_RES=fill_leftovers(LISTA_RES,LISTA_ASR)
			#LISTA_RES.insert(0,tm_fileID)
			#----------------------------------------------#
			#Create the final transcription
			#----------------------------------------------#
			final_trans=" ".join(LISTA_RES)
			#----------------------------------------------#
			#Put the final transcription in the hash	
			HASH_RESULTS[segment_key]=final_trans			
			#----------------------------------------------#
		#ENDIF
	#ENDFOR
	#--------------------------------------------------------------#
	#Write the final transcriptions in an output file.
	#--------------------------------------------------------------#
	list_results=list(HASH_RESULTS.items())
	list_results.sort()
	for key, trans in list_results:
		line_out=key+" "+trans
		trans_final_file.write(line_out+'\n')
	#ENDFOR
	#--------------------------------------------------------------#
	#Register the path of the final transcriptions file
	#--------------------------------------------------------------#
	line_out=fileID+" "+ftrans_path
	trans_final_path.write(line_out+'\n')
	#--------------------------------------------------------------#
	#Close the opened files
	#--------------------------------------------------------------#
	tm_file.close()
	trans_final_file.close()
#ENDFOR

trans_final_path.close()

########################################################################

