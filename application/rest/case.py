import json

from flask import Blueprint, request, Response, current_app, jsonify

from cms.use_cases.case import (
    case_list_use_case,
    create_new_case,
    add_initial_documents_use_case,
    view_case,
    doc_list,
    comment_list,
    add_case_verification_details,
    add_vote,
    vote_list,
    publish_case_use_case,
    close_case_with_details,
    add_payment_details_use_case)
from cms.serializers.case import CaseJsonEncoder, CaseDocsJsonEncoder, CaseCommentJsonEncoder,CaseVoteJsonEncoder
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
    updated_by = request.json['updated_by']
    response = publish_case_use_case(current_app.config.get('REPO'), case_id, updated_by)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<case_id>/add_initial_documents", methods=["POST"])
def add_initial_documents(case_id):
    doc_list = request.json['doc_list']
    created_by = request.json['created_by']
    response = add_initial_documents_use_case(current_app.config.get('REPO'), case_id, created_by, doc_list)
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

@blueprint.route("/api/v1/cases/<case_id>/add_case_verification_details", methods=["POST"])
def add_verification_comment_to_case(case_id):
    comment = request.json['comment']
    verified_by = request.json['verified_by']
    response = add_case_verification_details(current_app.config.get('REPO'), case_id, comment, verified_by)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<case_id>/add_payment_details", methods=["POST"])
def add_payment_details(case_id):
    amount_paid = request.json['amount_paid']
    comment = request.json['comment']
    doc_list = request.json['doc_list']
    created_by = request.json['created_by']
    response = add_payment_details_use_case(current_app.config.get('REPO'), case_id, comment, amount_paid, created_by, doc_list)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<id>/close", methods=["POST"])
def close_case_api(id):
    comment = request.json['comment']
    closed_by = request.json['closed_by']
    response = close_case_with_details(current_app.config.get('REPO'), id, comment, closed_by)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<id>/comments", methods=["GET"])
def comments_list_api(id):
    comment_type = request.args.get('comment_type')
    response = comment_list(current_app.config.get('REPO'), id, comment_type)
    return Response(
        json.dumps(response.value, cls=CaseCommentJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<case_id>/add_vote_to_case", methods=["POST"])
def add_vote_to_case(case_id):
    vote = request.json['vote']
    comment = request.json['comment']
    amount_suggested = request.json['amount_suggested']
    created_by = request.json['created_by']
    response = add_vote(current_app.config.get('REPO'), case_id, vote,comment,amount_suggested,created_by)
    return Response(
        json.dumps(response.value, cls=CaseVoteJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

@blueprint.route("/api/v1/cases/<id>/votes", methods=["GET"])
def votes_list_api(id):
    response = vote_list(current_app.config.get('REPO'), id)
    print(response)
    return Response(
        json.dumps(response.value, cls=CaseVoteJsonEncoder),
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
    amount_needed = request.json['amount_needed']
    created_by = request.json['created_by']
    response = create_new_case(current_app.config['REPO'],beneficiary_id, purpose, title, description,amount_needed,created_by)
    return Response(
        json.dumps(response.value, cls=CaseJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )

#curl -X POST -H "Content-Type: application/json" -d '{"beneficiary_id":"i.ben.4RRQqp2HZPXPytC9pZr99", "purpose": "EDUCATION", "title":"t", "description":"d"}'  http://localhost:8000/api/v1/cases