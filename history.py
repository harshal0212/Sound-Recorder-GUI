import tkinter as tk
from tkinter import ttk
import os
import sys
import glob
import wave
import datetime

class RecordingHistory(ttk.Frame):
    def __init__(self, master, on_select_recording, recordings_dir=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_select_recording = on_select_recording
        self.recordings_dir = recordings_dir or os.path.join(os.getcwd(), "recordings")
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<Double-1>', self._on_double_click)
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        files = sorted(glob.glob(os.path.join(self.recordings_dir, '*.wav')) +
                       glob.glob(os.path.join(self.recordings_dir, '*.mp3')),
                       reverse=True)
        for f in files:
            self.listbox.insert(tk.END, os.path.basename(f))

    def add_recording(self, filename):
        self.refresh()

    def _on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            filename = self.listbox.get(selection[0])
            full_path = os.path.join(self.recordings_dir, filename)
            self.open_file(full_path)
            if self.on_select_recording:
                self.on_select_recording(full_path)

    @staticmethod
    def open_file(path):
        if sys.platform.startswith('darwin'):
            os.system(f'open "{path}"')
        elif os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            os.system(f'xdg-open "{path}"')

    @staticmethod
    def get_all_recordings():
        recordings_dir = os.path.join(os.getcwd(), "recordings")
        files = sorted(glob.glob(os.path.join(recordings_dir, '*.wav')) +
                       glob.glob(os.path.join(recordings_dir, '*.mp3')),
                       reverse=True)
        recordings = []
        for f in files:
            basename = os.path.basename(f)
            # Title: Recording N (from filename or index)
            title = os.path.splitext(basename)[0].replace('_', ' ').capitalize()
            # Timestamp: from file creation time
            try:
                ctime = os.path.getctime(f)
                timestamp = datetime.datetime.fromtimestamp(ctime).strftime("%H:%M:%S")
            except Exception:
                timestamp = ""
            # Duration: for WAV files
            duration = ""
            if f.lower().endswith('.wav'):
                try:
                    with wave.open(f, 'rb') as wf:
                        frames = wf.getnframes()
                        rate = wf.getframerate()
                        seconds = int(frames / float(rate))
                        mins, secs = divmod(seconds, 60)
                        duration = f"{mins:02}:{secs:02}"
                except Exception:
                    duration = "--:--"
            else:
                duration = "--:--"
            recordings.append({
                'title': title,
                'timestamp': timestamp,
                'duration': duration,
                'filename': f
            })
        return recordings 