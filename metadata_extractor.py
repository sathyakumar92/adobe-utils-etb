import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.mp4 import MP4

class MetadataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}

    def extract_metadata(self):
        """Extracts metadata from the specified audio file."""
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

        try:
            audio_file = mutagen.File(self.file_path)
            if audio_file is None:
                raise ValueError("Unsupported audio format or file is corrupted.")

            self.metadata['filename'] = os.path.basename(self.file_path)
            self.metadata['file_size'] = os.path.getsize(self.file_path)
            self.metadata['length'] = audio_file.info.length  # Length in seconds

            # Extracting specific tags based on the file type
            if isinstance(audio_file, MP3):
                self.metadata['bitrate'] = audio_file.info.bitrate
                self.metadata['sample_rate'] = audio_file.info.sample_rate
            elif isinstance(audio_file, WAVE):
                self.metadata['sample_rate'] = audio_file.info.sample_rate
            elif isinstance(audio_file, MP4):
                self.metadata['bitrate'] = audio_file.info.bitrate
                self.metadata['sample_rate'] = audio_file.info.sample_rate

            # Add additional metadata tags
            if audio_file.tags:
                for key, value in audio_file.tags.items():
                    # Convert tag values to strings to handle different tag formats
                    if isinstance(value, list) and len(value) > 0:
                        self.metadata[key] = str(value[0])
                    else:
                        self.metadata[key] = str(value)

        except Exception as e:
            print(f"Error extracting metadata: {e}")
            raise  # Re-raise the exception so caller knows extraction failed

    def get_metadata(self):
        """Returns the extracted metadata."""
        return self.metadata

# Example usage (for testing purposes)
if __name__ == "__main__":
    extractor = MetadataExtractor('path/to/your/audio/file.mp3')  # Change this path
    extractor.extract_metadata()
    print(extractor.get_metadata())

# TODO: Add support for more audio formats
# TODO: Implement command line interface for easier user interaction
# TODO: Add unit tests for better reliability
# Limitations: Only extracts basic metadata; advanced tagging might not be supported.
