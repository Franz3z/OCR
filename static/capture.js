const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const imageDataField = document.getElementById('imageData');
const uploadForm = document.getElementById('uploadForm');

// Get camera stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        alert("Camera access denied or not available: " + err);
    });

// Capture image and send to server
snap.addEventListener("click", () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataURL = canvas.toDataURL('image/png');
    imageDataField.value = imageDataURL;
    uploadForm.submit();
});
