from flask import Blueprint, request, jsonify
from config import projects, transactions
from datetime import datetime, timezone
from dateutil import parser
from common.auth import token_required

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route('', methods=['POST'])
@token_required
def create_project():
    try:
        data = request.get_json()
        
        data['dueDate'] = parser.parse(data['dueDate'])
        data['createdAt'] = datetime.now(timezone.utc)
        data['updatedAt'] = datetime.now(timezone.utc)

        project_ref = projects.document()
        project_id = project_ref.id
        data['projectId'] = project_id

        project_ref.set(data)

        created_doc = project_ref.get().to_dict()
        return jsonify(created_doc), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@projects_blueprint.route('', methods=['GET'])
@token_required
def get_projects():
    try:
        projects_list = [doc.to_dict() for doc in projects.stream()]
        return jsonify(projects_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@projects_blueprint.route('/<project_id>', methods=['GET'])
@token_required
def get_project(project_id):
    try:
        doc = projects.document(project_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@projects_blueprint.route('/<project_id>', methods=['PUT'])
@token_required
def update_project(project_id):
    try:
        data = request.get_json()
        data['updatedAt'] = datetime.now(timezone.utc)
        projects.document(project_id).update(data)
        updated_doc = projects.document(project_id).get().to_dict()
        return jsonify(updated_doc), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@projects_blueprint.route('/<project_id>', methods=['DELETE'])
@token_required
def delete_project(project_id):
    try:
        doc_ref = projects.document(project_id)
        deleted_doc = doc_ref.get().to_dict()
        if deleted_doc:
            doc_ref.delete()
            transaction_refs = transactions.where('project', '==', project_id).stream() 
            for transaction in transaction_refs: 
                transaction_ref = transactions.document(transaction.id)
                transaction_ref.update({"project": None})
            return jsonify(deleted_doc), 200
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
