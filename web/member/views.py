from flask import Blueprint, render_template, current_app
import json

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