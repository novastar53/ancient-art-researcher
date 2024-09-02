import os
import random
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template

from google.cloud import storage
from google.cloud import firestore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

# Set up Firestore collection
db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"), database=os.getenv("FIRESTORE_DATABASE"))
collection = db.collection(os.getenv("FIRESTORE_IMAGE_COLLECTION"))

# Set up Google cloud storage
client = storage.Client()
bucket = client.bucket(os.getenv("BUCKET_NAME"))

app = Flask(__name__)

def get_random_finds(n=8):

    # Get the images and sort them by most recent.
    blobs = bucket.list_blobs()

    blobs = [ b for b in blobs if b.content_type.startswith("image/") ]

    # pick n random images
    blobs = random.sample(blobs, n)

    # Get the content from Firestore
    hashes = [ b.metadata.get("sha256hash") for b in blobs ]
    content = [ collection.document(h).get().to_dict() for h in hashes ]
    
    # Generate input data for the template engine
    images = [{"url": b.public_url, 
               "source_url": d.get("source_url") if d else "",
               "title": d.get("title") if d else "", 
               "description": d.get("generated_description") if d else ""} for b,d in zip(blobs,content) ]

    return images



def get_recent_finds():

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
    images = get_random_finds(8)
    current_date = datetime.now().strftime("%B %d, %Y")

    # Render the page
    return render_template('index.html', images=images, title="")

@app.route('/latest')
def latest():
    # Generate content
    images = get_recent_finds()
    current_date = datetime.now().strftime("%B %d, %Y")
    title = f"Latest Finds on {current_date}"

    # Render the page
    return render_template('latest.html', images=images, title=title)

@app.route('/gridview')
def grid():
    # Generate content
    images = get_random_finds(8)
    current_date = datetime.now().strftime("%B %d, %Y")
    return render_template('gridview.html', images=images, title="")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
