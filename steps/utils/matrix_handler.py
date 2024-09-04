#-*- coding: utf-8 -*- 
########################################################################
#matrix_handler.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 20th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 matrix_handler.py

#Example:

#	$ python3 matrix_handler.py

#Description:

#This is a python3 template.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import numpy as np
import jiwer as jw

########################################################################
def create_empty_vector(lista_asr):
	list_result_vector=[]
	for item in lista_asr:
		list_result_vector.append("*")
	#ENDFOR
	return list_result_vector
#ENDDEF
#----------------------------------------------------------------------#
def create_matching_matrix(lista_ref,lista_asr):
	matching_matrix=np.zeros((len(lista_ref),len(lista_asr)))
	for col_asr in range(0,len(lista_asr)):
		for row_ref in range(0,len(lista_ref)):
			#print(matching_matrix[row_ref,col_asr])
			word_asr=lista_asr[col_asr]
			word_ref=lista_ref[row_ref]
			if word_asr==word_ref:
				matching_matrix[row_ref,col_asr]=1.0
			#ENDIF
		#ENDFOR
	#ENDFOR
	return matching_matrix
#ENDDEF
#----------------------------------------------------------------------#
def define_search_area(matrix_in):
	rows_ref, cols_asr = matrix_in.shape
	max_num_of_diags=(rows_ref-cols_asr)+1
	hash_search_area={}
	row_offset=-1
	for col in range(0,cols_asr):
		row_offset=row_offset+1
		row_ini=row_offset
		row_end=row_ini+max_num_of_diags-1
		hash_search_area[col]=[row_ini,row_end]
	#ENDFOR
	return hash_search_area
#ENDDEF
#----------------------------------------------------------------------#
def search_in_area(matrix_in,hash_search_area,list_result_vector,list_asr):
	rows_ref, cols_asr = matrix_in.shape
	for col in range(0,cols_asr):
		lista_row_limits=hash_search_area[col]
		row_ini=lista_row_limits[0]
		row_end=lista_row_limits[-1]+1
		for row in range(row_ini,row_end):
			if matrix_in[row,col]==1.0:
				list_result_vector[col]=list_asr[col]
				break
			#ENDFOR
		#ENDFOR
	#ENDFOR
	return list_result_vector
#ENDDEF
#----------------------------------------------------------------------#
def find_gaps(matrix_in):
	rows_ref, cols_asr = matrix_in.shape
	max_num_of_diags=(rows_ref-cols_asr)+1
	lista_gaps=[]
	for diag in range(0,max_num_of_diags):
		col=0
		row=diag
		count_zeros=False
		num_zeros=0
		for index in range(0,cols_asr):
			fila_actual=row+index
			col_actual=col+index
			if matrix_in[fila_actual,col_actual]==1.0:
				if count_zeros==False:
					count_zeros=True
				else:
					if num_zeros==1:
						gap_row=fila_actual-1
						gap_col=col_actual-1
						lista_gaps.append([gap_row,gap_col])
					#ENDIF
					num_zeros=0
				#ENDIF
			else:
				if count_zeros==True:
					num_zeros=num_zeros+1
				#ENDIF
			#ENDIF	
		#ENDFOR
	#ENDFOR
	return lista_gaps
#ENDDEF
#----------------------------------------------------------------------#
def fill_the_gaps(lista_gaps,lista_res,lista_ref,lista_asr):
	for gap in lista_gaps:
		row_ref=gap[0]
		col_asr=gap[-1]
		word_ref=lista_ref[row_ref]
		word_asr=lista_asr[col_asr]
		cer=jw.cer(word_ref,word_asr)
		if cer<=0.5:
			lista_res[col_asr]=word_ref
		else:
			lista_res[col_asr]=word_asr
		#ENDIF
	#ENDFOR
	return lista_res
#ENDDEF
#----------------------------------------------------------------------#
def fill_leftovers(lista_res,lista_asr):
	col=-1
	for item in lista_res:
		col=col+1
		if lista_res[col]=="*":
			word_asr=lista_asr[col]
			lista_res[col]=word_asr
		#ENDIF
	#ENDFOR
	return lista_res
#ENDDEF
########################################################################

