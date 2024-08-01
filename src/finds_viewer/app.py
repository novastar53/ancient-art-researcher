import os
from datetime import datetime

from flask import Flask, render_template
from google.cloud import storage

# Configure your Google Cloud Storage bucket name


app = Flask(__name__)

# Function to list all image URLs in the Google Cloud Storage bucket
def list_images():
    client = storage.Client()
    bucket = client.bucket(os.environ["BUCKET_NAME"])
    blobs = bucket.list_blobs()

    image_urls = []
    for blob in blobs:
        if blob.content_type.startswith('image/'):
            image_urls.append(blob.public_url)
    
    return image_urls

@app.route('/')
def home():

    images = list_images()
    current_date = datetime.now().strftime("%B %d, %Y")

    return render_template('index.html', images=images, current_date=current_date)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
