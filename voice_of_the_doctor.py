# from dotenv import load_dotenv
# load_dotenv()
from pydub import AudioSegment 
import os
import subprocess
from playsound import playsound 
import platform
from gtts import gTTS

# def text_to_speech_with_gtts(input_text, output_filepath):
#     temp_mp3 = "temp_gtts.mp3"
#     language = "en"  # Handles Hinglish well

#     # Generate MP3 with gTTS
#     audioobj = gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(temp_mp3)

#     # Convert MP3 to WAV using pydub
#     sound = AudioSegment.from_mp3(temp_mp3)
#     sound.export(output_filepath, format="wav")

#     # Clean up temp file
#     os.remove(temp_mp3)

#     return output_filepath


import os
import time

def text_to_speech_with_gtts(input_text, output_filepath="final.mp3"):
    try:
        # Safety check for empty or whitespace input
        if not input_text or not input_text.strip():
            raise ValueError("Input text for TTS is empty.")

        # Remove old file if it exists
        if os.path.exists(output_filepath):
            os.remove(output_filepath)

        # Generate and save the TTS output
        tts = gTTS(text=input_text.strip(), lang="en", slow=False)
        tts.save(output_filepath)

        # Wait briefly to ensure file is fully written
        time.sleep(0.5)

        # Confirm file exists and has content
        if not os.path.exists(output_filepath):
            raise FileNotFoundError(f"{output_filepath} was not created.")
        if os.path.getsize(output_filepath) == 0:
            raise IOError(f"{output_filepath} is empty after TTS generation.")

        print(f"[TTS] Audio file saved successfully to {output_filepath}")

    except Exception as e:
        print(f"[TTS ERROR] {e}")


input_text="Hi this is MediBot, autoplay testing chal raha hai!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.wav")
