import os
import sys
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from langchain.llms import Ollama
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QFileDialog

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    full_text = ""
    with sr.AudioFile(audio_path) as source:
        # Split audio into chunks to improve transcription accuracy
        audio_duration = source.DURATION
        chunk_duration = 30  # seconds
        for i in range(0, int(audio_duration), chunk_duration):
            audio = recognizer.record(source, duration=chunk_duration)
            try:
                chunk_text = recognizer.recognize_google(audio)
                full_text += chunk_text + " "
            except sr.UnknownValueError:
                print(f"Could not understand audio in chunk starting at {i} seconds")
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service; {e}")
    return full_text.strip()

def summarize_text(text, video_title):
    llm = Ollama(model="llama3")
    prompt = f"""
    The following text is a transcription of a video titled "{video_title}".
    Please provide a detailed description of the key points discussed in the video, based on this transcription:

    {text}

    Summary:
    """
    summary = llm(prompt)
    return summary

def main(video_path):
    audio_path = "extracted_audio.wav"
    video_title = os.path.basename(video_path)
    
    print("Extracting audio...")
    extract_audio(video_path, audio_path)
    
    print("Transcribing audio...")
    text = transcribe_audio(audio_path)
    
    print("Summarizing text...")
    summary = summarize_text(text, video_title)
    
    os.remove(audio_path)
    
    return summary

class VideoSummaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Video Summary App')
        
        self.videoLabel = QLabel('Video Path:')
        self.videoPath = QLineEdit(self)
        self.browseButton = QPushButton('Browse', self)
        self.browseButton.clicked.connect(self.browseFile)
        
        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.startProcess)
        
        self.summaryLabel = QLabel('Summary:')
        self.summaryText = QTextEdit(self)
        self.summaryText.setReadOnly(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.videoLabel)
        layout.addWidget(self.videoPath)
        layout.addWidget(self.browseButton)
        layout.addWidget(self.startButton)
        layout.addWidget(self.summaryLabel)
        layout.addWidget(self.summaryText)
        
        self.setLayout(layout)
    
    def browseFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '', 'Video Files (*.mp4 *.avi *.mov)')
        if file_path:
            self.videoPath.setText(file_path)
    
    def startProcess(self):
        video_path = self.videoPath.text()
        if video_path:
            summary = main(video_path)
            self.summaryText.setPlainText(summary)
        else:
            self.summaryText.setPlainText("Please select a video file first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoSummaryApp()
    ex.show()
    sys.exit(app.exec_())
