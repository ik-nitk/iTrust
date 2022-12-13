import traceback
from turtle import title
from cms.domain.case_state import CaseState
from cms.domain.comment_type import CommentType
from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, Response
import requests
from cms.domain.utils import isNotBlank
from concurrent.futures import ThreadPoolExecutor, wait
import json
from web.utils import get_member_from_session, get_member_details

pool = ThreadPoolExecutor(10)
blueprint = Blueprint(
            'case',
             __name__
        )

@blueprint.route("/cases")
def case_list_view():
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    url = api.cases
    response = app_session.get(url)
    response.raise_for_status()
    cases=response.json()
    return render_template("cases/list.html", cases=cases)

def get_case_details(api, app_session, id):
    url = api.case_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

def get_case_comments(api, app_session, id):
    url = api.case_comment_list(id)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

def get_case_votes(api, app_session, id):
    url = api.case_vote_list(id)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

def get_case_initial_documents(api, app_session, id):
    doc_url = api.case_doc_list(id, 'INITIAL_CASE_DOC')
    response = app_session.get(doc_url)
    response.raise_for_status()
    return response.json()

def get_beneficiary_details(api, app_session, id):
    url = api.beneficiary_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    beneficiaries = response.json()
    assert beneficiaries and len(beneficiaries) > 0, "Invalid beneficiary_id"
    return beneficiaries[0]

@blueprint.route("/cases/view/<id>", methods = ["GET"])
def case_view(id):
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    try:
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        futures = []
        futures.append(pool.submit(get_case_details, api, app_session, id))
        futures.append(pool.submit(get_case_initial_documents, api, app_session, id))
        futures.append(pool.submit(get_case_comments, api, app_session, id))
        futures.append(pool.submit(get_case_votes, api, app_session, id))
        wait(futures)
        case = futures[0].result()
        initial_doc_list=futures[1].result()
        case_comments=futures[2].result()
        case_votes = futures[3].result()
        verification_comments = list(filter(lambda x: (x['comment_type'] == CommentType.VERIFICATION_COMMENTS), case_comments))
        beneficiary = get_beneficiary_details(api, app_session, case['beneficiary__id'])
        updated_by = get_member_details(api, app_session, case["updated__by"])
        return render_template("cases/view.html",
            case=case,
            beneficiary=beneficiary,
            initial_doc_list=initial_doc_list,
            publish_disable=((case['case_state'] != CaseState.DRAFT) or (case['case_state'] == CaseState.DRAFT and len(initial_doc_list) == 0)),
            verification_done=(len(verification_comments) > 0), #atleast one verification comment added.
            verification_comments=verification_comments,
            voting_done = (len(case_votes) > 0),
            case_votes = case_votes,
            updated_by = updated_by
        )
    except Exception as e:
        print(traceback.format_exc())
        return render_template("error.html", error_msg=str(e))

@blueprint.route("/cases/<id>/publish", methods = ["POST"])
def publish_case(id):
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    url = api.publish_case(id)
    response = app_session.post(url, json={ "updated_by":current_member['member_id']})
    response.raise_for_status()
    return redirect('/cases/view/' + id)

@blueprint.route("/cases/<id>/add_initial_documents", methods = ["POST"])
def add_initial_case_documents(id):
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    url = api.case_initial_docs(id)
    # TODO - Get case state, don't render if its not in Draft state
    doc_list = request.json['doc_list']
    response = app_session.post(url, json={'doc_list':doc_list, "created_by":current_member['member_id']})
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: Uploading failed for case: ' + id)
        print(e)
        return Response(
            json.dumps({'error': response.reason}),
            mimetype="application/json",
            status=response.status_code,
        )
    return Response(
        json.dumps({'redirect': '/cases/view/' + id}),
        mimetype="application/json",
        status=200,
    )

@blueprint.route("/cases/<case_id>/add_verification_details", methods = ["GET", "POST"])
def add_verification_details(case_id):
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    try:
        if request.method == "GET":
            return render_template('cases/add_verification_details.html', case_id=case_id)
        else:
            api = current_app.config.get('api')
            app_session = current_app.config.get('app_session')
            comment = request.form.get('comment')
            url = api.case_verification_details(case_id)
            response = app_session.post(url, json = {'comment':comment, "verified_by":current_member['member_id']})
            response.raise_for_status()
            return redirect('/cases/view/' + case_id)
    except Exception as e:
        print(traceback.format_exc())
        return render_template("error.html", error_msg=str(e))

@blueprint.route("/cases/<case_id>/add_vote_to_case", methods = ["GET", "POST"])
def add_vote_to_case(case_id):
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    try:
        if request.method == "GET":
            api = current_app.config.get('api')
            app_session = current_app.config.get('app_session')
            case = get_case_details(api, app_session, case_id)
            return render_template('cases/add_vote_to_case.html', case = case)
        else:
            api = current_app.config.get('api')
            app_session = current_app.config.get('app_session')
            vote = request.form.get('vote')
            comment = request.form.get('comment')
            amount_suggested = request.form.get('amount_suggested')
            url = api.case_vote(case_id)
            assert isNotBlank(comment) and isNotBlank(amount_suggested) , "values can't be empty"
            response = app_session.post(url, json = {'vote':vote,'comment':comment,'amount_suggested': amount_suggested,"created_by":current_member['member_id']})
            response.raise_for_status()
            return redirect('/cases/view/' + case_id)
    except Exception as e:
        print(traceback.format_exc())
        return render_template("error.html", error_msg=str(e))

@blueprint.route("/cases/<id>/upload", methods = ["GET"])
def upload_case_docs(id):
    return render_template('cases/upload_case_docs.html', id=id)

@blueprint.route("/cases/create", methods = ["GET","POST"])
def create_case():
    current_member = ''
    try:
        current_member = get_member_from_session()
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    try:
        if request.method == 'GET':
            for_ben = request.args.get('for')
            beneficiary = None
            if for_ben:
                api = current_app.config.get('api')
                app_session = current_app.config.get('app_session')
                url = api.beneficiary_id(for_ben)
                response = app_session.get(url)
                response.raise_for_status()
                beneficiary = response.json()[0]
            return render_template("cases/create.html", beneficiary=beneficiary)
        else:
            beneficiary_id = request.form.get('beneficiary_id')
            purpose = request.form.get('purpose')
            title = request.form.get('title')
            description = request.form.get('description')
            amount_needed = request.form.get('amount_needed')
            api = current_app.config.get('api')
            app_session = current_app.config.get('app_session')
            url = api.cases
            assert isNotBlank(beneficiary_id) and isNotBlank(title) and isNotBlank(description) and isNotBlank(amount_needed), "values can't be empty"
            beneficiary = get_beneficiary_details(api, app_session, beneficiary_id)
            assert beneficiary
            response = app_session.post(url, json = {"beneficiary_id":beneficiary_id,"purpose":purpose,"title":title,"description":description,"amount_needed":amount_needed,"created_by":current_member['member_id']})
            response.raise_for_status()
            case_id = response.json()
            return redirect('/cases/view/' + case_id)
    except Exception as e:
        print(traceback.format_exc())
        return render_template("error.html", error_msg=str(e))

