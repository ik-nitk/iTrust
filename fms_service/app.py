import os
from flask import Flask

import logging
import logging.handlers
from fms_service.rest import document
from fms.repository.mongorepo import MongoRepo

mongodb_configuration = {
    "MONGODB_USER": os.environ.get("MONGODB_USER"),
    "MONGODB_PASSWORD": os.environ.get("MONGODB_PASSWORD"),
    "MONGODB_HOSTNAME": os.environ.get("MONGODB_HOSTNAME"),
    "MONGODB_PORT": os.environ.get("MONGODB_PORT", 27017),
    "APPLICATION_DB": os.environ.get("APPLICATION_DB"),
}

def create_app(config_name):

    app = Flask(__name__)
    handler = logging.handlers.RotatingFileHandler(
        '/var/log/app.log',
        maxBytes=1024 * 1024)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    config_module = f"fms_service.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(document.blueprint)

    with app.app_context():
            app.config['REPO'] = MongoRepo(mongodb_configuration)
    app.logger.info('Starting FMS rest service!!')

    return app
