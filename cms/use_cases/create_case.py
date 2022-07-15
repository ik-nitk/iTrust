from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
)

def create_new_case(repo, beneficiary_id, purpose, title, description):
    try:
        id = repo.create_case(beneficiary_id=beneficiary_id, purpose=purpose, title=title, description=description)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)