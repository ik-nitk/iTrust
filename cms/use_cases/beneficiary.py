from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

def create_new_beneficiary(repo,govt_id, id_type, fname,mname,lname,phone,email, created_by):
    try:
        id = repo.create_beneficiary(govt_id, id_type, fname,mname,lname,phone,email, created_by)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def beneficiary_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        beneficiaries = repo.beneficiary_list(filters=request.filters)
        return ResponseSuccess(beneficiaries)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)


def search_beneficiary(repo, search_input):
    try:
        member = repo.search_beneficiary(search_input)
        return ResponseSuccess(member)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def view_beneficiary(repo, beneficiary_id):
    try:
        beneficiary = repo.view_beneficiary(beneficiary_id)
        return ResponseSuccess(beneficiary)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def update_beneficiary(repo, beneficiary_id,govt_id, id_type, fname,mname,lname,phone,email, updated_by):
    try:
        beneficiary = repo.update_beneficiary(beneficiary_id, govt_id, id_type, fname,mname,lname,phone,email, updated_by)
        return ResponseSuccess(beneficiary)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

