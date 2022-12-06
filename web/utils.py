from flask import session, abort, render_template, current_app
import json


def get_member_id_with_email(api, app_session, email):
    url = api.member_email_id(email)
    response = app_session.get(url)
    response.raise_for_status()
    return response.json()

def get_beneficiary_details(api, app_session, id):
    url = api.beneficiary_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    beneficiaries = response.json()
    assert beneficiaries and len(beneficiaries) > 0, "Invalid beneficiary_id"
    return beneficiaries[0]

def get_member_details(api, app_session, id):
    url = api.member_id(id)
    response = app_session.get(url)
    response.raise_for_status()
    member = response.json()
    assert member and len(member) > 0, "Invalid member_id"
    return member[0]

def get_member_from_session():
    if "google_id" not in session:
        raise Exception("Please login to create member")
    api = current_app.config.get('api')
    app_session = current_app.config.get('app_session')
    member_array = get_member_id_with_email(api, app_session, session["google_id"])
    if not member_array:
        raise Exception("You need to be a member to perform this operation")
    return member_array[0]

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            return abort(401)
        else:
            return function()

    return wrapper