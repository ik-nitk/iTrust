from flask import Blueprint, render_template, current_app, request, redirect, url_for, jsonify

blueprint = Blueprint(
            'member',
             __name__
        )

@blueprint.route("/members")
def member_list_view():
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    url = api.members
    response = session.get(url)
    response.raise_for_status()
    members=response.json()
    return render_template("members/list.html", members=members)

@blueprint.route("/members/create",methods = ["GET","POST"])
def create_member():
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
        session = current_app.config.get('session')
        url = api.members
        response = session.post(url, json = {"govtId":govtId,"idType":idType,"firstName":firstName,"lastName":lastName,"middleName":middleName,"isCore":isCore,"phone":phone,"email":email})
        response.raise_for_status()
        return redirect(url_for('member.member_list_view'))


@blueprint.route("/members/search",methods = ["GET","POST"])
def member_search():
    if request.method == 'GET':
        return render_template("members/search.html")
    else:
        search_input = request.form.get('query')
        api = current_app.config.get('api')
        session = current_app.config.get('session')
        url = api.member_search
        response = session.post(url, json = {"search_input":search_input})
        response.raise_for_status()
        members = response.json()
        return jsonify({'htmlresponse': render_template("members/search_response.html", members=members)})


@blueprint.route("/members/view/<id>",methods = ["GET"])
def member_view(id):
    print(id)
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    url = api.member_id(id)
    print(url)
    response = session.get(url)
    response.raise_for_status()
    members = response.json()
    print(members)
    return render_template("members/view.html", members=members)


@blueprint.route("/members/update/<id>",methods = ["GET","POST"])
def member_update(id):
    if request.method == "GET":
        api = current_app.config.get('api')
        session = current_app.config.get('session')
        url = api.member_id(id)
        response = session.get(url)
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
        session = current_app.config.get('session')
        url =  api.member_id(id)
        response = session.post(url, json = {"govtId":govtId,"idType":idType,"firstName":firstName,"lastName":lastName,"middleName":middleName,"isCore":isCore,"phone":phone,"email":email}) 
        return redirect("/members")
