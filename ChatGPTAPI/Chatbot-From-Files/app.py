from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from vector_and_embedding import LangChaing
from speechRecognation import SpeechRecognation
from llm_Response import LLMResponse
from webCrawling import Crawl
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/pdf'
UPLOAD_URL = 'uploads/url'
UPLOAD_YOUTUBE = 'uploads/youtube'
AUDIO_FOLDER = 'audios/mp3'
REPLY_FOLDER = 'audios/reply'
url_file_name = "url.txt"
youtube_file_name = "youtube.txt"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_URL'] = UPLOAD_URL
app.config['UPLOAD_YOUTUBE'] = UPLOAD_YOUTUBE
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['REPLY_FOLDER'] = REPLY_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_AUDIO = {'mp3', 'wav'}

lc = LangChaing()
sr = SpeechRecognation()
llm = LLMResponse()
c = Crawl()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/files_page')
def files_page():
    return render_template('files_page.html')

@app.route('/submit_Question', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        question = data.get('question')
        includeAudio = data.get('includeAudio')

        # Pass the user email to the chat method
        response = llm.chat(question, includeAudio)
        answer = response['answer']

        return jsonify({'response': answer})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'error': f"Can't answer questions: {e}"})

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:      

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file uploaded'})

        if file and allowed_file(file.filename):

            #Create directory if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #Verify if the file exists
            count = 0
            while os.path.exists(file_path):
                filename = secure_filename(
                    file.filename.rsplit('.', 1)[0] + f'_{count}.{file.filename.rsplit(".", 1)[1].lower()}')
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                count += 1
            
            if count> 0:
                return jsonify({'error': 'This file was been uploaded already!'})

            #Save pdf file
            file.save(file_path)

            #Create a vectorstore
            created = lc.upload_pdf(file_path)

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
    pdf_directory = app.config['UPLOAD_FOLDER']
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

        #Create vectorstore with remaining files 
        lc.upload_all_files()     

        response = {'message': f'{pdf_to_delete} deleted successfully.'}
    except FileNotFoundError:
        response = {'error': 'File not found.'}
    except Exception as e:
        response = {'error': str(e)}

    return jsonify(response)

@app.route('/upload_url', methods=['POST'])
def upload_url(file_name = url_file_name, webCrawling = False):
    try:     
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'No url uploaded'})

        if not os.path.exists(app.config['UPLOAD_URL']):
            os.makedirs(app.config['UPLOAD_URL'])
        
        file_path = os.path.join(app.config['UPLOAD_URL'], file_name)

        # Check if the URL is already in the file
        with open(file_path, 'a+') as file:
            file.seek(0)
            existing_urls = [line.strip() for line in file.readlines()]

        if url in existing_urls:
            return jsonify({'error': 'URL already exists'})
        
        if webCrawling:                
            # Create a vectorstore
            c.crawling(url)
        else:        
            #Load url and save it to vectorstore
            lc.upload_url(url, timer= False) 
        
        # Save the URL to the file
        with open(file_path, 'a') as file:
            file.write(url + '\n') 

        return jsonify({'message': f'Url uploaded successfully url: {url}'})
    except Exception as e:        
        print(f"Unexpected Error: {e}")
        return jsonify({'error': f"It wasn't possible to use this URL to ask questions: {e}"})

@app.route('/urls', methods=['GET'])
def get_urls(file_name = url_file_name):  
    try:
        file_path = os.path.join(app.config['UPLOAD_URL'], file_name)
        with open(file_path, 'r') as file:
            url_links = [line.strip() for line in file.readlines()]    
    except FileNotFoundError:
        # If the directory is not found, return an empty list
        url_links = []
    return jsonify(url_links)

@app.route('/delete_url', methods=['POST'])
def delete_url(file_name = url_file_name):
    data = request.get_json()
    url_to_delete = data.get('urlToDelete')

    try:
        file_path = os.path.join(app.config['UPLOAD_URL'], file_name)

        # Check if the URL is already in the file
        with open(file_path, 'r') as file:
            existing_urls = [line.strip() for line in file.readlines()]
        
        if url_to_delete in existing_urls:
            existing_urls.remove(url_to_delete)

            # Write the updated list back to the file
            with open(file_path, 'w') as file:
                file.write('\n'.join(existing_urls))
            
            #Create vectorstore with remaining files  
            lc.upload_all_files() 

            return jsonify({'message': 'URL deleted successfully'})
        else: 
            return jsonify({'error': 'URL not found'})
    except FileNotFoundError:
        return jsonify({'error': 'URL not found.'})
    except Exception as e:
         return jsonify({'error': str(e)})

@app.route('/upload_youtube', methods=['POST'])
def upload_youtube(file_name = youtube_file_name):
    try:     
        data = request.get_json()
        youtube = data.get('youtube')

        if not youtube:
            return jsonify({'error': 'No youtube link uploaded'})

        if not os.path.exists(app.config['UPLOAD_YOUTUBE']):
            os.makedirs(app.config['UPLOAD_YOUTUBE'])
        
        file_path = os.path.join(app.config['UPLOAD_YOUTUBE'], file_name)

        # Check if the URL is already in the file
        with open(file_path, 'a+') as file:
            file.seek(0)
            existing_youtubes = [line.strip() for line in file.readlines()]

        if youtube in existing_youtubes:
            return jsonify({'error': 'Youtube link already exists'})
        
        #Create a vectorstore
        created = lc.upload_youtube(youtube) 

        if created == False:
            return jsonify({'error': "It wasn't possible to use this url to ask questions"})

        # Save the URL to the file
        with open(file_path, 'a') as file:
            file.write(youtube + '\n')  

        return jsonify({'message': f'Youtube link uploaded successfully: {youtube}'})
    except Exception as e:        
        print(f"Unexpected Error: {e}")
        return jsonify({'error': f"It wasn't possible to use this Youtube link to ask questions: {e}"})

@app.route('/youtubes', methods=['GET'])
def get_youtubes(file_name = youtube_file_name):  
    try:
        file_path = os.path.join(app.config['UPLOAD_YOUTUBE'], file_name)
        with open(file_path, 'r') as file:
            youtube_links = [line.strip() for line in file.readlines()]    
    except FileNotFoundError:
        # If the directory is not found, return an empty list
        youtube_links = []
    return jsonify(youtube_links)

@app.route('/delete_youtube', methods=['POST'])
def delete_youtube(file_name = youtube_file_name):
    data = request.get_json()
    youtube_to_delete = data.get('youtubeToDelete')

    try:
        file_path = os.path.join(app.config['UPLOAD_YOUTUBE'], file_name)

        # Check if the URL is already in the file
        with open(file_path, 'r') as file:
            existing_urls = [line.strip() for line in file.readlines()]
        
        if youtube_to_delete in existing_urls:
            existing_urls.remove(youtube_to_delete)

            # Write the updated list back to the file
            with open(file_path, 'w') as file:
                file.write('\n'.join(existing_urls))
            
            #Create vectorstore with remaining files  
            lc.upload_all_files() 

            return jsonify({'message': 'Youtube video deleted successfully'})
        else: 
            return jsonify({'error': 'Youtube video not found'})
    except FileNotFoundError:
        return jsonify({'error': 'Youtube video not found.'})
    except Exception as e:
         return jsonify({'error': str(e)})

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

@app.route('/update_page', methods=['GET'])
def update_page():
    #Removing chat from the memory
    llm.chatbot = None
    return jsonify({'message': 'Update Page'})
 
if __name__ == '__main__':
    app.run(debug=True, port=5555)