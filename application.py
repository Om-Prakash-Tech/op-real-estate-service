from flask import Blueprint, Flask, make_response
from flask_cors import CORS
from api_v1.routes.contractors import contractors_blueprint
from api_v1.routes.projects import projects_blueprint
from api_v1.routes.transactions import transactions_blueprint
from api_v1.routes.metrics import metrics_blueprint
from api_v1.routes.deals import deals_blueprint

application = Flask(__name__)

cors = CORS(application)

api_v1_blueprint = Blueprint('api_v1', __name__)

@application.route('/', methods=['GET'])
def index():
    return make_response()

@api_v1_blueprint.route('/', methods=['GET'])
def v1_health_check():
    return make_response()

api_v1_blueprint.register_blueprint(contractors_blueprint, url_prefix='/contractors')
api_v1_blueprint.register_blueprint(projects_blueprint, url_prefix='/projects')
api_v1_blueprint.register_blueprint(transactions_blueprint, url_prefix='/transactions')
api_v1_blueprint.register_blueprint(metrics_blueprint, url_prefix='/metrics')
api_v1_blueprint.register_blueprint(deals_blueprint, url_prefix='/deals')

application.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=8000)