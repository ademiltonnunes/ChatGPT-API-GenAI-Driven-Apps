function addLanguagesDropdown(){
//Languages Options
var languageOptions = ["English", "Spanish", "French", "Portuguese", "Chinese"];

//Adding Languages to dropdown box
var languageQuestionSelect = document.getElementById("languageQuestion");

languageOptions.forEach(function(language) {
    var option = document.createElement("option");
    option.text = language;
    option.value = language.toLowerCase();
    languageQuestionSelect.add(option);
});
}

function addProductsDropdown(){
    var productsSelect = document.getElementById("products");
    
    fetch('/updateProducts', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var productsOptions = data.products;

        productsOptions.forEach(function(product) {
            var option = document.createElement("option");
            option.text = product;
            option.value = product.toLowerCase();
            productsSelect.add(option);
        });
        productsSelect.selectedIndex = -1;
    })
    .catch(error => {
        alert('There was a problem with products:', error);
    });
}

function showLoaderForAnswer() {
    document.getElementById('loaderAnswer').style.display = 'flex';
}

function hideLoaderForAnswer() {
    document.getElementById('loaderAnswer').style.display = 'none';
}

function submitQuestion() {    
    var languageQuestionOption = document.getElementById("languageQuestion").value;
    var selectedProduct = document.getElementById("products").value;
    var questionTextarea = document.getElementById("question").value;
    var answerTextarea = document.getElementById("answer");

    if(selectedProduct == ''){
        alert("Select a product first!")
        return
    }

    if(questionTextarea == ""){
        alert("Ask a question first!")
        return
    }

    showLoaderForAnswer();    

    fetch('/submit_Question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            question: questionTextarea,
            product: selectedProduct,
            language: languageQuestionOption
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        answerTextarea.value = data.response;
        hideLoaderForAnswer();
    })
    .catch(error => {
        hideLoaderForAnswer();
        alert('There was a problem with the submit button:', error);
    });
    
}

//Call function to add languages to dropdwon
addLanguagesDropdown();
//Call function to add products to dropdwon
addProductsDropdown();
