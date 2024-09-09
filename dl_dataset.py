import argparse
from datasets import load_dataset
import librosa
import os
import soundfile as sf

# This script downloads an audio dataset from Huggingface and saves for each data row 2 files into the given data folder
# with the audio data in one file and the transcription text in another file. Both files have the same base name but
# different suffixes .wav/.txt.
#
# The dataset needs to have the following columns:
# {
#   'audio_id': 'leikfangavelin_007-0066-00:18:5686-00:00:0392',
#   'audio': {
#     'array': array([-0.03311157, -0.08340454, -0.11801147, ...,  0.        ,
#         0.00033569,  0.00054932], dtype=float32),
#     'sampling_rate': 16000
#   },
#   'normalized_text': 'hætti í bandinu skömmu eftir að platan sem ekki kom út var tekin upp'
# }
#
# By default, the dataset language-and-voice-lab/raddromur_asr is downloaded

def process_dataset(dataset, output_path, target_sr=None):
    print(f"Creating output directory: {output_path}")
    os.makedirs(output_path, exist_ok=True)

    print("Dataset structure:")
    print(dataset)

    if isinstance(dataset, dict):
        # If it's a DatasetDict, use the first split (usually 'train')
        split_name = list(dataset.keys())[0]
        dataset = dataset[split_name]
        print(f"\nUsing split: {split_name}")

    print("\nFirst item in dataset:")
    print(dataset[0])
    print("\nDataset columns:")
    print(dataset.column_names)
    print("\nProcessing dataset items:")

    for i, item in enumerate(dataset):
        print(f"\nProcessing item {i+1}")

        audio_id = item['audio_id']
        audio = item['audio']
        normalized_text = item['normalized_text']

        if not audio_id or not audio or not normalized_text:
            print(f"Skipping item {i+1} due to missing data")
            continue

        basename = audio_id

        print(f"  Creating audio file: {basename}.wav")
        audio_path = os.path.join(output_path, f"{basename}.wav")
        audio_data = audio['array']
        original_sr = audio['sampling_rate']

        if target_sr and target_sr != original_sr:
            print(f"  Resampling audio from {original_sr} Hz to {target_sr} Hz")
            audio_data = librosa.resample(audio_data, orig_sr=original_sr, target_sr=target_sr)
            sr_to_use = target_sr
        else:
            sr_to_use = original_sr

        sf.write(audio_path, audio_data, sr_to_use, subtype='PCM_16')

        print(f"  Creating text file: {basename}.txt")
        text_path = os.path.join(output_path, f"{basename}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(normalized_text)

    print("\nProcessing complete!")

def main():
    parser = argparse.ArgumentParser(description="""
    This script processes a Hugging Face dataset, creating audio and text file pairs.
    It downloads the dataset, extracts audio and text information, and saves them as separate files.
    Audio files are saved in WAV format (16-bit mono RIFF), and text files contain normalized transcriptions.
    """)

    parser.add_argument('--output', type=str, default='data_raddromur',
                        help='Path to create the output data files (default: data_raddromur)')
    parser.add_argument('--sample-rate', type=int,
                        help='Target sampling rate for audio files. If not provided, original sampling rate is used.')
    parser.add_argument('--dataset', type=str, default='language-and-voice-lab/raddromur_asr',
                        help='Hugging Face dataset to use (default: language-and-voice-lab/raddromur_asr)')
    parser.add_argument('--split', type=str, choices=['train', 'test', 'validation'],
                        help='Dataset split to use. If not provided, no split is used.')

    args = parser.parse_args()

    print("Loading dataset...")
    if args.split:
        print(f"Using dataset: {args.dataset}, split: {args.split}")
        dataset = load_dataset(args.dataset, split=args.split)
    else:
        print(f"Using dataset: {args.dataset}, no split specified")
        dataset = load_dataset(args.dataset)

    process_dataset(dataset, args.output, args.sample_rate)

if __name__ == "__main__":
    main()