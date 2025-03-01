from flask import Flask, request, jsonify
import requests
import json
import os
import openai
from io import BytesIO
from PIL import Image
from unstructured.partition.text import partition_text

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key")
# Change to deployed Langflow API if needed
langflow_url = os.getenv(
    "LANGFLOW_API_URL", "http://localhost:7860/api/v1/predict")

app = Flask(__name__)


def send_to_langflow(image_url):
    """
    Sends the image to Langflow for automated processing.
    Langflow will:
    1. Download the image.
    2. Process it using OpenAI CLIP.
    3. Extract text via Unstructured.io.
    4. Return Excalidraw JSON.
    """
    payload = {
        "image_url": image_url
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(langflow_url, json=payload, headers=headers)
        response_data = response.json()
        return response_data.get("excalidraw_json", {})
    except requests.exceptions.RequestException as e:
        return {"error": f"Langflow request failed: {str(e)}"}


@app.route("/process-image", methods=["POST"])
def process_image():
    """Processes an image via Langflow and returns Excalidraw JSON."""
    data = request.json
    image_url = data.get("file_url")

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    # Send image to Langflow for processing
    excalidraw_json = send_to_langflow(image_url)

    # Print JSON to console for debugging
    print("Generated Excalidraw JSON:", json.dumps(excalidraw_json, indent=4))

    return jsonify({"excalidraw_json": excalidraw_json})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
