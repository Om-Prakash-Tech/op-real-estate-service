import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV')

cred = credentials.Certificate('real-estate-firebase-adminsdk.json')
initialize_app(cred)

db = firestore.client()
transactions = db.collection('transactions')
projects = db.collection('projects')
contractors = db.collection('contractors')
deals = db.collection('deals')