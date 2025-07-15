import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from audio_recorder import AudioRecorder
from history import RecordingHistory
import os
import numpy as np
import wave
import simpleaudio as sa
import tkinter.filedialog as filedialog

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sound Recorder GUI")
        self.root.geometry("700x500")
        self.audio_recorder = AudioRecorder(self.on_audio_data, self.on_recording_finished)
        self.is_recording = False
        self.setup_ui()
        self.update_timer()

    def setup_ui(self):
        self.root.configure(bg="#f7f7f7")
        topbar = tk.Frame(self.root, bg="#f7f7f7", height=50)
        topbar.pack(side=tk.TOP, fill=tk.X)
        self.record_btn = tk.Button(topbar, text="● Record", font=("Segoe UI", 12, "bold"), fg="#fff", bg="#2196f3", activebackground="#1976d2", bd=0, padx=20, pady=5, relief=tk.FLAT, command=self.toggle_recording, cursor="hand2")
        self.record_btn.pack(side=tk.LEFT, padx=16, pady=10)
        title = tk.Label(topbar, text="Sound Recorder GUI", font=("Segoe UI", 14, "bold"), bg="#f7f7f7", fg="#222")
        title.pack(side=tk.LEFT, padx=20)
        self.content = tk.Frame(self.root, bg="#f7f7f7")
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.recording_list_frame = tk.Frame(self.content, bg="#f7f7f7")
        self.recording_list_frame.pack(fill=tk.BOTH, expand=True)
        self.timer_label = tk.Label(topbar, text="00:00", font=("Segoe UI", 12), bg="#f7f7f7", fg="#666")
        self.timer_label.pack(side=tk.RIGHT, padx=16)
        self.refresh_recording_list()

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.audio_recorder.start_recording()
        self.record_btn.config(text="■ Stop", bg="#e53935", activebackground="#b71c1c")
        self.timer_seconds = 0

    def stop_recording(self):
        self.is_recording = False
        self.audio_recorder.stop_recording()
        self.record_btn.config(text="● Record", bg="#2196f3", activebackground="#1976d2")

    def on_audio_data(self, data):
        pass

    def on_recording_finished(self, filename, mp3_filename=None):
        messagebox.showinfo("Recording Saved", f"Recording saved as {os.path.basename(filename)}")
        self.refresh_recording_list()

    def refresh_recording_list(self):
        for widget in self.recording_list_frame.winfo_children():
            widget.destroy()
        recordings = RecordingHistory.get_all_recordings()
        for rec in recordings:
            RecordingCard(self.recording_list_frame, rec, refresh_callback=self.refresh_recording_list).pack(fill=tk.X, pady=8, padx=0)

    def update_timer(self):
        if self.is_recording:
            self.timer_seconds = getattr(self, 'timer_seconds', 0) + 1
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
        else:
            self.timer_label.config(text="00:00")
        self.root.after(1000, self.update_timer)

class RecordingCard(tk.Frame):
    def __init__(self, master, rec, refresh_callback=None, **kwargs):
        super().__init__(master, bg="#fff", bd=0, highlightthickness=0, **kwargs)
        self.configure(highlightbackground="#e0e0e0", highlightcolor="#e0e0e0", relief=tk.RIDGE)
        self.rec = rec
        self.refresh_callback = refresh_callback
        self.play_obj = None
        self.is_playing = False
        self.build_card()

    def build_card(self):
        top = tk.Frame(self, bg="#fff")
        top.pack(fill=tk.X, padx=16, pady=(10, 0))
        self.title_label = tk.Label(top, text=self.rec['title'], font=("Segoe UI", 11, "bold"), bg="#fff", fg="#222")
        self.title_label.pack(side=tk.LEFT)
        timestamp = tk.Label(top, text=self.rec['timestamp'], font=("Segoe UI", 9), bg="#fff", fg="#888")
        timestamp.pack(side=tk.LEFT, padx=12)
        duration = tk.Label(top, text=self.rec['duration'], font=("Segoe UI", 10), bg="#fff", fg="#666")
        duration.pack(side=tk.RIGHT)
        waveform = tk.Canvas(self, width=400, height=40, bg="#f7f7f7", bd=0, highlightthickness=0)
        waveform.pack(fill=tk.X, padx=16, pady=8)
        self.draw_waveform_preview(waveform, self.rec['filename'])
        controls = tk.Frame(self, bg="#fff")
        controls.pack(fill=tk.X, padx=16, pady=(0, 10))
        style = ttk.Style()
        style.configure('Card.TButton', font=("Segoe UI", 12), padding=6, relief="flat", background="#e3eafc", foreground="#222", borderwidth=0)
        style.map('Card.TButton', background=[('active', '#bbdefb'), ('!active', '#e3eafc')])
        ttk.Button(controls, text="🗑", style='Card.TButton', command=self.delete_recording).pack(side=tk.LEFT, padx=4)
        self.play_btn = ttk.Button(controls, text="▶", style='Card.TButton', command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="⬇", style='Card.TButton', command=self.download_recording).pack(side=tk.LEFT, padx=4)
        rename_btn = ttk.Button(controls, text="📝", style='Card.TButton', command=self.rename_recording)
        rename_btn.pack(side=tk.LEFT, padx=4)

    def draw_waveform_preview(self, canvas, filename):
        try:
            with wave.open(filename, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                samples = np.frombuffer(frames, dtype=np.int16)
                if len(samples) == 0:
                    return
                width = int(canvas['width'])
                height = int(canvas['height'])
                step = max(1, len(samples) // width)
                mid = height // 2
                scale = (height // 2) * 0.9 / max(1, np.max(np.abs(samples)))
                points = []
                for x in range(width):
                    idx = x * step
                    if idx < len(samples):
                        y = int(mid - samples[idx] * scale)
                        points.append((x, y))
                for i in range(1, len(points)):
                    canvas.create_line(points[i-1][0], points[i-1][1], points[i][0], points[i][1], fill='#4caf50', width=2)
        except Exception:
            pass

    def toggle_play(self):
        if not self.is_playing:
            try:
                wave_obj = sa.WaveObject.from_wave_file(self.rec['filename'])
                self.play_obj = wave_obj.play()
                self.is_playing = True
                self.play_btn.config(text="⏸")
                self.after(100, self.check_playback)
            except Exception:
                messagebox.showerror("Playback Error", "Unable to play this recording.")
        else:
            if self.play_obj:
                self.play_obj.stop()
            self.is_playing = False
            self.play_btn.config(text="▶")

    def check_playback(self):
        if self.play_obj and self.play_obj.is_playing():
            self.after(100, self.check_playback)
        else:
            self.is_playing = False
            self.play_btn.config(text="▶")

    def delete_recording(self):
        if messagebox.askyesno("Delete Recording", "Are you sure you want to delete this recording?"):
            try:
                os.remove(self.rec['filename'])
                if self.refresh_callback:
                    self.refresh_callback()
            except Exception:
                messagebox.showerror("Delete Error", "Unable to delete this recording.")

    def download_recording(self):
        dest = filedialog.asksaveasfilename(defaultextension=os.path.splitext(self.rec['filename'])[1], initialfile=os.path.basename(self.rec['filename']))
        if dest:
            try:
                with open(self.rec['filename'], 'rb') as src, open(dest, 'wb') as dst:
                    dst.write(src.read())
                messagebox.showinfo("Download", "Recording saved to chosen location.")
            except Exception:
                messagebox.showerror("Download Error", "Unable to save the recording.")

    def rename_recording(self):
        new_name = simpledialog.askstring("Rename Recording", "Enter new name:", initialvalue=os.path.splitext(os.path.basename(self.rec['filename']))[0])
        if new_name:
            new_path = os.path.join(os.path.dirname(self.rec['filename']), new_name + os.path.splitext(self.rec['filename'])[1])
            try:
                os.rename(self.rec['filename'], new_path)
                if self.refresh_callback:
                    self.refresh_callback()
            except Exception:
                messagebox.showerror("Rename Error", "Unable to rename the recording.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop() 