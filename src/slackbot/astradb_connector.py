import os
import base64
import hashlib
from astrapy.db import AstraDB
from dotenv import load_dotenv

# Load AstraDB Credentials
load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = "https://b3332883-e9fa-4c4f-bccc-75558d0faf64-us-east-2.apps.astra.datastax.com"
COLLECTION_NAME = "slacker_images"

# ✅ Initialize AstraDB connection
db = AstraDB(token=ASTRA_DB_APPLICATION_TOKEN, api_endpoint=ASTRA_DB_API_ENDPOINT)

def generate_image_id(image_path):
    """Generate a SHA-256 hash for the image as a unique identifier."""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return hashlib.sha256(image_data).hexdigest()

def upload_image_to_astra(image_path):
    """Upload an image to AstraDB by converting it to Base64."""
    collections = db.get_collections()
    actual_collections = collections.get("status", {}).get("collections", [])
    print("✅ Available Collections:", actual_collections)  # Debugging Step
    collection = db.collection(COLLECTION_NAME)

    if collection is None:
        raise ValueError(f"❌ Cannot find collection: '{COLLECTION_NAME}' in AstraDB")

    # Generate unique image ID
    image_id = generate_image_id(image_path)

    # Read and encode image as Base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Insert image into AstraDB
    document = {
        "image_id": image_id,
        "filename": os.path.basename(image_path),
        "image_data": image_data
    }
    
    collection.insert_one(document)
    print(f"✅ Image '{image_path}' uploaded to AstraDB with ID: {image_id}")

    return image_id

# 🔹 Example Usage
if __name__ == "__main__":
    image_path = "simple.png"  # Change this to your image file
    upload_image_to_astra(image_path)
