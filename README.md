# Voice Recorder GUI

A feature-rich, cross-platform voice recorder application built with Python, Tkinter, and PyAudio. Includes real-time waveform visualization, dark/light mode, and export to WAV/MP3.

## Features

- 🎛️ User-Friendly Interface with Start/Stop buttons, duration timer, and stylish layout
- 🎤 Real-Time Voice Capture with configurable sample rate, channels, and format
- 📈 Live Visual Feedback (VU Meter / waveform animation during recording)
- 🎧 WAV File Export with automatic timestamp-based filenames
- 📂 Recording History Log to browse previously saved clips
- 💾 Audio Compression Support (optional: MP3 using pydub and ffmpeg)
- 🌙 Dark Mode/Light Mode toggle using Tkinter ttk.Style
- 🧪 Tested for cross-platform compatibility (Windows/Linux/MacOS)

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd "Voice Recorder GUI"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   - For MP3 export, install [ffmpeg](https://ffmpeg.org/download.html) and ensure it is in your system PATH.

3. **Run the application**

   ```bash
   python main.py
   ```

## Usage

- Click **Start Recording** to begin capturing audio.
- Watch the real-time waveform for visual feedback.
- Click **Stop Recording** to save the file (WAV by default, MP3 if enabled).
- Browse and open previous recordings from the history log.
- Toggle between dark and light mode using the theme button.

## Configuration

- Sample rate, channels, and format can be adjusted in `audio_recorder.py`.
- MP3 export requires `pydub` and `ffmpeg`.

## Dependencies

- Python 3.7+
- PyAudio
- numpy
- pydub (for MP3 export)
- ffmpeg (system dependency for MP3 export)
- Tkinter (included with Python)

## License

MIT License 