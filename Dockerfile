# Use an official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for PyAudio and other packages, and alsa-utils for playing audio
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    python3-gi \
    gir1.2-gtk-3.0 \
    portaudio19-dev \
    alsa-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all project files except what's excluded by .dockerignore
COPY . .

# Expose Gradio port
EXPOSE 8080

# Run the Gradio app
CMD ["python", "gradio_app.py"]
