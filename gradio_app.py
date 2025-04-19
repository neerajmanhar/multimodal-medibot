# from dotenv import load_dotenv
# load_dotenv()

import os
import time
import gradio as gr
from gtts import gTTS

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").replace("\n", "").replace("\r", "").strip()
headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

from brain_of_the_doctor import encode_image, analyze_image_with_query, analyze_without_image
from voice_of_the_patient import transcribe_with_groq

# Text-to-speech function
def text_to_speech_with_gtts(input_text, output_filepath="final.mp3"):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath)
    time.sleep(1)  # Ensure file is fully written

# System prompt for the doctor
system_prompt = """
You are acting as a professional, empathetic doctor for a healthcare chatbot designed to assist patients in rural or remote areas. 
Based on the image (if provided) and the patient's spoken description, respond as if you are speaking directly to the patient.

Structure your response as follows:

1. Assessment: Provide a brief and human-like summary of what you think the condition might be, based on visible symptoms or described issues. Use plain, friendly language. Avoid AI-style phrases like "the image shows..." — instead, say things like "It looks like you might be experiencing..."

2. Home Remedies: If appropriate, suggest simple and safe home remedies using easily available ingredients. Make sure to include only culturally acceptable and medically sound suggestions.

3. Over-the-Counter Medicines: Mention any relevant medicines that might help, but keep the list minimal and easy to understand. DO NOT prescribe prescription-only drugs. Use generic names where possible.

4. Caution: Always end with a disclaimer like — "Please consult a certified medical professional before starting any medicine. This response is for educational purposes only."

Instructions:
- Do not use special characters or numbered lists in your output.
- Keep the response short, around 4–6 sentences total.
- Speak like a real doctor talking to a patient, not like an AI model.
"""

# Main pipeline
def gradio_pipeline(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=GROQ_API_KEY,
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    query = system_prompt + speech_to_text_output

    if image_filepath:
        encoded_img = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=query,
            encoded_image=encoded_img,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = analyze_without_image(
            query=query,
            model="llama-3.3-70b-versatile"
        )

    audio_path = "final.mp3"
    text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath=audio_path
    )

    return speech_to_text_output, doctor_response, audio_path

# Gradio UI
with gr.Blocks(title="AI Doctor with Vision and Voice") as iface:
    gr.Markdown("## 🩺 Speak to the Doctor and Upload an Image")

    audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Record Your Symptoms")
    image_input = gr.Image(type="filepath", label="📸 Upload Medical Image (Optional)")

    submit_btn = gr.Button("🩻 Analyze")

    stt_output = gr.Textbox(label="🗣️ Transcribed Speech")
    doc_output = gr.Textbox(label="👨‍⚕️ Doctor's Response")
    audio_output = gr.Audio(label="🔊 Doctor's Voice", type="filepath", autoplay=True)

    submit_btn.click(
        fn=gradio_pipeline,
        inputs=[audio_input, image_input],
        outputs=[stt_output, doc_output, audio_output]
    )

iface.launch(server_name="0.0.0.0", server_port=8080)


