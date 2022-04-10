import json

from flask import Blueprint, request, Response, current_app

from cms.use_cases.member_list import member_list_use_case
from cms.serializers.member import MemberJsonEncoder
from cms.requests.member_list import build_member_list_request
from cms.responses import ResponseTypes

blueprint = Blueprint("member", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


@blueprint.route("/api/v1/members", methods=["GET"])
def member_list():
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
