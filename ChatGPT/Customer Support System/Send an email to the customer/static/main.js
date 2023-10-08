function addLanguagesDropdown(){
//Languages Options
var languageOptions = ["English", "Spanish", "French", "Portuguese", "Chinese"];

//Adding Languages to dropdown boxes
var languageQuestionSelect = document.getElementById("languageQuestion");
var languageAnswerSelect = document.getElementById("languageAnswer");

languageOptions.forEach(function(language) {
    var option = document.createElement("option");
    option.text = language;
    option.value = language.toLowerCase(); // Use o valor em minúsculas como valor da opção
    languageQuestionSelect.add(option);
    
    // Clone language options to the second dropdown box
    languageAnswerSelect.add(option.cloneNode(true));
});
}

function showLoaderForQuestion() {
    document.getElementById('loaderQuestion').style.display = 'flex';
}

function hideLoaderForQuestion() {
    document.getElementById('loaderQuestion').style.display = 'none';
}

function showLoaderForAnswer() {
    document.getElementById('loaderAnswer').style.display = 'flex';
}

function hideLoaderForAnswer() {
    document.getElementById('loaderAnswer').style.display = 'none';
}

function showLoaderForEmail() {
    document.getElementById('loaderEmail').style.display = 'flex';
}

function hideLoaderForEmail() {
    document.getElementById('loaderEmail').style.display = 'none';
}

function updateLanguageQuestion() {
    showLoaderForQuestion();
    //Clean the Answer
    document.getElementById('answer').value = '';

    var languageQuestionOption = document.getElementById("languageQuestion").value;
    var questionTextarea = document.getElementById("question"); 

    // Send the selected language to server
    fetch('/updateQuestionLanguage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language_option: languageQuestionOption }),
    })
    .then(response => response.json())
    .then(data => {
        // Atualiza o textarea com a mensagem recebida do servidor
        questionTextarea.value = data.message;
        hideLoaderForQuestion();
    });
    
}

function submitQuestion() {
    showLoaderForAnswer();
    var languageAnswerOption = document.getElementById("languageAnswer").value;
    var questionTextarea = document.getElementById("question").value;
    var answerTextarea = document.getElementById("answer"); 

    fetch('/submit_Question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            comment: questionTextarea,
            language: languageAnswerOption
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        answerTextarea.value = data.message;
        hideLoaderForAnswer();
    })
    .catch(error => {
        hideLoaderForAnswer();
        alert('There was a problem with the submit button:', error);
    });
    
}

function send_email(){
    showLoaderForEmail();
    var senderEmail = document.getElementById("sender_email").value;
    var senderPassword = document.getElementById("sender_password").value;
    var recipientEmail = document.getElementById("recipient_email").value;
    var answerTextarea = document.getElementById("answer").value; 
    var comment = document.getElementById("question").value;
    var languageAnswerOption = document.getElementById("languageAnswer").value;

    if(answerTextarea == ""){
        alert("Submit email content first")
        return
    }

    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            senderEmail: senderEmail,
            senderPassword: senderPassword,
            recipientEmail: recipientEmail,
            answerTextarea: answerTextarea,
            comment: comment,
            language: languageAnswerOption
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        hideLoaderForEmail();
        alert("Email Sent Successfully!", data.message)
    })
    .catch(error => {
        hideLoaderForEmail();
        alert('There was a problem sending email:', error.error);
    });
}


//Call function to add languages to dropdwon
addLanguagesDropdown();
// Call function to show initial value
updateLanguageQuestion();