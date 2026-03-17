import os
import sys
from mutagen import File

def extract_metadata(audio_file):
    """Extract metadata from audio file using mutagen"""
    audio_file_obj = File(audio_file)
    if audio_file_obj is None:
        return None
    
    metadata = {}
    for key, value in audio_file_obj.items():
        if isinstance(value, list):
            if len(value) == 1:
                metadata[key] = str(value[0])
            else:
                metadata[key] = ', '.join(str(v) for v in value)
        else:
            metadata[key] = str(value)
    return metadata

def main():
    # Check if the user provided a file path
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]

    # Ensure the file exists
    if not os.path.isfile(audio_file):
        print(f"Error: The file '{audio_file}' does not exist.")
        sys.exit(1)

    # Check if the file has a supported audio extension
    supported_extensions = ['.wav', '.mp3', '.aac', '.flac', '.ogg']
    if not any(audio_file.lower().endswith(ext) for ext in supported_extensions):
        print(f"Error: The file '{audio_file}' does not have a supported audio format.")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        sys.exit(1)

    # Try to extract metadata
    try:
        metadata = extract_metadata(audio_file)
        if metadata:
            print("Metadata extracted successfully:")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print("Warning: No metadata found in the file.")
    except Exception as e:
        print(f"An error occurred while extracting metadata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
