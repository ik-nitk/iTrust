import os
from flask import Flask
import redis
from rq import Queue

from application.rest import member
from application.rest import beneficiary
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

    return app
