import boto3
from flask import Flask,request,jsonify,render_template

server = Flask(__name__)

s3 = boto3.client('s3')

@server.route("/")
def index():
    return render_template('index.html')

@server.route('/upload',methods=['POST'])
def upload_file():
    BUCKET_NAME = request.args.get('name')

    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return "File uploaded successfully"
    except NoCredentialsError:
        return "Credentials not available"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000, debug=True)