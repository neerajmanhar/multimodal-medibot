import logging
# from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
# load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # 🔧 Raise threshold to ignore minor background noise
            recognizer.energy_threshold += 100  # Try 100–200 for starters

            recognizer.pause_threshold = 4

            logging.info(f"Energy threshold set to: {recognizer.energy_threshold}")
            logging.info("Start speaking now...")
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        
audio_filepath="patient_voice_test.mp3"
# record_audio(file_path=audio_filepath)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()

stt_model="whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client=Groq(api_key=GROQ_API_KEY)
    
    audio_file=open(audio_filepath, "rb")
    transcription=client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
        
    )

    return transcription.text