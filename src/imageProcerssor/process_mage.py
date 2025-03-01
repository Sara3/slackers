import openai
import requests
import json
import os
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def download_image(image_url):
    """Downloads an image from a URL."""
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("❌ Error: Failed to download image.")
        return None


def analyze_image(image_path):
    """Sends an image to OpenAI CLIP model for object detection."""
    with open(image_path, "rb") as image_file:
        response = openai.Image.create(
            model="clip",  # Ensure the correct OpenAI vision model is used
            image=image_file.read()
        )
    return response["data"]


def generate_excalidraw_json(objects):
    """Converts OpenAI's detected objects into Excalidraw JSON format."""
    elements = []

    for obj in objects:
        # Simulating coordinates since OpenAI CLIP doesn’t return bounding boxes
        elements.append({
            "type": "rectangle" if "box" in obj["label"] else "text",
            "x": len(elements) * 100,  # Simulated X position
            "y": len(elements) * 50,   # Simulated Y position
            "text": obj["label"] if obj["label"] == "text" else ""
        })

    return json.dumps({"elements": elements}, indent=4)


def process_image(image_input):
    """Processes an image and returns Excalidraw JSON."""
    if image_input.startswith("http"):
        image = download_image(image_input)
        if image:
            image_path = "temp_image.jpg"
            image.save(image_path)
        else:
            return None
    else:
        image_path = image_input  # Assume it's a local file

    detected_objects = analyze_image(image_path)
    excalidraw_json = generate_excalidraw_json(detected_objects)

    print("\n✅ **Excalidraw JSON Output:**")
    print(excalidraw_json)
    return excalidraw_json


# Example Usage
if __name__ == "__main__":
    # Replace with actual image URL
    image_url = "https://your-image-url-here.com/image.jpg"
    process_image(image_url)
