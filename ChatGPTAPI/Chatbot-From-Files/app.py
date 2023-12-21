from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from vector_and_embedding import LangChaing
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/pdf'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lc = LangChaing()

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
            return jsonify({'status': 'error', 'message': "NO PDFs to ask questions"})
        response = {'status': 'success', 'message': f'{pdf_to_delete} deleted successfully.'}
    except FileNotFoundError:
        response = {'status': 'error', 'message': 'File not found.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)
