import json

from flask import Blueprint, request, Response, current_app,jsonify

from cms.use_cases.beneficiary import beneficiary_list_use_case,create_new_beneficiary,search_beneficiary,update_beneficiary,view_beneficiary
from cms.serializers.beneficiary import BeneficiaryJsonEncoder
from cms.requests.beneficiary_list import build_beneficiary_list_request
from common.responses import ResponseTypes



blueprint = Blueprint("beneficiary", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


@blueprint.route("/api/v1/beneficiaries", methods=["GET"])
def beneficiary_list():
    qrystr_params = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_beneficiary_list_request(
        filters=qrystr_params["filters"]
    )

    response = beneficiary_list_use_case(current_app.config.get('REPO'), request_object)

    return Response(
        json.dumps(response.value, cls=BeneficiaryJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/beneficiaries", methods=["POST"])
def create_beneficiary():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    middleName = request.json['middleName']
    phone = request.json['phone']
    email = request.json['email']
    response = create_new_beneficiary(current_app.config['REPO'],firstName,lastName,middleName,phone,email)
    return Response(
        json.dumps(response.value, cls=BeneficiaryJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/beneficiaries/search", methods=["POST"])
def beneficiary_search():
    search_input = request.json['search_input']
    response = search_beneficiary(current_app.config.get('REPO'), search_input)
    return Response(
        json.dumps(response.value, cls=BeneficiaryJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/beneficiaries/<id>", methods=["GET"])
def beneficiary_view(id):
    response = view_beneficiary(current_app.config.get('REPO'), id)
    return Response(
        json.dumps(response.value, cls=BeneficiaryJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/beneficiaries/<id>", methods=["POST"])
def beneficiary_update(id):
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    middleName = request.json['middleName']
    phone = request.json['phone']
    email = request.json['email']
    response = update_beneficiary(current_app.config['REPO'],id,firstName,lastName,middleName,phone,email)
    return Response(
        json.dumps(response.value, cls=BeneficiaryJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

    