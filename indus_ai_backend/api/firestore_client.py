import os
from google.cloud import firestore
from google.oauth2 import service_account
from django.conf import settings
import dotenv
from pathlib import Path
import logging

# Load environment variables
dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')

# Set up logging
logger = logging.getLogger('firestore_client')

try:
    # Initialize credentials
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    
    # Initialize Firestore client with production settings
    db = firestore.Client(
        project=getattr(settings, 'FIRESTORE_PROJECT_ID', os.getenv('FIRESTORE_PROJECT_ID')),
        credentials=credentials
    )
    
    logger.info("Firestore client initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize Firestore client: {e}")
    raise
