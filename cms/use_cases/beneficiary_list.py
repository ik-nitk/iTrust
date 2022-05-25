from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request, 
)


def beneficiary_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        beneficiaries = repo.beneficiary_list(filters=request.filters)
        return ResponseSuccess(beneficiaries)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
