from flask import Blueprint, render_template, current_app, request

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



