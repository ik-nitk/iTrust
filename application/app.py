import os
import traceback
from flask import Flask, jsonify, request, json
import redis
from rq import Queue
from logging.config import dictConfig


from application.rest import member
from application.rest import beneficiary
from application.rest import case
from cms.repository.postgresrepo import PostgresRepo
from cms.repository.memrepo import MemRepo

postgres_configuration = {
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "POSTGRES_HOSTNAME": os.environ.get("POSTGRES_HOSTNAME"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT", 2000),
    "APPLICATION_DB": os.environ.get("APPLICATION_DB"),
}

def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(member.blueprint)
    app.register_blueprint(beneficiary.blueprint)
    app.register_blueprint(case.blueprint)
    app.config['TRAP_HTTP_EXCEPTIONS']=True

    @app.after_request
    def after_request(response):
        app.logger.info('%s %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status, response.data if response.status == 500 else '')
        return response

    @app.errorhandler(500)
    def handle_500(e):
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())
        return jsonify({"error_msg":str(e)})

    @app.errorhandler(Exception)
    def handle_exception(e):
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())
        return jsonify({"error_msg":str(e)})

    with app.app_context():
        if config_name == "testing":
            app.config['REPO'] = MemRepo([])
        else:
            # get redis connection
            redis_connection = redis.from_url(os.environ.get("REDIS_URL"))
            # get rq queue with redis connection
            queue = Queue(connection=redis_connection)
            app.config['QUEUE'] = queue
            # Postgress installtion.
            app.config['REPO'] = PostgresRepo(postgres_configuration)
            # Logging configuration
            dictConfig(
                {
                    "version": 1,
                    "formatters": {
                        "default": {
                            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                        }
                    },
                    "handlers": {
                        "console": {
                            "class": "logging.StreamHandler",
                            "stream": "ext://sys.stdout",
                            "formatter": "default",
                        },
                        "file": {
                            "class": "logging.handlers.RotatingFileHandler",
                            "filename": "/var/log/application.log",
                            "maxBytes": 1000000,
                            "backupCount": 3,
                            "formatter": "default",
                        }
                    },
                    "root": {"level": "INFO", "handlers": ["console", "file"]},
                }
            )

    return app
