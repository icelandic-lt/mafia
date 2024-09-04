#-*- coding: utf-8 -*- 
########################################################################
#match_finder.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 18th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 match_finder.py

#Description:

#This functions requires the whole script file and the
#transcriptions produced by the ASR system.

#As an outcome, this function produce the "transcription-matches" files.

#A transcription-matches file is a CSV file with tewo columns. The second
#column contains the words produced by the ASR system when transcribing
#a single audio file. The first column contains a region of the
#original script file with the most chances to match with the words in 
#the second column.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os
from utils.libcrocomad import crocomad_best_match
from utils.csv_handler import lists_to_csv
from utils.csv_handler import lists_to_list
from utils.csv_handler import prune_trans_matches

########################################################################

def match_finder(file_script, file_asr, output_dir):
	#--------------------------------------------------------------#
	def trans_match_to_file(list_trans_match,filename):
		file_out=open(filename,'w')
		for linea in list_trans_match:
			file_out.write(linea+"\n")
		#ENDFOR
		file_out.close()
	#ENDDEF
	#--------------------------------------------------------------#
	#Create the output directory	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	#ENDIF
	#--------------------------------------------------------------#
	#Read the original script
	archivo_ref=open(file_script,"r")
	all_lines_ref=archivo_ref.read()
	all_lines_ref=all_lines_ref.replace("\n"," ")
	all_lines_ref=all_lines_ref.strip()
	lista_ref=all_lines_ref.split(" ")
	archivo_ref.close()
	#--------------------------------------------------------------#
	#Read the transcriptions generated by the ASR system
	archivo_asr=open(file_asr,"r")
	lista_asr=[]
	for linea in archivo_asr:
		linea=linea.replace("\n","")
		lista_linea=linea.split(" ")
		lista_asr.append(lista_linea)
	#ENDFOR
	archivo_asr.close()
	#--------------------------------------------------------------#
	#Find the matches for the first transcription
	HASH_TM_PATHS={}
	prev_index=0
	list_prev_trans=lista_asr[prev_index]
	prev_trans_name=os.path.join(output_dir,list_prev_trans[0]+"_TMs.csv")
	HASH_TM_PATHS[list_prev_trans[0]]=prev_trans_name
	#Remove the fileID from the transcription list
	list_prev_trans.pop(0)
	#Find the best match for this transcription list
	list_prev_best_match=crocomad_best_match(lista_ref,list_prev_trans)
	#--------------------------------------------------------------#
	#for cur_index in range(1,2):
	for cur_index in range(1,len(lista_asr)):
		prev_index=cur_index-1
		list_cur_trans=lista_asr[cur_index]
		cur_trans_name=os.path.join(output_dir,list_cur_trans[0]+"_TMs.csv")
		HASH_TM_PATHS[list_cur_trans[0]]=cur_trans_name
		#Remove the fileID from the transcription list
		list_cur_trans.pop(0)
		list_cur_best_match=crocomad_best_match(lista_ref,list_cur_trans)
		#Align the matches with the reference. This process combine 3 lists into one.
		list_of_lists=[lista_ref,list_prev_best_match,list_cur_best_match]
		list_two_trans_matches=lists_to_list(list_of_lists)
		#Prune the previous list of transcription matches
		lista_trans_match,lista_rest=prune_trans_matches(list_two_trans_matches)
		#Write the previous transcription match in a file.
		trans_match_to_file(lista_trans_match,prev_trans_name)
			
		#------------------------------------------------------#	
		#Update variables or the next iteration.
		#------------------------------------------------------#
		#Obtain new lista_ref
		lista_ref_new=[]
		for linea in lista_rest:
			lista_linea=linea.split(",")
			word_ref=lista_linea[0]
			lista_ref_new.append(word_ref)
		#ENDFOR
		lista_ref=lista_ref_new
		#Prune best match. The lenght of this list has to be same
		#as the lenght of the lista_ref.
		list_prev_best_match=list_cur_best_match
		new_len=len(list_prev_best_match)-len(lista_ref_new)
		for cuenta in range(0,new_len):
			list_prev_best_match.pop(0)
		#ENDFOR
		#Update the name of the next output file
		prev_trans_name=cur_trans_name	
	#ENDFOR
	#Write the last transcription match to a file.
	trans_match_to_file(lista_rest,cur_trans_name)
	#Return the paths
	return HASH_TM_PATHS
#ENDDEF

########################################################################
