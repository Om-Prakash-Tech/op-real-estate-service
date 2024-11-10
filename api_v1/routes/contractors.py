from flask import Blueprint, request, jsonify
from config import contractors, transactions, projects
from datetime import datetime, timezone
from common.auth import token_required

contractors_blueprint = Blueprint('contractors', __name__)

@contractors_blueprint.route('', methods=['POST'])
@token_required
def create_contractor():
    try:
        data = request.get_json()
        data['createdAt'] = datetime.now(timezone.utc)
        data['updatedAt'] = datetime.now(timezone.utc)

        contractor_ref = contractors.document()
        contractor_id = contractor_ref.id
        data['contractorId'] = contractor_id

        contractor_ref.set(data)

        created_doc = contractor_ref.get().to_dict()
        return jsonify(created_doc), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contractors_blueprint.route('', methods=['GET'])
@token_required
def get_contractors():
    try:
        all_contractors = [doc.to_dict() for doc in contractors.stream()]
        return jsonify(all_contractors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contractors_blueprint.route('/<contractor_id>', methods=['GET'])
@token_required
def get_contractor(contractor_id):
    try:
        doc = contractors.document(contractor_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Contractor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contractors_blueprint.route('/<contractor_id>', methods=['PUT'])
@token_required
def update_contractor(contractor_id):
    try:
        data = request.get_json()
        data['updatedAt'] = datetime.now(timezone.utc)
        contractors.document(contractor_id).update(data)
        updated_doc = contractors.document(contractor_id).get().to_dict() 
        return jsonify(updated_doc), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contractors_blueprint.route('/<contractor_id>', methods=['DELETE'])
@token_required
def delete_contractor(contractor_id):
    try:
        # Check if there are any transactions with the given contractor ID
        transaction_refs = transactions.where('contractor', '==', contractor_id).stream()
        transaction_exists = any(True for _ in transaction_refs)
        if transaction_exists:
            return jsonify({"error": "All transactions for this contractor should be deleted first"}), 400

        # Update all projects where the contractors array contains the given contractor ID
        project_refs = projects.where('contractors', 'array_contains', contractor_id).stream()
        for project in project_refs:
            project_ref = projects.document(project.id)
            project_data = project.to_dict()
            if 'contractors' in project_data:
                project_data['contractors'] = [c for c in project_data['contractors'] if c != contractor_id]
                project_ref.update({'contractors': project_data['contractors']})

        # Delete the contractor
        doc_ref = contractors.document(contractor_id)
        deleted_doc = doc_ref.get().to_dict()
        if deleted_doc:
            doc_ref.delete()
            return jsonify(deleted_doc), 200
        else:
            return jsonify({"error": "Contractor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

