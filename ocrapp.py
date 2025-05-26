import os
from flask import Flask, request, render_template
from PIL import Image, ImageEnhance
import pytesseract
import base64
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.form['imageData']
    header, encoded = data_url.split(',', 1)
    image_data = base64.b64decode(encoded)

    image = Image.open(BytesIO(image_data)).convert('RGB')

    # Enhance image for better OCR
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = image.convert('L')

    # Extract text
    text = pytesseract.image_to_string(image)

    # Render result
    return f"""
    <html>
    <head><title>OCR Result</title></head>
    <body>
        <h2>Extracted Text:</h2>
        <div id="ocr-text" style="white-space: pre-wrap; border:1px solid #ccc; padding:10px;">{text}</div>
        <br>
        <button onclick="speakText()">🔊 Read Aloud</button>
        <br><br>
        <a href="/">⬅️ Back</a>

        <script>
        function speakText() {{
            const text = document.getElementById('ocr-text').innerText;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.rate = 1.0;
            speechSynthesis.speak(utterance);
        }}
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
