import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from google.oauth2 import service_account
import base64
import json
load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV')
service_key_b64 = os.getenv('SERVICE_ACCOUNT_KEY')

service_key_json = base64.b64decode(service_key_b64).decode('utf-8')
service_account_info = json.loads(service_key_json)

cred = service_account.Credentials.from_service_account_info(service_account_info)
# cred = credentials.Certificate('real-estate-firebase-adminsdk.json')
initialize_app(cred)

db = firestore.client()
transactions = db.collection('transactions')
projects = db.collection('projects')
contractors = db.collection('contractors')
deals = db.collection('deals')