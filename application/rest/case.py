import json

from flask import Blueprint, request, Response, current_app,jsonify

from cms.use_cases.case_list import case_list_use_case
from cms.serializers.case import CaseJsonEncoder
from cms.requests.case_list import build_case_list_request
from common.responses import ResponseTypes

blueprint = Blueprint("case", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


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
