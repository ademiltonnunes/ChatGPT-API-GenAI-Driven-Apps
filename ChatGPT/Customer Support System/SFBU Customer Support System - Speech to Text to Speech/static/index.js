let mediaRecorder;
load_upload_pdf();

function handleKeyDown(event) {
    if (event.key === "Enter") {        
        submitQuestion();
    }
}

function submitQuestion() {
    // Get the input text
    var inputQuestion = document.getElementById('inputQuestion').value;

    // Validate that the input field is not empty
    if (inputQuestion.trim() === '') {
        alert('Please ask a question before!.');
        return;
    }

    // Create message
    createOutGoingMessage(inputQuestion);

    // Clear the input field for the next entry
    document.getElementById('inputQuestion').value = '';
    
    //Ask Question
    askQuestion(inputQuestion);
}

function askQuestion(question, includeAudio = false){
    showLoaderAnswering();

    // Ask question
    fetch('/submit_Question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            question: question
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        answer = data.response;   
        if (answer === "" || typeof answer === 'undefined') {
            alert("There is an error answering the question");
            hideLoaderAnswering(); 
            return;
        }
        if (includeAudio){
            getAudioFromServer(answer)
            .then(audio => {

                // Response with audio
                createReceivedMessage(answer, audio);
                hideLoaderAnswering();
            })
            .catch(error => {
                console.error('Error getting audio:', error);
                hideLoaderAnswering();
            });
        }else {
            // Response
            createReceivedMessage(answer); 
            hideLoaderAnswering(); 
        }           
    })
    .catch(error => {  
        alert('There was a problem asking question: ' + error);
        hideLoaderAnswering(); 
    });   
}

function createOutGoingMessage(message, audio_file= null){
    // Create a new div structure
    var divStructure = document.createElement('div');
    divStructure.classList.add('outgoing-chats');

    var outgoingMsg = document.createElement('div');
    outgoingMsg.classList.add('outgoing-msg');

    var outgoingChatsMsg = document.createElement('div');
    outgoingChatsMsg.classList.add('outgoing-chats-msg');

    var paragraph = document.createElement('p');
    paragraph.classList.add('multi-msg');
    paragraph.textContent = message;

    // Append the paragraph to the div structure
    outgoingChatsMsg.appendChild(paragraph);

    //If audio
    if (audio_file != null){
        var audio = document.createElement('audio');
        audio.classList.add('multi-msg');
        audio.controls = true;

        // Create a blob URL for the audio
        var blobUrl = URL.createObjectURL(audio_file);
        audio.src = blobUrl;

        // Append the audio element to the div structure
        outgoingChatsMsg.appendChild(audio);
    }

    //Putting in the structure
    outgoingMsg.appendChild(outgoingChatsMsg);
    divStructure.appendChild(outgoingMsg);

    // Get the output container
    var outputContainer = document.getElementById('conversation');

    // Append the div structure to the output container
    outputContainer.appendChild(divStructure);
}

function createReceivedMessage(answer, audio_file= null){
    // Create a new div structure
    var divStructure = document.createElement('div');
    divStructure.classList.add('received-chats');

    var receivedMsg = document.createElement('div');
    receivedMsg.classList.add('received-chats-img');

    var receivedChatsMsg = document.createElement('div');
    receivedChatsMsg.classList.add('received-msg-inbox');

    var paragraph = document.createElement('p');
    paragraph.textContent = answer;    

    // Append the paragraphs to the div structure
    receivedChatsMsg.appendChild(paragraph); 
    
    //if audio
    if (audio_file != null){
        var audio = document.createElement('audio');
        audio.controls = true;

        // Create a blob URL for the audio
        var blobUrl = URL.createObjectURL(audio_file);
        audio.src = blobUrl;

        // Append the audio element to the div structure
        receivedMsg.appendChild(audio);
    
    }

    //Putting in the structure
    receivedMsg.appendChild(receivedChatsMsg);
    divStructure.appendChild(receivedMsg);

    // Get the output container
    var outputContainer = document.getElementById('conversation');

    // Append the div structure to the output container
    outputContainer.appendChild(divStructure);
}

function uploadPDF(){
    showLoaderUploadingFile();
    var pdfInput = document.getElementById('pdInput');
    if (pdfInput.files.length <= 0) {
        alert('Please, select a file before uploading it');
        hideLoaderUploadingFile();
        return
    }
    var file = pdfInput.files[0];

    var formData = new FormData();
    formData.append('file', file);

    fetch('/upload_pdf', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            alert('File uploaded successfully\nSaved as: ' + data.filename);
        } else {
            alert('Error: ' + data.error);
        }
        pdfInput.value = '';
        load_upload_pdf();
        hideLoaderUploadingFile();
    })
    .catch(error => {
        console.error('Error:', error);  
        alert('An unexpected error while uploading file');
        pdfInput.value = '';
        load_upload_pdf();
        hideLoaderUploadingFile();
    });
}

function load_upload_pdf(){
    const pdfList = document.getElementById('pdf-list');

    fetch('/pdfs')
            .then(response => response.json())
            .then(pdfFiles => {
                // Clear all items from the list
                pdfList.innerHTML = '';
                
                // Populate the list with new items
                pdfFiles.forEach((pdfFile, index) => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `PDF ${index + 1}: ${pdfFile}`;             

                    // Create the clickable "x" image
                    const deleteIcon = document.createElement('img');
                    deleteIcon.src = 'static/delete.png';
                    deleteIcon.alt = 'Delete';
                    deleteIcon.className = 'delete-icon';
                    deleteIcon.style.width = '0.2in';
                    deleteIcon.style.height = 'auto';

                    // Attach a click event listener to the "x" image
                    deleteIcon.addEventListener('click', function() {
                        // Call your function when the "x" is clicked
                        deleteItem(pdfFile);
                    });

                    // Append the "x" image to the list item
                    listItem.appendChild(deleteIcon);

                    // Append the list item to the list
                    pdfList.appendChild(listItem);
                });
            })
            .catch(error => alert('Error fetching PDFs:', error));
}

function deleteItem(pdfFile) {
    showLoaderUploadingFile();   
    fetch('/delete_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pdfToDelete: pdfFile,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        load_upload_pdf();
        hideLoaderUploadingFile();
    })
    .catch(error => {        
        alert('Error deleting PDF:', error.message);
        load_upload_pdf();
        hideLoaderUploadingFile();
    });

    
}

function showLoaderUploadingFile() {
    document.getElementById('loaderUpload').style.display = 'flex';
}

function showLoaderAnswering() {
    document.getElementById('loaderAnswerQuestion').style.display = 'flex';
}

function hideLoaderUploadingFile() {
    document.getElementById('loaderUpload').style.display = 'none';
}

function hideLoaderAnswering() {
    document.getElementById('loaderAnswerQuestion').style.display = 'none';
}

async  function startRecording() {
    const startRecordingButton = document.getElementById('startRecordingButton');
    const stopRecordingButton = document.getElementById('stopRecordingButton');

    let audioChunks = [];    

    // Getting user permission to access the microphone
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaRecorder = new MediaRecorder(stream);

            //Change buttons
            startRecordingButton.style.display = 'none';
            stopRecordingButton.style.display = 'inline-block';
            console.log('Recording started...');

            mediaRecorder.start();

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                // Send `audioBlob` to server
                sendAudioToServer(audioBlob);
                // Clear mediaRecorder
                mediaRecorder = null;                
            };
        })
        .catch((error) => {
            alert('Error accessing microphone:', error);
            console.error('Error accessing microphone:', error);
        });
}

function stopRecording() {
    const startRecordingButton = document.getElementById('startRecordingButton');
    const stopRecordingButton = document.getElementById('stopRecordingButton');

    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        startRecordingButton.style.display = 'inline-block';
        stopRecordingButton.style.display =  'none';
        console.log('Recording stopped...');
    }
}

function sendAudioToServer(audioBlob) {
    showLoaderAnswering();

    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.mp3');

    fetch('/upload-audio', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error sending audio to server: ' + data.error);
            hideLoaderAnswering();
        } 
        else if (data.transcription == null){
            alert("It wasn't possible to transcribe audio");
            hideLoaderAnswering();
        }
        else{
            question = data.transcription;

            // Create message
            createOutGoingMessage(question, audioBlob);
            hideLoaderAnswering();

            // Ask Question
            askQuestion(question, includeAudio = true);
        }           
    })
    .catch(error => {
        alert('Error sending audio to server:', error);
        hideLoaderAnswering();
    });
}

function getAudioFromServer(text) {
    return fetch('/get_question_audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok getting server audio');
        }
        return response.blob();
    })
    .catch(error => {
        console.error('Error fetching audio:', error);
        throw error;
    });
}

