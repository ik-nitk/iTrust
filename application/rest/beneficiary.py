import json

from flask import Blueprint, request, Response, current_app,jsonify

from cms.use_cases.beneficiary_list import beneficiary_list_use_case
from cms.serializers.beneficiary import BeneficiaryJsonEncoder
from cms.requests.beneficiary_list import build_beneficiary_list_request
from common.responses import ResponseTypes
from cms.use_cases.create_beneficiary import create_new_beneficiary

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

    # curl   -X POST -H "Content-Type: application/json" -d '{"firstName":"sample","lastName":"lname","middleName":"mname","phone":"99872111","email":"email2@sample"}'  http://localhost:8000/api/v1/beneficiaries