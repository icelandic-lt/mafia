#-*- coding: utf-8 -*- 
########################################################################
#segment_audio.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 26th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 segment_audio.py <audio_paths_list> <csv_segment_list> <output_dir>

#Description:

#This program uses ffmpeg to segment the specified audio files.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import os

########################################################################
#INPUT PARAMETERS

path_AUDIO_PATHS=sys.argv[1]
path_CSV_PATHS=sys.argv[2]
SEGMENTS_OUT_DIR=sys.argv[3]

########################################################################
#Read the audio paths

file_audio_paths=open(path_AUDIO_PATHS,'r')
HASH_AUDIO_PATHS={}
for line in file_audio_paths:
	line=line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	audio_path=list_line[-1]
	HASH_AUDIO_PATHS[fileID]=audio_path
#ENDFOR
file_audio_paths.close()

########################################################################
#Read the CSV paths

file_csv_paths=open(path_CSV_PATHS,'r')
HASH_CSV_PATHS={}
for line in file_csv_paths:
	line=line.replace("\n","")
	list_line=line.split(" ")
	fileID=list_line[0]
	csv_path=list_line[-1]
	HASH_CSV_PATHS[fileID]=csv_path
#ENDFOR
file_csv_paths.close()

########################################################################
#Create a directory for the segment paths
base_dir=os.path.dirname(path_CSV_PATHS)

SEGMENTS_PATHS_DIR=os.path.join(base_dir,"segments_paths")

if not os.path.exists(SEGMENTS_PATHS_DIR):
	os.mkdir(SEGMENTS_PATHS_DIR)
#ENDIF

########################################################################
#GLOBAL FUNCTIONS
########################################################################

def put_zeros(time_in):
	time_in=str(time_in)
	lista_time=time_in.split(".")
	time_out=lista_time[0]
	if len(time_out)==1:
		time_out="0"+time_in
	else:
		time_out=time_in
	#ENDIF
	#Pone un cero después del punto
	if len(lista_time[-1])==1 and len(lista_time)>1:
		time_out=time_out+"0"
	#ENDIF
	return time_out
#ENDDEF

#----------------------------------------------------------------------#

def time_format(secs_in):
	#Calculate hours
	hours=int(secs_in/3600)
	#Calculate minutes
	mins=int(secs_in/60)
	#Calculate seconds
	secs=float(round(secs_in-mins*60-hours*3600,2))
	#Time in the output format
	hours=put_zeros(hours)
	mins =put_zeros(mins)
	secs =put_zeros(secs)
	time_out=str(hours)+":"+str(mins)+":"+str(secs)
	return time_out
#ENDDEF

#----------------------------------------------------------------------#

def left_zeros(num_in):
	num_out=str(num_in)
	if len(num_out)==1:
		num_out="000"+num_out
	elif len(num_out)==2:
		num_out="00"+num_out
	elif len(num_out)==3:
		num_out="0"+num_out
	elif len(num_out)>=4:
		num_out="0"+num_out
	#ENDIF
	return num_out
#ENDDEF

#----------------------------------------------------------------------#

def time_naming(time_in):
	time_out=time_in.replace(".","")
	return time_out
#ENDDEF

#----------------------------------------------------------------------#

def extract_csv_info(csv_file):
	#--------------------------------------------------------------#
	#Ignore the header of the CSV file
	for header in csv_file:
		break
	#ENDFOR
	#--------------------------------------------------------------#
	#Read the files of the CSV file
	#--------------------------------------------------------------#
	HASH_CSV={}
	lista_csv=[]
	speech_max=0
	speech_min=10000
	CONT=0
	for linea in csv_file:
		CONT=CONT+1
		linea = linea.replace("\n","")
		lista_linea=linea.split("\t")
		label = lista_linea[0]
		start = round(float(lista_linea[1]),2)
		stop = round(float(lista_linea[2]),2)
		duration = round(stop-start,2)
		#wf means "with format"
		start_wf=time_format(start)
		stop_wf =time_format(stop)
		duration_wf=time_format(duration)
		#fn means "for name"
		start_fn=time_naming(start_wf)
		stop_fn =time_naming(stop_wf)
		duration_fn=time_naming(duration_wf)
		#Create the filename
		file_name=fileID+"-NUM_AUDIO-"+start_fn+"-"+duration_fn+".wav"
		#Create a list with relevant information
		lista_out = [label, start, stop, duration, start_wf, stop_wf,duration_wf,file_name]
		lista_csv.append(lista_out)
	#ENDFOR
	#--------------------------------------------------------------#
	return lista_csv
#ENDDEF

########################################################################
#SEGMENTATION TASK
########################################################################

for fileID in HASH_CSV_PATHS:
	#--------------------------------------------------------------#
	#Read the current CSV path
	csv_path=HASH_CSV_PATHS[fileID]
	print("Processing Segments in: "+csv_path)
	#Open the CSV file
	current_csv=open(csv_path,'r')
	#Extract information from the current CSV
	lista_csv=extract_csv_info(current_csv)
	#--------------------------------------------------------------#
	#Create file for the segments of the current CSV
	name_segs_paths_file=os.path.join(SEGMENTS_PATHS_DIR,fileID+"_segments.paths")
	FILE_SEGMENTS_PATHS=open(name_segs_paths_file,'w')
	#--------------------------------------------------------------#
	#Create a directory for the segments of the current audio
	CURRENT_SEGS_DIR=os.path.join(SEGMENTS_OUT_DIR,fileID)
	if not os.path.exists(CURRENT_SEGS_DIR):
		os.mkdir(CURRENT_SEGS_DIR)
	#ENDIF
	#--------------------------------------------------------------#
	#Start the Segmentation with ffmpeg
	#--------------------------------------------------------------#
	idxLabel=0
	idxStart=1
	idxStop=2
	idxDur=3
	idxStartWF=4
	idxStopWF=5
	idxDurWF=6
	idxFilename=7
	audio_in=HASH_AUDIO_PATHS[fileID]
	CONT=0
	lista_files_asr=[]
	for tupla in lista_csv:	
		label=tupla[idxLabel]
		duration=tupla[idxDur]
		
		filename=tupla[idxFilename]

		if label=="speech" and duration>=3.0:
			CONT=CONT+1
			num_audio=left_zeros(CONT)
			filename=filename.replace("NUM_AUDIO",num_audio)
			ruta_wav_actual=os.path.join(CURRENT_SEGS_DIR,filename)
			lista_files_asr.append(ruta_wav_actual)
			
			start=tupla[idxStart]
			
			comando_ffmpeg='ffmpeg -i '+audio_in+' -loglevel panic -vn -acodec copy -ss '+str(start)+' -t '+str(duration)+' '+ruta_wav_actual

			FILE_SEGMENTS_PATHS.write(ruta_wav_actual+"\n")
			if not os.path.exists(ruta_wav_actual):
				#Ejecuta el comando
				try:
					print("Creating Segment: "+ruta_wav_actual)
					os.system(comando_ffmpeg)
				except Exception as e:
					exit(e)
					print(e)
				#ENDTRY
			#ENDIF
		#ENDDEF	
	#ENDFOR
	#--------------------------------------------------------------#
	FILE_SEGMENTS_PATHS.close()
#ENDFOR

########################################################################

