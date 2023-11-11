from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from vector_and_embedding import LangChaing
from speechRecognation import SpeechRecognation
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/pdf'
AUDIO_FOLDER = 'audios/mp3'
REPLY_FOLDER = 'audios/reply'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['REPLY_FOLDER'] = REPLY_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_AUDIO = {'mp3', 'wav'}

lc = LangChaing()
sr = SpeechRecognation()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/submit_Question', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        question = data.get('question')

        #Ask question
        response = lc.chat(question) 
        print(response)

        answer = response['answer']

        return jsonify({'response': answer})
    except Exception as e:
        
        print(f"Unexpected Error: {e}")
        return jsonify({'error': f"Can't answer questions: {e}"})

@app.route('/upload_pdf', methods=['POST'])
def upload_file():
    try:      

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file uploaded'})

        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            count = 0
            while os.path.exists(file_path):
                filename = secure_filename(
                    file.filename.rsplit('.', 1)[0] + f'_{count}.{file.filename.rsplit(".", 1)[1].lower()}')
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                count += 1
            
            if count> 0:
                return jsonify({'error': 'This file was been uploaded already!'})

            file.save(file_path)

            #Create a vectorstore
            created = lc.upload_file(UPLOAD_FOLDER)

            if created == False:
                return jsonify({'error': "It wasn't possible to use this PDF to ask questions"})

            return jsonify({'response': True, 'message': 'File uploaded successfully', 'filename': filename})

        return jsonify({'error': 'Invalid file format'})
    except Exception as e:
        
        print(f"Unexpected Error: {e}")
        return jsonify({'error': f"It wasn't possible to use this PDF to ask questions: {e}"})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pdfs')
def get_pdfs():
    pdf_directory = UPLOAD_FOLDER
    try:
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    except FileNotFoundError:
        # If the directory is not found, return an empty list
        pdf_files = []
    return jsonify(pdf_files)

@app.route('/delete_pdf', methods=['POST'])
def delete_pdf():
    data = request.get_json()
    pdf_to_delete = data.get('pdfToDelete')

    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_to_delete)
    
    try:
        os.remove(pdf_path)

        #Create a vectorstore
        created = lc.upload_file(UPLOAD_FOLDER)
        
        if created == False:
            return jsonify({'status': 'error', 'message': "NO content to ask questions"})
        
        response = {'status': 'success', 'message': f'{pdf_to_delete} deleted successfully.'}
    except FileNotFoundError:
        response = {'status': 'error', 'message': 'File not found.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        audio_file = request.files.get('audio', None)

        # Check if an audio file was received
        if audio_file is None:
            return jsonify({'error': 'No audio file received'}), 400

        # Check if the file has a valid extension
        if not allowed_audio_file(audio_file.filename):
            return jsonify({'error': 'Invalid audio file type'}), 400

        # Save audio file
        if not os.path.exists(app.config['AUDIO_FOLDER']):
            os.makedirs(app.config['AUDIO_FOLDER'])

        audio_path = os.path.join(app.config['AUDIO_FOLDER'], 'audio.mp3')
        audio_file.save(audio_path)

        #Change audio to text
        transciption = sr.transcribe_audio(audio_path)

        return jsonify({'transcription': transciption})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO

@app.route('/get_question_audio', methods=['POST'])
def get_audio():
    try:

        data = request.get_json()
        # Get the audio text
        text = data.get('text')

        if text:
            # Changing Text to audio
            audio = sr.text_to_audio(text)

            # Create directory if it doesn't exist
            if not os.path.exists(app.config['REPLY_FOLDER']):
                os.makedirs(app.config['REPLY_FOLDER'])

            # Audio Path
            audio_path = os.path.join(app.config['REPLY_FOLDER'], 'reply.mp3')
            
            # Save audio
            audio.save(audio_path)

            # Return the audio file for download
            return send_file(audio_path, as_attachment=True)
        else:
            return jsonify({'error': 'No text provided to transform into audio'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5555)