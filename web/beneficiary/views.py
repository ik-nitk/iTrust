from crypt import methods
from flask import Blueprint, render_template, current_app, request

blueprint = Blueprint(
            'beneficiary',
             __name__
        )

# @blueprint.route("/beneficiaries")
# def beneficiary_list_view():
#     api = current_app.config.get('api')
#     session = current_app.config.get('session')
#     url = api.beneficiaries
#     response = session.get(url)
#     response.raise_for_status()
#     beneficiaries=response.json()
#     #print(f'=====================///////////////////////////-------------------{url}--------{response}-------==========')
#     return render_template("beneficiaries/list.html", beneficiaries=beneficiaries)

@blueprint.route("/beneficiaries",methods = ["GET","POST"])
def create_beneficiary():
    if request.method == 'GET':
        return render_template("beneficiaries/create.html")
    else:
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        middleName = request.form.get('middle_name')
        phone = request.form.get('phone_no')
        email = request.form.get('email')
        api = current_app.config.get('api')
        session = current_app.config.get('session')
        url = api.beneficiaries
        response = session.post(url, json = {"firstName":firstName,"lastName":lastName,"middleName":middleName,"phone":phone,"email":email})
        response.raise_for_status()
        response = session.get(url)
        response.raise_for_status()
        beneficiaries=response.json()
        return render_template("beneficiaries/list.html", beneficiaries=beneficiaries)




