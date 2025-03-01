from astrapy import DataAPIClient
from dotenv import load_dotenv
import os

# Load AstraDB Credentials
load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = "https://b3332883-e9fa-4c4f-bccc-75558d0faf64-us-east-2.apps.astra.datastax.com"

client = DataAPIClient(token=ASTRA_DB_APPLICATION_TOKEN)

# Initialize AstraDB connection
db = client.get_database_by_api_endpoint(ASTRA_DB_API_ENDPOINT)
print(f"Connected to Astra DB: {db.list_collection_names()}")
