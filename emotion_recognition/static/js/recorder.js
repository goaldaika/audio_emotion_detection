const audioElement = document.querySelector('#recorder');
const recorder = new MediaRecorder(audioElement.srcObject);

document.querySelector('#start-recording').addEventListener('click', () => {
    recorder.start();
});

document.querySelector('#stop-recording').addEventListener('click', () => {
    recorder.stop();
});

recorder.ondataavailable = event => {
    const audioBlob = event.data;
    const formData = new FormData();
    formData.append('audio_file', audioBlob);

    fetch('/emotion_recognition/', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('There was an error processing the request');
        }
    }).then(data => {
        // Update the page with the emotion labels returned by the server
        const emotionList = document.querySelector('#emotion-list');
        data.forEach(emotion => {
            const li = document.createElement('li');
            li.textContent = emotion;
            emotionList.appendChild(li);
        });
    }).catch(error => {
        console.error(error);
    });
};
