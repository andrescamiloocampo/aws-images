import boto3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
s3 = boto3.client('s3', region_name='us-east-1')  

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    BUCKET_NAME = 'andres-ocampo-test-bucket'
    
    if not BUCKET_NAME:
        return 'Bucket name is required', 400

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return "File uploaded successfully", 200    
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
