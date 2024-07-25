# cli.py

import argparse
from TTS import TTS, DynamicPoems, Static, CreateVideo, CleanUp

def main():
    parser = argparse.ArgumentParser(description="Video Bot CLI")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # TTS Command
    tts_parser = subparsers.add_parser("tts", help="Generate TTS audio")
    tts_parser.add_argument("text", type=str, help="Text to convert to speech")
    tts_parser.add_argument("speaker", type=str, help="Speaker name")
    tts_parser.add_argument("filename", type=str, help="Output filename")
    
    # Dynamic Poems Command
    dynamic_parser = subparsers.add_parser("dynamic", help="Fetch dynamic poems")
    
    # Static Poems Command
    static_parser = subparsers.add_parser("static", help="Fetch static poems")
    static_parser.add_argument("speaker", type=str, help="Speaker name")

    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up files in Music, Subtitles, WAVFILES")
    
    args = parser.parse_args()
    
    if args.command == "tts":
        TTS(args.text, args.speaker, args.filename)
    elif args.command == "dynamic":
        poems = DynamicPoems()
    elif args.command == "static":
        Static(args.speaker)
    elif args.command == "cleanup":
        CleanUp()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()