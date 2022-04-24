from flask import Flask, render_template
import requests
from flask_bootstrap import Bootstrap
from web.member import views as members
from web.home import views as home
from web.upload import views as upload
from web.backend_api_builder import BackendApiBuilder

def create_app(config_name):

    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    api = BackendApiBuilder()
    session = requests.session()
    config_module = f"web.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(members.blueprint)
    app.register_blueprint(home.blueprint)
    app.register_blueprint(upload.blueprint)
    app.config['api'] = api
    app.config['session'] = session

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")
    return app
