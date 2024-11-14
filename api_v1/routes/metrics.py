from flask import Blueprint, jsonify
from common.constants import get_contractor_data, get_project_data
from config import transactions, projects
from common.auth import token_required

metrics_blueprint = Blueprint('metrics', __name__)

@metrics_blueprint.route('/transactions/project/<project_id>', methods=['GET'])
@token_required
def get_transactions_by_project_id(project_id):
    try:
        transactions_list = []
        for doc in transactions.where('project', '==', project_id).stream():
            transaction = doc.to_dict()
            transaction['project'] = get_project_data(transaction['project'])
            transaction['contractor'] = get_contractor_data(transaction['contractor'])
            transactions_list.append(transaction)
        return jsonify(transactions_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@metrics_blueprint.route('/transactions/contractor/<contractor_id>', methods=['GET'])
@token_required
def get_transactions_by_contractor_id(contractor_id):
    try:
        transactions_list = []
        for doc in transactions.where('contractor', '==', contractor_id).stream():
            transaction = doc.to_dict()
            transaction['project'] = get_project_data(transaction['project'])
            transaction['contractor'] = get_contractor_data(transaction['contractor'])
            transactions_list.append(transaction)
        return jsonify(transactions_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@metrics_blueprint.route('/contractors/project/<project_id>', methods=['GET'])
@token_required
def get_contractors_by_project_id(project_id):
    try:
        project_doc = projects.document(project_id).get()
        if not project_doc.exists:
            return jsonify({"error": "Project not found"}), 404

        project_data = project_doc.to_dict()
        contractors_list = []
        for contractor_id in project_data.get('contractors', []):
            contractor = get_contractor_data(contractor_id)
            if contractor:
                contractors_list.append(contractor)
        return jsonify(contractors_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@metrics_blueprint.route('/projects/contractor/<contractor_id>', methods=['GET'])
@token_required
def get_projects_by_contractor_id(contractor_id):
    try:
        projects_list = []
        for project_doc in projects.stream():
            project_data = project_doc.to_dict()
            if contractor_id in project_data.get('contractors', []):
                project = {
                    "projectId": project_doc.id,
                    "projectName": project_data.get("name"),
                    "address": project_data.get("address"),
                    "dueDate": project_data.get("dueDate"),
                    "budget": project_data.get("budget")
                }
                projects_list.append(project)
        return jsonify(projects_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
