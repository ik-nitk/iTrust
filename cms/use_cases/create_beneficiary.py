from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
)

def create_new_beneficiary(repo,fname,mname,lname,phone,email):
    try:
        id = repo.create_beneficiary(fname,mname,lname,phone,email)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)