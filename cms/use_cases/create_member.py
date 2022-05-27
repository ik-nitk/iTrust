from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
)

def create_new_member(repo,govt_id,id_type,fname,mname,lname,is_core,phone,email):
    try:
        id = repo.create_member(govt_id,id_type,fname,mname,lname,is_core,phone,email)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)