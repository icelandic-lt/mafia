#-*- coding: utf-8 -*- 
########################################################################
#libcrocomad.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 18th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 libcrocomad.py

#Example:

#	$ python3 libcrocomad.py

#Description:

#This is a python3 template.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################

def crocomad_best_match(list_in1,list_in2):
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Setting up input values	
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#The longest list will be the reference and the other will
	#be the hypothesis	
	if len(list_in1)>=len(list_in2):
		LIST_REF=list_in1
		LIST_HYP=list_in2
	else:
		LIST_REF=list_in2
		LIST_HYP=list_in1
	#ENDIF
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Internal Functions
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#The function step_fwd() shifts the input list one place to
	#the right.
	def step_fwd(lista_in):
		len_lista_in=len(lista_in)
		lista_out=["."]
		for i in range(0,len_lista_in-1):
			lista_out.append(lista_in[i])
		#ENDFOR
		return lista_out
	#ENDDEF
	#--------------------------------------------------------------#
	#The function extract_indexes() provides two list containing 
	#indexes corresponding to the current cross-correlation step.
	def extract_indexes(list_ref_in,list_hyp_in):
		list_ref_out=[]
		list_hyp_out=[]
		for i in range(0,len(list_ref_in)):
			if list_ref_in[i]!="." and list_hyp_in[i]!=".":
				list_ref_out.append(list_ref_in[i])
				list_hyp_out.append(list_hyp_in[i])
			#ENDIF
		#ENDFOR
		return [list_ref_out,list_hyp_out]
	#ENDDEF
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#The algorithm begins here.
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Calculating some relevant lenghts.
	ref_len=len(LIST_REF)
	hyp_len=len(LIST_HYP)
	vector_len=ref_len+2*hyp_len-2	
	#--------------------------------------------------------------#
	#Initialize the reference
	lista_ref=[]
	for i in range(0,hyp_len-1):
		lista_ref.append(".")
	#ENDFOR
	for i in range(0,ref_len):
		lista_ref.append(i)
	#ENDFOR
	for i in range(0,hyp_len-1):
		lista_ref.append(".")
	#ENDFOR
	#--------------------------------------------------------------#
	#Initialize the hypotesis
	lista_hyp=[]
	for j in range(0,vector_len):
		if j < hyp_len:
			lista_hyp.append(j)
		else:
			lista_hyp.append(".")
		#ENDDEF
	#ENDFOR
	#--------------------------------------------------------------#
	#Match the lenght of the ref and hyp if still necessary
	diff=len(lista_ref)-len(lista_hyp)
	if diff>0:
		for cont in range(0,diff):
			lista_hyp.append(".")
		#ENDFOR
	#ENDIF	
	#--------------------------------------------------------------#
	#Performing the cross-correlation.	
	#--------------------------------------------------------------#
	#This external "for" performs the whole cross-correlation
	#between the reference and the hypothesis.
	max_num_matches_found=0
	lista_best_aligment=[]
	num_of_shifts=len(LIST_REF)+len(LIST_HYP)-1
	for k in range(0, (len(LIST_REF)+len(LIST_HYP)-1)):
		#Extracting the indexes corresponding to the current
		#cross-correlation step.
		indexes_ref, indexes_hyp = extract_indexes(lista_ref,lista_hyp)

		#Extracting just the portion of the string indicated
		#by the indexes calculated above and counting the
		#number of character-matches.
		num_matches=0
		for m in range(0,len(indexes_ref)):
			index_ref=indexes_ref[m]
			index_hyp=indexes_hyp[m]
			if LIST_REF[index_ref]==LIST_HYP[index_hyp]:
				num_matches=num_matches+1
			#ENDIF
		#ENDDEF
		#If the number of matches is greater than the one
		#found before, store it.
		if num_matches>max_num_matches_found:
			max_num_matches_found=num_matches
			lista_best_aligment=lista_hyp
			
		#ENDIF

		#Performing the next cross-correlation step.
		lista_hyp=step_fwd(lista_hyp)
	#ENDFOR
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	lista_all_words=[]
	lista_only_matches=[]
	for index in range(0,len(lista_ref)):
		if lista_ref[index]!=".":
			idx_ref = lista_ref[index]
			if len(lista_best_aligment)>0:
				idx_best_al=lista_best_aligment[index]
			else:
				idx_best_al=lista_hyp[index]
			#ENDIF
			if idx_best_al!=".":
				lista_all_words.append(LIST_HYP[idx_best_al])
				item_ref=LIST_REF[idx_ref]
				item_hyp=LIST_HYP[idx_best_al]			
				if item_ref==item_hyp:
					lista_only_matches.append(item_hyp)
				else:
					lista_only_matches.append('.')
				#ENDIF
			else:
				lista_all_words.append(idx_best_al)
				lista_only_matches.append('.')
			#ENDIF
		#ENDIF
	#ENDFOR	
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#return lista_all_words, lista_only_matches
	return lista_all_words
#ENDDEF

########################################################################

