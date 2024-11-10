from config import projects, contractors

UNVERIFIED = "unverified"
VERIFIED = "verified"

DEAL_TYPES = ["buy", "sell"]

def get_project_data(project_id):
    doc = projects.document(project_id).get()
    if doc.exists:
        project_data = doc.to_dict()
        return {
            "projectId": project_id,
            "projectName": project_data.get("projectName"),
            "address": project_data.get("address"),
            "dueDate": project_data.get("dueDate"),
            "budget": project_data.get("budget")
        }
    return None

def get_contractor_data(contractor_id):
    doc = contractors.document(contractor_id).get()
    if doc.exists:
        contractor_data = doc.to_dict()
        return {
            "contractorId": contractor_id,
            "name": contractor_data.get("name"),
            "email": contractor_data.get("email"),
            "phone": contractor_data.get("phone")
        }
    return None