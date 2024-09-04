#-*- coding: utf-8 -*- 
########################################################################
#transcribe_segments.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 26th, 2022
#Location : Reykjavík University

#Usage:

#	$ python3 transcribe_segments.py <dir_seg_paths> <acoustic_model> <lang_model>

#Description:

#This script uses NeMo to decode the audio segments.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import os

import nemo
import nemo.collections.asr as nemo_asr
import numpy as np

########################################################################
#Input parameters

NUM_JOBS=int(sys.argv[1])
DIR_SEGMENTS_PATHS=sys.argv[2]
PRETRAINED_MODEL=sys.argv[3]
LANGUAGE_MODEL=sys.argv[4]
TRANS_OUT_DIR=sys.argv[5]
LOGITS_OUT_DIR=sys.argv[6]
DATA_PATHS=sys.argv[7]

########################################################################
#Create folders for the files of paths

data_path_logits=os.path.join(DATA_PATHS,"logits_paths")
if not os.path.exists(data_path_logits):
	os.mkdir(data_path_logits)
#ENDIF

########################################################################
#Collect the Segments Paths in a single file
list_audios=[]
HASH_GROUPS={}
for root, dirs, files in os.walk(DIR_SEGMENTS_PATHS):
	for filename in files:
		path_to_file=os.path.join(root,filename)
		groupID=filename.replace("_segments.paths","")
		#Create a directory for the transcriptions and for the logits.
		#Both have similar structures.
		logits_path_dir=os.path.join(LOGITS_OUT_DIR,groupID)
		if not os.path.exists(logits_path_dir):
			os.mkdir(logits_path_dir)
		#ENDIF
		file_paths=open(path_to_file,'r')
		for seg_path in file_paths:
			seg_path=seg_path.replace("\n","")
			if os.path.exists(seg_path):
				list_audios.append(seg_path)
				wavID=os.path.basename(seg_path)
				wavID=wavID.replace(".wav","")
				HASH_GROUPS[wavID]=groupID
			else:
				print("File not Found: "+seg_path)
			#ENDIF
		#ENDFOR
	#ENDFOR
#ENDFOR

########################################################################
#Loading the pretrained model 
nemo_asr_model = nemo_asr.models.EncDecCTCModel.restore_from(PRETRAINED_MODEL)

########################################################################
# Instantiate BeamSearchDecoderWithLM module.
beam_search_lm = nemo_asr.modules.BeamSearchDecoderWithLM(
	vocab=list(nemo_asr_model.decoder.vocabulary),
	beam_width=16,
	alpha=2, beta=1.5,
	lm_path=LANGUAGE_MODEL,
	num_cpus=max(NUM_JOBS, 1),
	input_tensor=False)

########################################################################
# Softmax implementation in NumPy
def softmax(logits):
	e = np.exp(logits - np.max(logits))
	return e / e.sum(axis=-1).reshape([logits.shape[0], 1])
#ENDDEF

########################################################################

def create_logits_name(wav_path_in):
	name_logits=os.path.basename(wav_path_in)
	name_logits=name_logits.replace(".wav","")
	name_logits=name_logits+"_logits"
	return name_logits
#ENDDEF

########################################################################
#Decoding the list of files with NeMo
HASH_LOGITS_PATHS={}
HASH_TRANS={}
for wav_file, current_logits in zip(list_audios, nemo_asr_model.transcribe(paths2audio_files=list_audios, logprobs=True,batch_size=NUM_JOBS)):
	#Determine the group
	logits_name=create_logits_name(wav_file)
	fileID=os.path.basename(wav_file)
	fileID=fileID.replace(".wav","")
	GROUP=HASH_GROUPS[fileID]	
	#Save the current logit in a file
	logits_path=os.path.join(LOGITS_OUT_DIR,GROUP,logits_name)
	np.save(logits_path,current_logits)
	HASH_LOGITS_PATHS[fileID]=logits_path+".npy"
	#Convert logits into probabilities.
	probs = softmax(current_logits)
	# Printing the best candidates for each audio file
	best_candidate=beam_search_lm.forward(log_probs = np.expand_dims(probs, axis=0), log_probs_length=None)[0][0]
	#print(best_candidate[-1])
	#line_out=format_line_out(wav_file, best_candidate[-1])
	trans_out=best_candidate[-1]
	HASH_TRANS[fileID]=trans_out
#ENDFOR

########################################################################
#Clasify the transcriptions and the logits before written them in a file
HASH_CLASSIFIED_TRANS={}
HASH_CLASSIFIED_LOGITS={}

for fileID in HASH_TRANS:
	group=HASH_GROUPS[fileID]
	current_trans=HASH_TRANS[fileID]
	line_trans=fileID+" "+current_trans
	logit_path=HASH_LOGITS_PATHS[fileID]
	line_logit=fileID+" "+logit_path
	if group not in HASH_CLASSIFIED_TRANS:
		HASH_CLASSIFIED_TRANS[group]=[line_trans]
	else:
		HASH_CLASSIFIED_TRANS[group].append(line_trans)
	#ENDIF	
	if group not in HASH_CLASSIFIED_LOGITS:
		HASH_CLASSIFIED_LOGITS[group]=[line_logit]
	else:
		HASH_CLASSIFIED_LOGITS[group].append(line_logit)
	#ENDIF
#ENDFOR

########################################################################
#Write the transcriptions in files
LIST_TRANS_FILE_PATHS=[]
HASH_TRANS_FILE_PATHS={}
for group in HASH_CLASSIFIED_TRANS:
	list_trans=HASH_CLASSIFIED_TRANS[group]
	list_trans.sort()
	#Create the output file	
	group_file_path=os.path.join(TRANS_OUT_DIR,group+".trans")
	LIST_TRANS_FILE_PATHS.append(group_file_path)
	HASH_TRANS_FILE_PATHS[group_file_path]=group
	group_file=open(group_file_path,'w')
	for line in list_trans:
		group_file.write(line+"\n")
	#ENDFOR
	group_file.close()
#ENDFOR

########################################################################
#Register the transcription files in a paths file
FILE_TRANS_PATHS_path=os.path.join(DATA_PATHS,"asr_transcriptions.paths")
file_trans_paths=open(FILE_TRANS_PATHS_path,'w')
LIST_TRANS_FILE_PATHS.sort()
for path in LIST_TRANS_FILE_PATHS:
	group=HASH_TRANS_FILE_PATHS[path]
	line_out=group+" "+path
	file_trans_paths.write(line_out+"\n")
#ENDFOR
file_trans_paths.close()

########################################################################
#Register the logits paths in files
LIST_LOGITS_FILE_PATHS=[]
for group in HASH_CLASSIFIED_LOGITS:
	list_logits=HASH_CLASSIFIED_LOGITS[group]
	list_logits.sort()
	#Create the output file	
	group_file_path=os.path.join(data_path_logits,group+"_logits.paths")
	group_file=open(group_file_path,'w')
	for line in list_logits:
		group_file.write(line+"\n")
	#ENDFOR
	group_file.close()
#ENDFOR

########################################################################
print("Decoding Done!!!")
########################################################################
