// static/capture.js
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snapButton = document.getElementById('snap');
const imageDataInput = document.getElementById('imageData');
const form = document.getElementById('uploadForm');

// Get access to the camera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Error accessing camera: ", err);
  });

// On capture button click
snapButton.addEventListener('click', () => {
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataURL = canvas.toDataURL('image/png');
  imageDataInput.value = dataURL;
  form.submit();
});
