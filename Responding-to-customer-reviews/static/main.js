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

//Call function to add languages to dropdwon
addLanguagesDropdown();
// Call function to show initial value
updateLanguageQuestion();