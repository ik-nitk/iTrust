from flask import Blueprint, render_template, current_app, session, request, redirect, url_for, jsonify
from web.utils import get_member_from_session, get_member_details

blueprint = Blueprint(
            'member',
             __name__
        )

@blueprint.route("/members")
def member_list_view():
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    url = api.members
    response = app_session.get(url)
    response.raise_for_status()
    members=response.json()
    return render_template("members/list.html", members=members)

@blueprint.route("/members/create",methods = ["GET","POST"])
def create_member():
    current_member = ''
    try:
        current_member = get_member_from_session()
        if not current_member["is_core"]:
            raise Exception("Only Core member can create members")
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    if request.method == 'GET':
        return render_template("members/create.html")
    else:
        govtId = request.form.get('govt_id')
        idType = request.form.get('id_type')
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        middleName = request.form.get('middle_name')
        isCore = request.form.get('is_core')
        if isCore == "True":
            isCore = True
        else:
            isCore = False
        phone = request.form.get('phone_no')
        email = request.form.get('email')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.members
        response = app_session.post(url, json = {"govtId":govtId,"idType":idType,"firstName":firstName,"lastName":lastName,"middleName":middleName,"isCore":isCore,"phone":phone,"email":email, "created_by":current_member['member_id']})
        response.raise_for_status()
        return redirect(url_for('member.member_view', id=response.json()))


@blueprint.route("/members/search",methods = ["GET","POST"])
def member_search():
    if request.method == 'GET':
        return render_template("members/search.html")
    else:
        search_input = request.form.get('query')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.member_search
        response = app_session.post(url, json = {"search_input":search_input})
        response.raise_for_status()
        members = response.json()
        return jsonify({'htmlresponse': render_template("members/search_response.html", members=members)})


def get_case_details_with_member_id(api, app_session, id):
    ## TODO : the below code looks like not working, need fix it.
    url = api.case_list(id)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

@blueprint.route("/members/view/<id>",methods = ["GET"])
def member_view(id):
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    cases = get_case_details_with_member_id(api,app_session,id)
    url = api.member_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    members = response.json()
    updated_by = get_member_details(api, app_session, members[0]["updated__by"])
    return render_template("members/view.html", members=members,cases = cases, updated_by=updated_by)


@blueprint.route("/members/update/<id>",methods = ["GET","POST"])
def member_update(id):
    current_member = ''
    try:
        current_member = get_member_from_session()
        if not current_member["is_core"]:
            raise Exception("Only Core member can update members")
    except Exception as e:
        return render_template("error.html", error_msg=str(e))
    if request.method == "GET":
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url = api.member_id(id)
        response = app_session.get(url)
        response.raise_for_status()
        members = response.json()
        return render_template("members/update.html", members=members)
    else:
        govtId = request.form.get('govt_id')
        idType = request.form.get('id_type')
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        middleName = request.form.get('middle_name')
        isCore = request.form.get('is_core')
        if isCore == "True":
            isCore = True
        else:
            isCore = False
        phone = request.form.get('phone_no')
        email = request.form.get('email')
        api = current_app.config.get('api')
        app_session = current_app.config.get('app_session')
        url =  api.member_id(id)
        response = app_session.post(url, json = {"govtId":govtId,"idType":idType,"firstName":firstName,"lastName":lastName,"middleName":middleName,"isCore":isCore,"phone":phone,"email":email, "updated_by":current_member['member_id']})
        return redirect(url_for('member.member_view', id=id))
