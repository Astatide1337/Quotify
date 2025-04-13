import os
from pydub import AudioSegment

def concatenate_wav_files(directory, output_filename):
    # Get all WAV files
    files = [f for f in os.listdir(directory) if f.endswith('.wav') and 'complete_collection' not in f]
    
    # Sort files to ensure they're in chronological order
    files.sort()
    
    print(f"Found {len(files)} files to concatenate")
    
    # Initialize with the first file
    try:
        combined = AudioSegment.from_wav(os.path.join(directory, files[0]))
        print(f"Starting with: {files[0]}")
        
        # Append each additional file
        for file in files[1:]:
            print(f"Adding: {file}")
            audio = AudioSegment.from_wav(os.path.join(directory, file))
            combined += audio
            
        # Export the combined audio
        print(f"Exporting to {output_filename}")
        combined.export(output_filename, format="wav")
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Current directory where the script is run
    directory = "."
    output_file = "fireship_complete_collection.wav"
    
    concatenate_wav_files(directory, output_file)