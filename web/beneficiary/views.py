from crypt import methods
from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, jsonify

blueprint = Blueprint(
            'beneficiary',
             __name__
        )

@blueprint.route("/beneficiaries")
def beneficiary_list_view():
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    url = api.beneficiaries
    response = app_session.get(url)
    response.raise_for_status()
    beneficiaries=response.json()
    return render_template("beneficiaries/list.html", beneficiaries=beneficiaries)

@blueprint.route("/beneficiaries/create",methods = ["GET","POST"])
def create_beneficiary():
    if "google_id" not in session:
        return render_template("error.html", error_msg="please login to create beneficiary")
    if request.method == 'GET':
        return render_template("beneficiaries/create.html")
    else:
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        middleName = request.form.get('middle_name')
        phone = request.form.get('phone_no')
        email = request.form.get('email')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.beneficiaries
        response = app_session.post(url, json = {"firstName":firstName,"lastName":lastName,"middleName":middleName,"phone":phone,"email":email})
        response.raise_for_status()
        return redirect(url_for('beneficiary.beneficiary_list_view'))

@blueprint.route("/beneficiaries/search",methods = ["GET","POST"])
def beneficiary_search():
    if request.method == 'GET':
        return render_template("beneficiaries/search.html")
    else:
        search_input = request.form.get('query')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.beneficiary_search
        response = app_session.post(url, json = {"search_input":search_input})
        response.raise_for_status()
        beneficiaries = response.json()
        return jsonify({'htmlresponse': render_template("beneficiaries/search_response.html", beneficiaries=beneficiaries)})

def get_case_details_with_beneficiary_id(api, app_session, id):
    url = api.case_list(id)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

@blueprint.route("/beneficiaries/view/<id>",methods = ["GET"])
def beneficiary_view(id):
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    cases = get_case_details_with_beneficiary_id(api,app_session,id)
    url = api.beneficiary_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    beneficiaries = response.json()
    return render_template("beneficiaries/view.html", beneficiaries=beneficiaries,cases = cases)


@blueprint.route("/beneficiaries/update/<id>",methods = ["GET","POST"])
def beneficiary_update(id):
    if "google_id" not in session:
        return render_template("error.html", error_msg="please login to update beneficiary")
    if request.method == "GET":
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.beneficiary_id(id)
        response = app_session.get(url)
        response.raise_for_status()
        beneficiaries = response.json()
        return render_template("beneficiaries/update.html", beneficiaries=beneficiaries)
    else:
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        middleName = request.form.get('middle_name')
        phone = request.form.get('phone_no')
        email = request.form.get('email')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.beneficiary_id(id)
        response = app_session.post(url, json = {"firstName":firstName,"lastName":lastName,"middleName":middleName,"phone":phone,"email":email}) 
        return redirect("/beneficiaries")




