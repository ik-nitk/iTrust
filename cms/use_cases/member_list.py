from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)


def member_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        members = repo.member_list(filters=request.filters)
        return ResponseSuccess(members)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
