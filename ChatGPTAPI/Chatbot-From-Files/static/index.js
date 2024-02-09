let mediaRecorder;

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
    // Ask question and the desired answer
    fetch('/submit_Question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            question: question, 
            includeAudio: includeAudio
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

function createOutGoingMessage(message, audio_file = null) {
    // Create a new div structure for the entire message block
    var divStructure = document.createElement('div');
    divStructure.classList.add('outgoing-chats');

    // Create a flex container for the message and the icon
    var flexContainer = document.createElement('div');
    flexContainer.classList.add('outgoing-flex-container','justify-content-end'); 

    // Create container for the message
    var messageContainer = document.createElement('div');
    messageContainer.classList.add('outgoing-chats-msg');

    var paragraph = document.createElement('p');
    paragraph.classList.add('multi-msg');
    paragraph.textContent = message;
    messageContainer.appendChild(paragraph);

    // If audio, append it to the message container
    if (audio_file != null) {
        var audio = document.createElement('audio');
        audio.classList.add('multi-msg');
        audio.controls = true;
        var blobUrl = URL.createObjectURL(audio_file);
        audio.src = blobUrl;
        messageContainer.appendChild(audio);
    }

    // Append message container to the flex container
    flexContainer.appendChild(messageContainer);

    // Create and append the user icon to the flex container
    var userIcon = document.createElement('img');
    userIcon.src = "static/user.png"; // Adjust the path as necessary
    userIcon.alt = "User";
    userIcon.classList.add('user-icon'); // Ensure you define this class in your CSS
    flexContainer.appendChild(userIcon); 

    // Append the flex container to the main div structure
    divStructure.appendChild(flexContainer);

    // Get the output container
    var outputContainer = document.getElementById('conversation');

    // Append the div structure to the output container
    outputContainer.appendChild(divStructure);
}


function createReceivedMessage(answer, audio_file = null) {
    // Create a new div structure
    var divStructure = document.createElement('div');
    divStructure.classList.add('received-chats');

    var receivedMsg = document.createElement('div');
    receivedMsg.classList.add('received-chats-img');

    // Add bot image
    var botImage = document.createElement('img');
    botImage.src = "static/SFBU-logo.png";
    botImage.alt = "Bot";
    botImage.classList.add('bot-img'); // Ensure you define 'bot-img' class in your CSS
    receivedMsg.appendChild(botImage);

    var receivedChatsMsg = document.createElement('div');
    receivedChatsMsg.classList.add('received-msg-inbox');

    var paragraph = document.createElement('p');
    paragraph.textContent = answer;

    // Append the paragraphs to the div structure
    receivedChatsMsg.appendChild(paragraph);

    // If audio
    if (audio_file != null) {
        var audio = document.createElement('audio');
        audio.controls = true;

        // Create a blob URL for the audio
        var blobUrl = URL.createObjectURL(audio_file);
        audio.src = blobUrl;

        // Append the audio element to the div structure
        receivedChatsMsg.appendChild(audio);
    }

    // Putting in the structure
    receivedMsg.appendChild(receivedChatsMsg);
    divStructure.appendChild(receivedMsg);

    // Get the output container
    var outputContainer = document.getElementById('conversation');

    // Append the div structure to the output container
    outputContainer.appendChild(divStructure);
}


function showLoaderAnswering() {
    // Create a temporary div to show the typing indicator
    var typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.classList.add('received-chats');

    var receivedMsg = document.createElement('div');
    receivedMsg.classList.add('received-chats-img');

    // Add bot image for typing indicator (you can use a different image or style)
    var botImage = document.createElement('img');
    botImage.src = "static/SFBU-logo.png"; // Replace with the correct path to your bot image
    botImage.alt = "Bot";
    botImage.classList.add('bot-img'); // Ensure you define 'bot-img' class in your CSS
    receivedMsg.appendChild(botImage);

    var typingContent = document.createElement('div');
    typingContent.classList.add('received-msg-inbox');

    var paragraph = document.createElement('p');
    paragraph.textContent = 'Typing...';

    // Append the content to the div
    typingContent.appendChild(paragraph);
    receivedMsg.appendChild(typingContent);
    typingDiv.appendChild(receivedMsg);

    // Append the typing indicator to the conversation area
    var conversationArea = document.getElementById('conversation');
    conversationArea.appendChild(typingDiv);

    // Optionally, scroll to the bottom of the chat
    conversationArea.scrollTop = conversationArea.scrollHeight;
}


function hideLoaderAnswering() {
    // Remove the typing indicator
    var typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Update other functions where showLoaderAnswering and hideLoaderAnswering are called


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
function displayGreetingMessage() {
    const greetingMessage = "Hello, I'm your virtual assistant. I help you chat with your files in format PDF, URL, and Youtube Videos. Feel free to ask any questions in English or your preferred language. You can also use the microphone button for audio questions, but please note that audio questions should be in English.";
    createReceivedMessage(greetingMessage);
}

document.addEventListener('DOMContentLoaded', (event) => {
    displayGreetingMessage();
});

window.addEventListener('beforeunload', function() {
    fetch('/update_page', {
        method: 'GET'
    });
});