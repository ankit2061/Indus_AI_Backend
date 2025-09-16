import os
from google.cloud import firestore
from google.oauth2 import service_account
from django.conf import settings
import dotenv
from pathlib import Path

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')

credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

db = firestore.Client(project=settings.FIRESTORE_PROJECT_ID, credentials=credentials)

# print("Firestore Project ID:", os.getenv('FIRESTORE_PROJECT_ID'))
# print("Credentials File:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
