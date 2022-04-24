from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
)

def create_new_document(repo, filename, user):
    try:
        id = repo.insert_document(filename, user)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def find_document(repo, id):
    try:
        document = repo.find_document(id)
        return ResponseSuccess(document)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)