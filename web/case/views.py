from flask import Blueprint, render_template, current_app, request, redirect, url_for, Response
import requests
from concurrent.futures import ThreadPoolExecutor, wait
import json

pool = ThreadPoolExecutor(10)
blueprint = Blueprint(
            'case',
             __name__
        )

@blueprint.route("/cases")
def case_list_view():
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    url = api.cases
    response = session.get(url)
    response.raise_for_status()
    cases=response.json()
    return render_template("cases/list.html", cases=cases)

def get_case_details(api, session, id):
    url = api.case_id(id)
    response = session.get(url)
    response.raise_for_status()
    return response.json()

def get_case_initial_documents(api, session, id):
    doc_url = api.case_doc_list(id, 'INITIAL_CASE_DOC')
    response = session.get(doc_url)
    response.raise_for_status()
    return response.json()

def get_beneficiary_details(api, session, id):
    url = api.beneficiary_id(id)
    response = session.get(url)
    response.raise_for_status()
    beneficiaries = response.json()
    return beneficiaries[0]

@blueprint.route("/cases/view/<id>",methods = ["GET"])
def case_view(id):
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    futures = []
    futures.append(pool.submit(get_case_details, api, session, id))
    futures.append(pool.submit(get_case_initial_documents, api, session, id))
    wait(futures)
    case = futures[0].result()
    initial_doc_list=futures[1].result()
    beneficiary = get_beneficiary_details(api, session, case['beneficiary__id'])
    return render_template("cases/view.html", case=case, beneficiary=beneficiary, initial_doc_list=initial_doc_list)

@blueprint.route("/cases/<id>/add_initial_documents", methods = ["POST"])
def add_initial_case_documents(id):
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    url = api.case_initial_docs(id)
    # TODO - Get case state, don't render if its not in Draft state
    doc_list = request.json['doc_list']
    response = session.post(url, json={'doc_list':doc_list})
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
    print('Uploading success to case: ' + id)
    print('rediecting to cases/view/' + id)
    return Response(
        json.dumps({'redirect': '/cases/view/' + id}),
        mimetype="application/json",
        status=200,
    )

@blueprint.route("/cases/<id>/upload", methods = ["GET"])
def upload_case_docs(id):
    return render_template('cases/upload_case_docs.html', id=id)

@blueprint.route("/cases/create", methods = ["GET","POST"])
def create_case():
    if request.method == 'GET':
        for_ben = request.args.get('for')
        beneficiary = None
        if for_ben:
            api = current_app.config.get('api')
            session = current_app.config.get('session')
            url = api.beneficiary_id(for_ben)
            response = session.get(url)
            response.raise_for_status()
            beneficiary = response.json()[0]
        return render_template("cases/create.html", beneficiary=beneficiary)
    else:
        beneficiary_id = request.form.get('beneficiary_id')
        purpose = request.form.get('purpose')
        title = request.form.get('title')
        description = request.form.get('description')
        api = current_app.config.get('api')
        session = current_app.config.get('session')
        url = api.cases
        response = session.post(url, json = {"beneficiary_id":beneficiary_id,"purpose":purpose,"title":title,"description":description})
        response.raise_for_status()
        return redirect(url_for('case.case_list_view'))

