#-*- coding: utf-8 -*- 
########################################################################
#csv_handler.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 18th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 csv_handler.py

#Example:

#	$ python3 csv_handler.py

#Description:

#This is a python3 template.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################

def lists_to_csv(list_with_lists, name_of_csv):
	#--------------------------------------------------------------#
	def get_max_len(list_with_lists):
		MAX_LEN=0
		for lista in list_with_lists:
			if len(lista) > MAX_LEN:
				MAX_LEN=len(lista)
			#ENDIF
		#ENDFOR
		return MAX_LEN
	#ENDDEF
	#--------------------------------------------------------------#
	def match_len(list_in, target_len):
		current_len=len(list_in)
		for index in range(current_len, target_len):
			list_in.append(".")
		#ENDFOR
		return list_in
	#ENDDEF
	#--------------------------------------------------------------#
	#MAIN TASK
	#--------------------------------------------------------------#
	MAX_LEN=get_max_len(list_with_lists)
	for lista in list_with_lists:
		if len(lista) != MAX_LEN:
			match_len(lista, MAX_LEN)
		#ENDIF
	#ENDFOR
	hash_csv={}
	for lista in list_with_lists:
		index=-1
		for item in lista:
			index=index+1
			if index not in hash_csv:
				hash_csv[index]=[item]
			else:
				hash_csv[index].append(item)
			#ENDIF
		#ENDFOR
	#ENDFOR
	file_csv=open(name_of_csv,"w")
	for index in range(0, MAX_LEN):
		lista=hash_csv[index]
		linea_out=",".join(lista)
		file_csv.write(linea_out+"\n")
	#ENDFOR
	file_csv.close()
#ENDDEF

########################################################################

def lists_to_list(list_with_lists):
	#--------------------------------------------------------------#
	def get_max_len(list_with_lists):
		MAX_LEN=0
		for lista in list_with_lists:
			if len(lista) > MAX_LEN:
				MAX_LEN=len(lista)
			#ENDIF
		#ENDFOR
		return MAX_LEN
	#ENDDEF
	#--------------------------------------------------------------#
	def match_len(list_in, target_len):
		current_len=len(list_in)
		for index in range(current_len, target_len):
			list_in.append(".")
		#ENDFOR
		return list_in
	#ENDDEF
	#--------------------------------------------------------------#
	#MAIN TASK
	#--------------------------------------------------------------#
	MAX_LEN=get_max_len(list_with_lists)
	for lista in list_with_lists:
		if len(lista) != MAX_LEN:
			match_len(lista, MAX_LEN)
		#ENDIF
	#ENDFOR
	hash_csv={}
	for lista in list_with_lists:
		index=-1
		for item in lista:
			index=index+1
			if index not in hash_csv:
				hash_csv[index]=[item]
			else:
				hash_csv[index].append(item)
			#ENDIF
		#ENDFOR
	#ENDFOR
	output_list=[]
	for index in range(0, MAX_LEN):
		lista=hash_csv[index]
		linea_out=",".join(lista)
		output_list.append(linea_out)
	#ENDFOR
	return output_list
#ENDDEF

########################################################################

def prune_trans_matches(list_trans_matches):
	lista_empty_1=[]
	lista_col_1=[]
	lista_empty_2=[]
	lista_col_2=[]
	lista_rest=[]

	store_empty_1=True
	store_col_1=False
	store_empty_2=False
	store_col_2=False
	store_rest=False
	#--------------------------------------------------------------#
	#The task of pruning begins here
	#--------------------------------------------------------------#
	for linea in list_trans_matches:
		lista_linea=linea.split(",")
		word_ref=lista_linea[0]
		word_col1=lista_linea[1]
		word_col2=lista_linea[2]
		if store_empty_1==True:
			if word_col1!=".":
				store_empty_1=False
				store_col_1=True
			else:
				linea_out=word_ref+",."
				lista_empty_1.append(linea_out)
			#ENDIF
		#ENDIF
		if store_col_1==True:
			if word_col1!=".":
				linea_out=word_ref+","+word_col1
				lista_col_1.append(linea_out)
			else:
				store_col_1=False
				store_empty_2=True
			#ENDIF
		#ENDIF
		if store_empty_2==True:
			if word_col2!=".":
				store_empty_2=False
				store_col_2=True
			else:
				linea_out=word_ref+",."
				lista_empty_2.append(linea_out)
			#ENDIF
		#ENDIF
		if store_col_2==True:
			if word_col2!=".":
				linea_out=word_ref+","+word_col2
				lista_col_2.append(linea_out)
			else:
				store_col_2=False
				store_rest=True
			#ENDIF	
		#ENDIF
		if store_rest==True:
			linea_out=word_ref+",."
			lista_rest.append(linea_out)
		#ENDIF
	#ENDFOR
	#--------------------------------------------------------------#
	#Create the output lists
	#--------------------------------------------------------------#
	lista_pruned=lista_empty_1+lista_col_1+lista_empty_2
	lista_rest=lista_empty_2+lista_col_2+lista_rest
	
	return lista_pruned, lista_rest
#ENDDEF


########################################################################

