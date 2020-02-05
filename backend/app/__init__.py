from flask import Blueprint
from flask_restplus import Api

from app.main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',

          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
# api.add_namespace(task_api)
