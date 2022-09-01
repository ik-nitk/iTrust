import json

from flask import Blueprint, request, Response, current_app,jsonify

from cms.use_cases.case import (
    case_list_use_case,
    create_new_case,
    add_initial_documents_use_case,
    view_case,
    doc_list,
    publish_case_use_case,
    case_list_from_beneficiary_id)
from cms.serializers.case import CaseJsonEncoder, CaseDocsJsonEncoder
from cms.requests.case_list import build_case_list_request
from common.responses import ResponseTypes

blueprint = Blueprint("case", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

@blueprint.route("/api/v1/cases/<case_id>/publish", methods=["POST"])
def publish_case(case_id):
    response = publish_case_use_case(current_app.config.get('REPO'), case_id)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<case_id>/add_initial_documents", methods=["POST"])
def add_initial_documents(case_id):
    doc_list = request.json['doc_list']
    response = add_initial_documents_use_case(current_app.config.get('REPO'), case_id, doc_list)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<id>", methods=["GET"])
def case_view(id):
    response = view_case(current_app.config.get('REPO'), id)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<id>/docs", methods=["GET"])
def doc_list_api(id):
    doc_type = request.args.get('doc_type')
    response = doc_list(current_app.config.get('REPO'), id, doc_type)
    return Response(
        json.dumps(response.value, cls=CaseDocsJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases", methods=["GET"])
def case_list():
    qrystr_params = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_case_list_request(
        filters=qrystr_params["filters"]
    )

    response = case_list_use_case(current_app.config.get('REPO'), request_object)

    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases", methods=["POST"])
def create_case():
    beneficiary_id = request.json['beneficiary_id']
    purpose = request.json['purpose']
    title = request.json['title']
    description = request.json['description']
    response = create_new_case(current_app.config['REPO'],beneficiary_id, purpose, title, description)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/caselistfrombenificiaryid/<id>", methods=["GET"])
def case_list_with_beneficiaryid(id):
    response = case_list_from_beneficiary_id(current_app.config.get('REPO'), id)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

#curl -X POST -H "Content-Type: application/json" -d '{"beneficiary_id":"i.ben.4RRQqp2HZPXPytC9pZr99", "purpose": "EDUCATION", "title":"t", "description":"d"}'  http://localhost:8000/api/v1/cases