# 🩺 Multimodal Medical Chatbot

A lightweight multimodal medical assistant chatbot that takes in **audio** and optionally **image inputs** to answer health-related queries using the **Meta LLaMA 4 (Scout 17B Instruct)** model via the **Groq API**. The bot transcribes spoken input using **Whisper**, optionally processes visual symptoms (e.g., acne, rashes, injuries), and generates informative, voice-based responses using **gTTS** — all inside a simple, user-friendly **Gradio** interface.

---

## 🚀 Features

- 🎙️ **Audio Input**: Users can ask health-related questions via microphone. The query is transcribed using OpenAI’s `Whisper` model.
- 🖼️ **Optional Image Input**: Images can be uploaded to assist with visually observable symptoms (e.g., acne, hair loss, skin conditions).
- 🧠 **Groq + Meta LLaMA Integration**: Processes both transcription and image via `llama-4-scout-17b-16e-instruct` for fast, accurate, and helpful medical responses.
- 🔊 **Voice-Based Output**: Responses are converted back to speech using `gTTS` and played aloud.
- 💡 **Gradio UI**: Simple and interactive web interface for seamless user experience.

---

## 🧰 Tech Stack

- `Python`
- `Gradio`
- `Whisper` (for transcription)
- `gTTS` (for text-to-speech)
- `Groq API` (for LLaMA-4 Scout inference)
- `Docker` (for containerization)
- `Google Cloud Platform (GCP)` – with full **CI/CD deployment via Cloud Build triggers**

---

## 🐳 Deployment

This project supports two forms of deployment:

1. **Manual Docker Deployment**  
   The app is containerized using Docker and pushed to Google Artifact Registry, then deployed to **Cloud Run** manually.

2. **CI/CD via GitHub + GCP Cloud Build**  
   Code changes pushed to GitHub automatically trigger Cloud Build pipelines which:
   - Build Docker image
   - Push to Artifact Registry
   - Deploy latest version to Cloud Run

Secrets such as the `GROQ_API_KEY` are securely managed using **Google Secret Manager**.

---

## 🛠️ Setup & Installation

1. **Clone the Repo**

```bash
git clone https://github.com/neerajmanhar/multimodal-medibot.git
cd multimodal-medibot
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Environment Variables**

Ensure you have a `.env` file or set the required API key directly:

```env
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run Locally**

```bash
python gradio_app.py
```

5. **Build Docker Image (Optional)**

```bash
docker build -t multimodal-medibot .
```

6. **Deploy to Cloud Run (Manual Method)**

```bash
gcloud run deploy medi-bot-app \
  --image=asia-south1-docker.pkg.dev/medibot-cicd/medi-bot-repo/medi-bot-app:latest \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --set-secrets=GROQ_API_KEY=GROQ_API_KEY:latest
```

---

## 🔒 Security

- **Secret Management**: API keys and tokens are stored in **Google Secret Manager** and injected securely during deployment.
- **Safe Uploads**: Image and audio files are processed in-memory and discarded post-inference.

---

## 📸 Demo

> [🌐 View Live Demo](https://medi-bot-app-122859879070.asia-south1.run.app/)  

---

## 👨‍💻 Author

**Neeraj Manhar**  
[GitHub](https://github.com/neerajmanhar) • [LinkedIn](https://linkedin.com/in/neerajmanhar)


---

## 📜 License

MIT License. Feel free to use and extend with attribution.

