import boto3
import os
from dotenv import load_dotenv

# Cloudflare R2 Configuration
load_dotenv()

# Initialize S3-Compatible Client
session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    endpoint_url=os.environ["R2_ENDPOINT_URL"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY"],
    aws_secret_access_key=os.environ["R2_SECRET_KEY"]
)

def upload_file_to_r2(file_path, object_key):
    """Uploads an image to Cloudflare R2 with public read access"""
    try:
        s3_client.upload_file(
            file_path, 
            os.environ["R2_BUCKET_NAME"], 
            object_key,
            ExtraArgs={"ACL": "public-read"}  # Ensures public access
        )
        public_url = f"{os.environ["R2_PUBLIC_URL"]}{object_key}"
        print(f"✅ Image uploaded successfully!\nPublic URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Upload failed: {e}")


if __name__ == "__main__":
    # Example Usage
    file_path = "simple.png"  # Replace with your image file
    object_key = f"uploads/{os.path.basename(file_path)}"  # Organize in 'uploads' folder
    upload_file_to_r2(file_path, object_key)
