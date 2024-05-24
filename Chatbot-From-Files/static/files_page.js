load_upload_pdf();
loadUploadUrl();
loadUploadYoutube();

function uploadPDF(){
    showLoaderUploadingFile();
    var pdfInput = document.getElementById('pdfInput');
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
            console.log('File uploaded successfully\nSaved as: ' + data.filename);
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

            // // Create the clickable "x" image
            // const deleteIcon = document.createElement('img');
            // deleteIcon.src = 'static/delete.png';
            // deleteIcon.alt = 'Delete';
            // deleteIcon.className = 'delete-icon';
            // deleteIcon.style.width = '0.2in';
            // deleteIcon.style.height = 'auto';

            // // Attach a click event listener to the "x" image
            // deleteIcon.addEventListener('click', function() {
            //     // Call your function when the "x" is clicked
            //     deleteItem(pdfFile);
            // });

            // // Append the "x" image to the list item
            // listItem.appendChild(deleteIcon);

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
        if(data.error){
            load_upload_pdf();
            hideLoaderUploadingFile();
            alert(data.error);
            return;
        }
        console.log(data.message);
        load_upload_pdf();
        hideLoaderUploadingFile();
    })
    .catch(error => {        
        alert('Error deleting PDF:', error.message);
        load_upload_pdf();
        hideLoaderUploadingFile();
    });

    
}

function uploadUrl(){
    showLoaderUploadingFile();
    var urlInput = document.getElementById('urlInput');
    var url = urlInput.value;
    urlInput.value = "";

    if (!isValidURL(url)) {
        hideLoaderUploadingFile();
        alert('Invalid URL! Please enter a valid URL.');
        return;
    }

    fetch('/upload_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            url: url
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.error){
            loadUploadUrl();
            hideLoaderUploadingFile();
            alert(data.error);

            return;
        }
        loadUploadUrl();
        hideLoaderUploadingFile();
        console.log(data.message);
        
    })
    .catch(error => {  
        loadUploadUrl();
        hideLoaderAnswering();
        alert('There was a problem uploading url: ' + error);         
    });
}

function isValidURL(url) {
    try {
        const parsedURL = new URL(url);
        return parsedURL.protocol === 'http:' || parsedURL.protocol === 'https:';
    } catch (error) {
        return false;
    }
}

function loadUploadUrl(){
    const urlList = document.getElementById('url-list');

    fetch('/urls')
    .then(response => response.json())
    .then(urlLinks => {
        // Clear all items from the list
        urlList.innerHTML = '';

        // Populate the list with new items
        urlLinks.forEach((url, index) => {
            const link = document.createElement('a');
            link.href = url;
            link.target = '_blank';
            link.textContent = `${url}`;

            const listItem = document.createElement('li');
            listItem.textContent = `URL ${index + 1}:`;
            listItem.appendChild(link);                

            // // Create the clickable "x" image
            // const deleteIcon = document.createElement('img');
            // deleteIcon.src = 'static/delete.png';
            // deleteIcon.alt = 'Delete';
            // deleteIcon.className = 'delete-icon';
            // deleteIcon.style.width = '0.2in';
            // deleteIcon.style.height = 'auto';

            // // Attach a click event listener to the "x" image
            // deleteIcon.addEventListener('click', function() {
            //     // Call your function when the "x" is clicked
            //     deleteUrlItem(url);
            // });

            // // Append the "x" image to the list item
            // listItem.appendChild(deleteIcon);

            // Append the list item to the list
            urlList.appendChild(listItem);
        });

    })
    .catch(error => alert('Error fetching URLs:', error));

}

function deleteUrlItem(url){
    showLoaderUploadingFile();   
    fetch('/delete_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            urlToDelete: url
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error){
            loadUploadUrl();
            hideLoaderUploadingFile();
            alert(data.error);
            return;
        }
        console.log(data.message);
        loadUploadUrl();
        hideLoaderUploadingFile();
    })
    .catch(error => {        
        alert('Error deleting URL:', error.message);
        loadUploadUrl();
        hideLoaderUploadingFile();
    });
}

function uploadYoutube(){
    showLoaderUploadingFile();
    var youtubeInput = document.getElementById('youtubeInput');
    var youtube = youtubeInput.value;
    youtubeInput.value = "";

    if (!isValidYoutubeURL(youtube)) {
        hideLoaderUploadingFile();
        alert('Invalid Youtube Link! Please enter a valid link.');
        return;
    }

    fetch('/upload_youtube', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            youtube: youtube
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.error){
            hideLoaderUploadingFile();
            loadUploadYoutube();
            alert(data.error);
            return;
        }
        loadUploadYoutube();
        hideLoaderUploadingFile();
        console.log(data.message);
        
    })
    .catch(error => {  
        loadUploadYoutube();
        hideLoaderAnswering();
        alert('There was a problem uploading youtube link: ' + error);         
    });
}

function isValidYoutubeURL(url) {
    var pattern = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|v\/|playlist\?list=)|youtu\.be\/)/;
    return pattern.test(url);
}

function loadUploadYoutube(){
    const youtubeList = document.getElementById('youtube-list');

    fetch('/youtubes')
    .then(response => response.json())
    .then(youtubeLinks => {
        // Clear all items from the list
        youtubeList.innerHTML = '';

        // Populate the list with new items
        youtubeLinks.forEach((youtube, index) => {
            const link = document.createElement('a');
            link.href = youtube;
            link.target = '_blank';
            link.textContent = `${youtube}`;

            const listItem = document.createElement('li');
            listItem.textContent = `URL ${index + 1}:`;   
            listItem.appendChild(link);          

            // // Create the clickable "x" image
            // const deleteIcon = document.createElement('img');
            // deleteIcon.src = 'static/delete.png';
            // deleteIcon.alt = 'Delete';
            // deleteIcon.className = 'delete-icon';
            // deleteIcon.style.width = '0.2in';
            // deleteIcon.style.height = 'auto';

            // // Attach a click event listener to the "x" image
            // deleteIcon.addEventListener('click', function() {
            //     // Call your function when the "x" is clicked
            //     deleteYoutubeItem(youtube);
            // });

            // // Append the "x" image to the list item
            // listItem.appendChild(deleteIcon);

            // Append the list item to the list
            youtubeList.appendChild(listItem);
        });

    })
    .catch(error => alert('Error fetching URLs:', error));

}

function deleteYoutubeItem(youtube){
    showLoaderUploadingFile();

    fetch('/delete_youtube', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            youtubeToDelete: youtube
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error){
            loadUploadYoutube();
            hideLoaderUploadingFile();
            alert(data.error);
            return;
        }
        console.log(data.message);
        loadUploadYoutube();
        hideLoaderUploadingFile();
    })
    .catch(error => {        
        alert('Error deleting URL:', error.message);
        loadUploadYoutube();
        hideLoaderUploadingFile();
    });
}

function showLoaderUploadingFile() {
    document.getElementById('loaderUpload').style.display = 'flex';
}

function hideLoaderUploadingFile() {
    document.getElementById('loaderUpload').style.display = 'none';
}

