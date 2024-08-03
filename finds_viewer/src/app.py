import os
import logging
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template

from google.cloud import storage
from google.cloud import firestore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up Firestore collection
db = firestore.Client(project="history-research-assistant", database="history-research-database")
collection = db.collection('found-image-descriptions')

# Set up Google cloud storage
client = storage.Client()
bucket = client.bucket(os.environ["BUCKET_NAME"])

app = Flask(__name__)

def list_images():

    # Get the images and sort them by most recent.
    blobs = bucket.list_blobs()

    # Get the current time and the time 24 hours ago
    day_ago = datetime.now(timezone.utc) - timedelta(hours=24)

    blobs = [ b for b in blobs if b.content_type.startswith("image/") and b.time_created >= day_ago ]
    blobs = sorted(blobs, key=lambda x: x.time_created, reverse=True)

    # Get the content from Firestore
    hashes = [ b.metadata.get("sha256hash") for b in blobs ]
    content = [ collection.document(h).get().to_dict() for h in hashes ]
    
    # Generate input data for the template engine
    images = [{"url": b.public_url, 
               "source_url": d.get("source_url") if d else "",
               "title": d.get("title") if d else "", 
               "description": d.get("generated_description") if d else ""} for b,d in zip(blobs,content) ]

    return images

@app.route('/')
def home():

    # Generate content
    images = list_images()
    current_date = datetime.now().strftime("%B %d, %Y")

    # Render the page
    return render_template('index.html', images=images, current_date=current_date)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
