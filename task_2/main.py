from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

s3_client = boto3.client('s3',region_name='us-east-1')
rekognition_client = boto3.client('rekognition',region_name='us-east-1')

@app.route('/analyze', methods=['GET'])
def analyze_image():
    image_name = request.args.get('image_name')
    bucket_name = request.args.get('bucket_name')

    if not image_name or not bucket_name:
        return jsonify({'error': 'Se deben proporcionar el nombre de la imagen y el bucket'}), 400

    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image_name
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )

    labels = response['Labels']
    return jsonify([(label['Name'], label['Confidence']) for label in labels])

if __name__ == '__main__':
    app.run(debug=True)
