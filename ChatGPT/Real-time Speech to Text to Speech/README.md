# Real-time Speech to Text to Speech: Building Your AI-Based Alexa
## Overview
This project aims to implement a AI-Based “Alexa”, which is the possibility of speaking with ChatGPT with voice using Whisper and Google Text to Speech (GTTS).
The system was built in Python and used the ChatGPT OpenAI text-davinci-002 model.
Please, read the pdf file CS589_week6_q5_19679_AdemiltonMarcelo_DaCruzNunes.pdf. It will have all steps taken to develop this project.

## Implementation Steps

To run this application, follow these implementation steps:

### 1. Create a Virtual Environment

```bash
python3 -m venv venv bash
```

### 2. Activate the virtual environment:
```bash
. venv/bin/activate
```

### 3.Install the required Python packages:
```bash
pip show pydub 
pip install pydub
pip install SpeechRecognition
pip install openai-whisper
pip install gtts
pip install openai
pip install pyaudio
sudo apt update && sudo apt install ffmpeg
```
