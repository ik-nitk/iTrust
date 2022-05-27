from crypt import methods
from flask import Blueprint, render_template, current_app, request

blueprint = Blueprint(
            'member',
             __name__
        )

#@blueprint.route("/members")
# def member_list_view():
#     api = current_app.config.get('api')
#     session = current_app.config.get('session')
#     url = api.members
#     response = session.get(url)
#     response.raise_for_status()
#     members=response.json()
#     return render_template("members/list.html", members=members)

@blueprint.route("/members",methods = ["GET","POST"])
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
        print(idType)
        api = current_app.config.get('api')
        session = current_app.config.get('session')
        url = api.members
        response = session.post(url, json = {"govtId":govtId,"idType":idType,"firstName":firstName,"lastName":lastName,"middleName":middleName,"isCore":isCore,"phone":phone,"email":email})
        #response.raise_for_status()
        response = session.get(url)
        response.raise_for_status()
        members=response.json()
        return render_template("members/list.html", members=members)


