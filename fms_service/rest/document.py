import json
import os
from urllib import response

from flask import Blueprint, request, Response, current_app, send_file
from werkzeug.utils import secure_filename
from fms.use_cases.documents import create_new_document, find_document
from common.responses import ResponseTypes

blueprint = Blueprint("document", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/api/v1/documents', methods=['POST'])
def upload_file():
    files = request.files['file']
    if files and allowed_file(files.filename):
        filename = secure_filename(files.filename)
        response = create_new_document(current_app.config['REPO'], filename, "TODO-USER")
        if bool(response) is True:
            current_app.logger.info(f"Saving file to : {response.value}")
            files.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), response.value + filename))
            return Response(
                json.dumps({"files":[
                    {
                        "name": f"{filename}",
                        "url": f"/fms/api/v1/documents/{response.value}"
                    }]}),
                mimetype="application/json",
                status=STATUS_CODES[ResponseTypes.SUCCESS],
            )
    return Response(
            None,
            mimetype="application/json",
            status=STATUS_CODES[ResponseTypes.SYSTEM_ERROR],
    )


@blueprint.route("/api/v1/documents/<id>", methods=["GET"])
def document_find(id):
    response = find_document(current_app.config['REPO'], id)
    if bool(response) is True:
        document = response.value
        current_app.logger.info(f"Sending file : {document.to_dict()}")
        return send_file(os.path.join(os.environ.get('UPLOAD_FOLDER'),  document._id + document.filename))
    else:
        return Response(
                json.dumps(response.value),
                mimetype="application/json",
                status=STATUS_CODES[ResponseTypes.RESOURCE_ERROR],
        )
