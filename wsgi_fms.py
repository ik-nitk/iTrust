import os

from fms_service.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
