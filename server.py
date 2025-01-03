from flask import Flask, render_template, request, jsonify
from process import process_image
from classify import classify_image
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


@app.route('/data', methods=['POST'])
def data():
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


@app.route('/classify', methods=['POST'])
def classify():
    """
    API endpoint to return predictions in JSON format.
    Expects an image file to be uploaded as part of the request.
    """
    if request.files:
        file_image = request.files.get('image')
        if file_image:
            data = classify_image(file_image)
            return jsonify(data=data)  
    return jsonify({"error": "No image file provided"}), 400

@app.route('/process', methods=['POST'])
def process():
    """
    API endpoint to return predictions in JSON format.
    Expects an image file to be uploaded as part of the request.
    """
    if request.files:
        file_image = request.files.get('image')
        if file_image:
            data = process_image(file_image)
            type = classify_image(file_image)
            data['type_invoice'] = type
            return jsonify(data=data)  
    return jsonify({"error": "No image file provided"}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

