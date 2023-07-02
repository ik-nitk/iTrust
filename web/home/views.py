
from flask import Blueprint, render_template, session, redirect, request, current_app
import requests
import os
from google.oauth2 import id_token
import json
from pip._vendor import cachecontrol
from concurrent.futures import ThreadPoolExecutor, wait
import google.auth.transport.requests

pool = ThreadPoolExecutor(10)
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
    flow.fetch_token(code=request.args['code'])

    if not session["state"] == request.args["state"]:
        #print (session["state"], request.args["state"])
        return render_template("error.html", error_msg=str('#state does not match!')), 500  #state does not match!

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


def get_case_list(api, app_session, state, limit=3):
    url = api.case_list_from_case_state(state, limit)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

@blueprint.route("/")
def home_page():
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    futures = []
    futures.append(pool.submit(get_case_list, api, app_session, 'CLOSE'))
    futures.append(pool.submit(get_case_list, api, app_session, 'PUBLISHED'))
    futures.append(pool.submit(get_case_list, api, app_session, 'VERIFICATION'))
    futures.append(pool.submit(get_case_list, api, app_session, 'VOTING'))
    futures.append(pool.submit(get_case_list, api, app_session, 'APPROVED'))
    futures.append(pool.submit(get_case_list, api, app_session, 'REJECTED'))
    futures.append(pool.submit(get_case_list, api, app_session, 'PAYMENT_DONE'))
    wait(futures)
    closed_cases = futures[0].result()
    published_cases = futures[1].result()
    verified_cases = futures[2].result()
    voting_cases = futures[3].result()
    approved_cases = futures[4].result()
    rejected_cases = futures[5].result()
    payment_done_cases = futures[6].result()
    return render_template("home/index.html",
        closed_cases = closed_cases,
        is_closed_cases=(len(closed_cases) > 0),
        published_cases = published_cases,
        is_published_cases = (len(published_cases) > 0),
        verified_cases = verified_cases,
        is_verified_cases = (len(verified_cases) > 0),
        voting_cases = voting_cases,
        is_voting_cases = (len(voting_cases) > 0),
        approved_cases = approved_cases,
        is_approved_cases = (len(approved_cases) > 0),
        rejected_cases = rejected_cases,
        is_rejected_cases = (len(rejected_cases) > 0),
        payment_done_cases = payment_done_cases,
        is_payment_done_cases = (len(payment_done_cases) > 0)
    )