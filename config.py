import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
import json
load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV')
service_account_info = json.loads(os.getenv('SERVICE_ACCOUNT_KEY'))
print('real-estate-firebase-adminsdk.json' if FLASK_ENV == 'localhost' else service_account_info)
cred = credentials.Certificate('real-estate-firebase-adminsdk.json' if FLASK_ENV == 'localhost' else service_account_info)
initialize_app(cred)

db = firestore.client()
transactions = db.collection('transactions')
projects = db.collection('projects')
contractors = db.collection('contractors')
deals = db.collection('deals')