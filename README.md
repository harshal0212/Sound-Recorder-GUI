# Voice Recorder GUI

A modern, cross-platform voice recorder application built with Python and Tkinter. Features real-time waveform visualization, easy recording management, and export to WAV/MP3.

## Features

- 🎛️ User-friendly interface with prominent Record/Stop button and timer
- 🎤 Real-time voice capture with configurable sample rate and channels
- 📈 Live waveform preview for each recording
- 🎧 WAV file export with automatic timestamp-based filenames
- 📂 Recording history log to browse, play, rename, delete, and download clips
- 💾 Optional MP3 export (requires ffmpeg and pydub)
- 🧪 Cross-platform: Windows, Linux, MacOS

## Setup

### 1. Clone the repository
```sh
git clone https://github.com/yourusername/voice-recorder-gui.git
cd "voice-recorder-gui"
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```
- For MP3 export, install [ffmpeg](https://ffmpeg.org/download.html) and ensure it is in your system PATH.

### 3. Run the application
```sh
python main.py
```

## Usage
- Click **Record** to start recording audio.
- Click **Stop** to finish and save the recording.
- Browse, play, rename, delete, or download recordings from the list.
- All recordings are saved in the `recordings/` folder.

## Project Structure
```
voice-recorder-gui/
├── main.py
├── audio_recorder.py
├── history.py
├── requirements.txt
├── README.md
└── recordings/           # (auto-created, not tracked in git)
```

## Contributing
1. Fork this repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to your fork: `git push origin feature/your-feature`
5. Open a Pull Request on GitHub

## License
MIT License 