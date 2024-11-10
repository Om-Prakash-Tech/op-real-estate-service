from flask import Blueprint, request, jsonify
from config import transactions
from datetime import datetime, timezone
from dateutil import parser
from common.auth import token_required
from common.validators import validate_str, validate_int
from common.constants import UNVERIFIED, VERIFIED, get_contractor_data, get_project_data

transactions_blueprint = Blueprint('transactions', __name__)

def validate_transaction_data(data):
    if not validate_str(data.get('contractor')):
        return False, "Contractor ID is required and must be a valid string."
    if not validate_int(data.get('transactionAmount')):
        return False, "Paid amount is required and must be a valid integer."
    if data.get('project') and not get_project_data(data.get('project')):
        return False, "Project ID does not exist."
    if not get_contractor_data(data.get('contractor')):
        return False, "Contractor ID does not exist."
    return True, ""

def derive_status(signature):
    return VERIFIED if signature else UNVERIFIED

@transactions_blueprint.route('', methods=['POST'])
@token_required
def create_transaction():
    try:
        data = request.get_json()
        is_valid, message = validate_transaction_data(data)
        if not is_valid:
            return jsonify({"error": message}), 400

        data['status'] = derive_status(data.get('signature'))
        data['transactionDate'] = parser.parse(data['transactionDate'])
        data['createdAt'] = datetime.now(timezone.utc)
        data['updatedAt'] = datetime.now(timezone.utc)

        transaction_ref = transactions.document()
        transaction_id = transaction_ref.id
        data['transactionId'] = transaction_id

        transaction_ref.set(data)

        created_doc = transaction_ref.get().to_dict()
        
        # Add project and contractor data
        created_doc['project'] = get_project_data(created_doc['project'])
        created_doc['contractor'] = get_contractor_data(created_doc['contractor'])
        
        return jsonify(created_doc), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_blueprint.route('', methods=['GET'])
@token_required
def get_transactions():
    try:
        transactions_list = []
        for doc in transactions.stream():
            transaction = doc.to_dict()
            transaction['project'] = get_project_data(transaction['project'])
            transaction['contractor'] = get_contractor_data(transaction['contractor'])
            transactions_list.append(transaction)
        return jsonify(transactions_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_blueprint.route('/<transaction_id>', methods=['GET'])
@token_required
def get_transaction(transaction_id):
    try:
        doc = transactions.document(transaction_id).get()
        if doc.exists:
            transaction = doc.to_dict()
            transaction['project'] = get_project_data(transaction['project'])
            transaction['contractor'] = get_contractor_data(transaction['contractor'])
            return jsonify(transaction), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_blueprint.route('/<transaction_id>', methods=['PUT'])
@token_required
def update_transaction(transaction_id):
    try:
        data = request.get_json()
        is_valid, message = validate_transaction_data(data)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        data['status'] = derive_status(data.get('signature'))
        data['updatedAt'] = datetime.now(timezone.utc)
        transactions.document(transaction_id).update(data)
        updated_doc = transactions.document(transaction_id).get().to_dict()
        
        # Add project and contractor data
        updated_doc['project'] = get_project_data(updated_doc['project'])
        updated_doc['contractor'] = get_contractor_data(updated_doc['contractor'])
        
        return jsonify(updated_doc), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_blueprint.route('/<transaction_id>', methods=['DELETE'])
@token_required
def delete_transaction(transaction_id):
    try:
        doc_ref = transactions.document(transaction_id)
        deleted_doc = doc_ref.get().to_dict()
        if deleted_doc:
            doc_ref.delete()
            deleted_doc['project'] = get_project_data(deleted_doc['project'])
            deleted_doc['contractor'] = get_contractor_data(deleted_doc['contractor'])
            return jsonify(deleted_doc), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
