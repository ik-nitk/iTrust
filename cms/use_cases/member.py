from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

def create_new_member(repo,govt_id,id_type,fname,mname,lname,is_core,phone,email, created_by):
    try:
        id = repo.create_member(govt_id,id_type,fname,mname,lname,is_core,phone,email, created_by)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def member_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        members = repo.member_list(filters=request.filters)
        return ResponseSuccess(members)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def search_member(repo, search_input):
    try:
        member = repo.search_member(search_input)
        return ResponseSuccess(member)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def view_member(repo, member_id):
    try:
        member = repo.view_member(member_id)
        return ResponseSuccess(member)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def view_member_by_email(repo, email_id):
    try:
        member = repo.view_member_by_email(email_id)
        return ResponseSuccess(member)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def update_member(repo, member_id,govt_id,id_type,fname,mname,lname,is_core,phone,email, updated_by):
    try:
        member = repo.update_member(member_id,govt_id,id_type,fname,mname,lname,is_core,phone,email, updated_by)
        return ResponseSuccess(member)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
