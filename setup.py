import os
import subprocess

# Create index.html file
index_html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Caption Generator</title>
</head>
<body>
    <h1>Image Caption Generator</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
        <input type="file" name="image">
        <input type="submit" value="Generate Caption">
    </form>
    {% if caption %}
    <h2>Generated Caption:</h2>
    <p>{{ caption }}</p>
    {% if generation_message %}
    <p>{{ generation_message }}</p>
    {% endif %}
    {% endif %}
</body>
</html>
"""

with open('index.html', 'w') as index_file:
    index_file.write(index_html_content)

# Create app.py file
app_py_content = """
from flask import Flask, request, jsonify
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import time

app = Flask(__name__)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

last_generation_time = None  # Variable to store the time of the last caption generation

def generate_caption(image):
    global last_generation_time

    if not image:
        return "No image uploaded"

    try:
        with Image.open(image) as img:
            raw_image = img.convert("RGB")

            # Unconditional image captioning
            inputs = processor(raw_image, return_tensors="pt", max_length=100)  # Set max length to 100

            start_time = time.time()  # Record the start time
            out = model.generate(**inputs)
            end_time = time.time()  # Record the end time

            last_generation_time = end_time - start_time  # Calculate generation time
            caption = processor.decode(out[0], skip_special_tokens=True)

            return caption
    except Exception as e:
        return f"Error processing image: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_generation_time

    caption = ""
    generation_message = ""

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            caption = generate_caption(image)
            generation_message = f"Caption generated in {last_generation_time:.2f} seconds."

    # Read index.html content from the same directory
    with open('index.html', 'r') as index_file:
        index_html = index_file.read()

    return index_html.replace('{{ caption }}', caption).replace('{{ generation_message }}', generation_message)

@app.route('/api/generate_caption', methods=['POST'])
def generate_caption_api():
    if 'image' in request.files:
        image = request.files['image']
        caption = generate_caption(image)
        image_name = image.filename

        response = {
            'image_name': image_name,
            'description': caption
        }

        return jsonify(response)
    else:
        return jsonify({'error': 'No image uploaded'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

with open('app.py', 'w') as app_file:
    app_file.write(app_py_content)

# Install required packages
subprocess.run(['pip', 'install', 'Flask', 'Pillow', 'requests', 'transformers', 'torch', 'torchvision', 'torchaudio'])

# Run app.py
os.system('python app.py')
