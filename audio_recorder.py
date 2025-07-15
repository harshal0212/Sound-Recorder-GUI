import pyaudio
import wave
import threading
import datetime
import os
import random
try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

class AudioRecorder:
    lock: threading.Lock  # type annotation for linter
    def __init__(self, on_audio_data, on_recording_finished, sample_rate=44100, channels=1, format=pyaudio.paInt16, chunk=1024, export_mp3=False):
        self.on_audio_data = on_audio_data
        self.on_recording_finished = on_recording_finished
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format
        self.chunk = chunk
        self.export_mp3 = export_mp3
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.thread = None
        self.filename = None
        self.wav_dir = os.path.join(os.getcwd(), "recordings")
        os.makedirs(self.wav_dir, exist_ok=True)
        self.lock = threading.Lock()

    def start_recording(self):
        self.frames = []
        self.is_recording = True
        self.filename = self._generate_filename()
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.thread:
            self.thread.join()
        self._save_wav()
        if self.export_mp3 and AudioSegment:
            self._export_mp3()
        self.on_recording_finished(self.filename)

    def _record(self):
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.sample_rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)
        while self.is_recording:
            data = stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)
            if self.on_audio_data:
                self.on_audio_data(data)
        stream.stop_stream()
        stream.close()

    def _save_wav(self):
        if not self.filename:
            print("No filename specified for saving WAV.")
            return False
        try:
            with self.lock:
                frames = list(self.frames)
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            return True
        except Exception as e:
            print(f"Error saving WAV file: {e}")
            return False

    def _export_mp3(self):
        if AudioSegment is None:
            print("pydub is not available for MP3 export.")
            return None, False
        if not self.filename:
            print("No filename specified for MP3 export.")
            return None, False
        try:
            wav_audio = AudioSegment.from_wav(self.filename)
            mp3_filename = self.filename.replace('.wav', f'_{random.randint(1000,9999)}.mp3')
            wav_audio.export(mp3_filename, format="mp3")
            return mp3_filename, True
        except Exception as e:
            print(f"Error exporting MP3: {e}")
            return None, False

    def _generate_filename(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.wav_dir, f"recording_{timestamp}.wav")

    def terminate(self):
        self.audio.terminate() 