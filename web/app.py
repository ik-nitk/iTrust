from flask import Flask, render_template, session
import traceback
import requests
import os
import pathlib
from google_auth_oauthlib.flow import Flow
from flask_bootstrap import Bootstrap
import json
from logging.config import dictConfig
from web.member import views as members
from web.case import views as cases
from web.home import views as home
from web.upload import views as upload
from web.beneficiary import views as beneficiaries

from web.backend_api_builder import BackendApiBuilder


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
                "filename": "/var/log/web.log",
                "maxBytes": 1000000,
                "backupCount": 3,
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console", "file"]},
    }
)



def create_app(config_name):

    app = Flask(__name__)
    app.secret_key = "iTrust-Beta"
    bootstrap = Bootstrap(app)
    api = BackendApiBuilder()
    app_session = requests.session()
    config_module = f"web.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(members.blueprint)
    app.register_blueprint(home.blueprint)
    app.register_blueprint(upload.blueprint)
    app.register_blueprint(beneficiaries.blueprint)
    app.register_blueprint(cases.blueprint)
    app.config['api'] = api

    def print_response_on_error(r, *args, **kwargs):
        if r.status_code == 500:
            print("Error with downstream URL", r.url, r.text)
            app.logger.error("Error with downstream URL %s %s", r.url, r.text)

    app.config['app_session'] = app_session
    app_session.hooks['response'].append(print_response_on_error)

    ## Authentication module if enabled.
    if os.environ.get("AUTH_ENABLED", "false").lower() == "true":
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
        with open(client_secrets_file, 'r') as f:
            client_secret_data = json.load(f)
            app.config['GOOGLE_CLIENT_ID'] = client_secret_data["web"]["client_id"]
        flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
            client_secrets_file=client_secrets_file,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
            redirect_uri=os.environ.get("REDIRECT_URL", "http://127.0.0.1:8080/callback")
        )
        app.config['FLOW'] = flow

    @app.context_processor
    def provide_user():
        logged_in=False
        user=''
        if "google_id" in session:
            logged_in=True
            user=session["name"]
        return {'logged_in': logged_in, 'user': user}

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")

    @app.errorhandler(Exception)
    def handle_exception(e):
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())
        return render_template("error.html", error_msg=str(e)), 500
    return app
