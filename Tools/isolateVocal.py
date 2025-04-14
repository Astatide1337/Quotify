import os
import glob
import shutil
import torch
import demucs.separate

# === Step 1: Info ===
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# === Step 2: Define paths ===
base_dir = os.getcwd()
input_folder = os.path.join(base_dir, "inputVideosAudio")
demucs_model = "htdemucs"
demucs_output_dir = os.path.join(base_dir, "separated", demucs_model)
final_output_dir = os.path.join(base_dir, "output")

os.makedirs(final_output_dir, exist_ok=True)

# === Step 3: Find input MP3s ===
input_files = glob.glob(os.path.join(input_folder, "*.mp3"))
if not input_files:
    print("⚠️ No MP3 files found in inputVideosAudio/")
    exit()

# === Step 4: Process each file ===
for input_file in input_files:
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    print(f"\n🎧 Processing: {base_name}")

    cmd_args = [
        "--mp3",
        "--two-stems", "vocals",
        "-n", demucs_model,
        "--segment", "7",
        "--device", "cuda",
        input_file
    ]

    try:
        print("🚀 Starting separation...")
        demucs.separate.main(cmd_args)
        print("✅ Separation complete!")

        # Path to the Demucs output vocals.mp3
        vocals_path = os.path.join(demucs_output_dir, base_name, "vocals.mp3")
        if os.path.exists(vocals_path):
            # New name and destination
            new_name = f"{base_name}_vocals.mp3"
            destination = os.path.join(final_output_dir, new_name)
            shutil.move(vocals_path, destination)
            print(f"📦 Moved: {new_name}")
        else:
            print(f"⚠️ vocals.mp3 not found for: {base_name}")

    except Exception as e:
        print(f"❌ Error processing {base_name}: {e}")
