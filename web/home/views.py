from flask import Blueprint, render_template, current_app, request, redirect, url_for, Response
import requests

blueprint = Blueprint(
            'home',
             __name__
        )

@blueprint.route("/")
def home_page():
    api = current_app.config.get('api')
    session = current_app.config.get('session')
    url = api.case_list_from_case_state('PUBLISHED')
    print(url)
    response = session.get(url)
    response.raise_for_status()
    cases = response.json()
    print(cases)
    return render_template("home/index.html",cases = cases)