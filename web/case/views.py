from flask import Blueprint, render_template, current_app, request, redirect, url_for

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

@blueprint.route("/cases/create",methods = ["GET","POST"])
def create_case():
    if request.method == 'GET':
        return render_template("cases/create.html")
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

