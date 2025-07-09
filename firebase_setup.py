from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from os import environ

load_dotenv()  # ✅ Load envs from .env file


# Set up credentials using environment variables
secrets = {
    "type": "service_account",
    "project_id": environ.get("PROJECT_ID", "uiux-123"),
    "private_key_id": environ.get("PRIVATE_KEY_ID"),
    "private_key": environ.get("PRIVATE_KEY").replace('\\n', '\n'),  # Make sure to fix newline formatting
    "client_email": environ.get("CLIENT_EMAIL"),
    "client_id": environ.get("CLIENT_ID"),
    "auth_uri": environ.get("AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": environ.get("TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": environ.get("AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": environ.get("CLIENT_X509_CERT_URL", "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40uiux-123.iam.gserviceaccount.com"),
    "universe_domain": "googleapis.com"
}

# Log project ID for confirmation
# print("Using environment variables for Firebase credentials")
# print("PROJECT_ID:", secrets["project_id"])

# Initialize Firebase
cred = credentials.Certificate(secrets)
app = firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
