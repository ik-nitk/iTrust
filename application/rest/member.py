import json

from flask import Blueprint, request, Response, current_app,jsonify

from cms.use_cases.member import member_list_use_case
from cms.serializers.member import MemberJsonEncoder
from cms.requests.member_list import build_member_list_request
from common.responses import ResponseTypes
from cms.use_cases.member import create_new_member
from cms.use_cases.member import search_member
from cms.use_cases.member import view_member
from cms.use_cases.member import view_member_by_email
from cms.use_cases.member import update_member

blueprint = Blueprint("member", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


@blueprint.route("/api/v1/members", methods=["GET"])
def member_list():
    email_id = request.args.get('email_id')
    if email_id is not None:
        response = view_member_by_email(current_app.config.get('REPO'), email_id)
        return Response(
            json.dumps(response.value, cls=MemberJsonEncoder),
            mimetype="application/json",
            status=STATUS_CODES[response.type],
        )
    qrystr_params = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_member_list_request(
        filters=qrystr_params["filters"]
    )

    response = member_list_use_case(current_app.config.get('REPO'), request_object)

    return Response(
        json.dumps(response.value, cls=MemberJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )


@blueprint.route("/api/v1/members", methods=["POST"])
def create_member():
    govtId = request.json['govtId']
    idType = request.json['idType']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    middleName = request.json['middleName']
    isCore = request.json['isCore']
    phone = request.json['phone']
    email = request.json['email']
    created_by = request.json['created_by']
    response = create_new_member(current_app.config['REPO'],govtId,idType,firstName,lastName,middleName,isCore,phone,email, created_by)
    return Response(
        json.dumps(response.value, cls=MemberJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/members/search", methods=["POST"])
def member_search():
    search_input = request.json['search_input']
    response = search_member(current_app.config.get('REPO'), search_input)
    print(response)
    return Response(
        json.dumps(response.value, cls=MemberJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/members/<id>", methods=["GET"])
def member_view(id):
    response = view_member(current_app.config.get('REPO'), id)
    return Response(
        json.dumps(response.value, cls=MemberJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/members/<id>", methods=["POST"])
def member_update(id):
    govtId = request.json['govtId']
    idType = request.json['idType']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    middleName = request.json['middleName']
    isCore = request.json['isCore']
    phone = request.json['phone']
    email = request.json['email']
    updated_by = request.json['updated_by']
    response = update_member(current_app.config['REPO'],id,govtId,idType,firstName,middleName,lastName,isCore,phone,email, updated_by)
    return Response(
        json.dumps(response.value, cls=MemberJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

# curl   -X POST -H "Content-Type: application/json" -d '{"memberId":"sample-113","govtId":"gid-1112","idType":"AADHAAR","firstName":"sample","lastName":"lname","middleName":"mname","isCore":false,"phone":"99872111","email":"email2@sample"}'  http://localhost:8000/api/v1/members/create