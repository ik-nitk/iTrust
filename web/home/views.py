from flask import Blueprint, render_template, session, redirect, request, current_app
import requests
import os
from google.oauth2 import id_token
import json
from pip._vendor import cachecontrol
import google.auth.transport.requests


blueprint = Blueprint(
            'home',
             __name__
        )

@blueprint.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    if os.environ.get("AUTH_ENABLED", "false").lower() == "false":
        # nothing to do in case the authentication is disabled.
        return redirect("/")
    flow = current_app.config.get('FLOW')
    google_client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id
    )

    session["google_id"] = id_info.get("email")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    return redirect("/")  #the final page where the authorized users will end up

@blueprint.route("/logout")  #the logout page and function
def logout():
    session.clear()
    return redirect("/")

@blueprint.route("/login")  #the page where the user can login
def login():
    if os.environ.get("AUTH_ENABLED", "false").lower() == "false":
        session["google_id"] = "itrust_test@gmail.com"
        session["name"] = "itrust_test"
        return redirect("/")
    flow = current_app.config.get('FLOW')
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@blueprint.route("/")
def home_page():
    return render_template("home/index.html")