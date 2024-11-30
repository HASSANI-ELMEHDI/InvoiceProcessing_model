from flask import Flask, render_template, request, jsonify
from utils import process_image

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def predict():
    """
    API endpoint to return predictions in JSON format.
    Expects an image file to be uploaded as part of the request.
    """
    if request.files:
        file_image = request.files.get('image')
        if file_image:
            data = process_image(file_image)
            return jsonify(data=data)  
    return jsonify({"error": "No image file provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)
