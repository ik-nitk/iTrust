from flask import Blueprint, render_template, send_file
import requests

blueprint = Blueprint(
            'upload',
             __name__
        )

@blueprint.route("/upload")
def upload_page():
    return send_file('/opt/code/web/templates/upload/upload.html')

@blueprint.route("/upload_dropzone")
def upload_dropzone():
    return render_template('upload/upload_dropzone.html')