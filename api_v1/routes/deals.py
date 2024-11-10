from flask import Blueprint, request, jsonify
from common.constants import DEAL_TYPES
from config import deals
from datetime import datetime, timezone
from dateutil import parser
from common.auth import token_required
from common.validators import validate_str, validate_int

deals_blueprint = Blueprint('deals', __name__)

def validate_deal_data(data):
    if not validate_str(data.get('name')):
        return False, "Name is required and must be a valid string."
    if not validate_str(data.get('projectName')):
        return False, "Project Name is required and must be a valid string."
    if not validate_str(data.get('dealType')) or data.get('dealType') not in DEAL_TYPES:
        return False, "Deal Type is required and must be either 'buy' or 'sell'."
    if not validate_int(data.get('transactionAmount')):
        return False, "Transaction Amount is required and must be a valid integer."
    if not validate_int(data.get('dealAmount')):
        return False, "Deal Amount is required and must be a valid integer."
    return True, ""

@deals_blueprint.route('', methods=['POST'])
@token_required
def create_deal():
    try:
        data = request.get_json()
        is_valid, message = validate_deal_data(data)
        if not is_valid:
            return jsonify({"error": message}), 400

        data['transactionDate'] = parser.parse(data['transactionDate'])
        data['createdAt'] = datetime.now(timezone.utc)
        data['updatedAt'] = datetime.now(timezone.utc)

        deal_ref = deals.document()
        deal_id = deal_ref.id
        data['dealId'] = deal_id

        deal_ref.set(data)

        created_doc = deal_ref.get().to_dict()
        
        return jsonify(created_doc), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@deals_blueprint.route('', methods=['GET'])
@token_required
def get_deals():
    try:
        deals_list = [doc.to_dict() for doc in deals.stream()]
        return jsonify(deals_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@deals_blueprint.route('/<deal_id>', methods=['GET'])
@token_required
def get_deal(deal_id):
    try:
        doc = deals.document(deal_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Deal not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@deals_blueprint.route('/<deal_id>', methods=['PUT'])
@token_required
def update_deal(deal_id):
    try:
        data = request.get_json()
        is_valid, message = validate_deal_data(data)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        data['updatedAt'] = datetime.now(timezone.utc)
        deals.document(deal_id).update(data)
        updated_doc = deals.document(deal_id).get().to_dict()
        
        return jsonify(updated_doc), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@deals_blueprint.route('/<deal_id>', methods=['DELETE'])
@token_required
def delete_deal(deal_id):
    try:
        doc_ref = deals.document(deal_id)
        deleted_doc = doc_ref.get().to_dict()
        if deleted_doc:
            doc_ref.delete()
            return jsonify(deleted_doc), 200
        else:
            return jsonify({"error": "Deal not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
