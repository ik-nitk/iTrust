from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

from cms.domain.case_state import CaseState
from cms.domain.case_docs import CaseDocs
from cms.domain.doc_type import DocType
from nanoid import generate

def case_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        cases = repo.case_list(filters=request.filters)
        return ResponseSuccess(cases)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)


def add_initial_documents(repo, case_id, doc_list):
    try:
        case = repo.find_case(case_id=case_id)
        if case.case_state is not CaseState.DRAFT:
            raise Exception("Adding documents after case is published is not allowed")
        case_docs = [
            CaseDocs(
                case_id=case_id,
                doc_id=f"i.doc.{generate()}",
                doc_url=i["doc_url"],
                doc_name=i["doc_name"],
                doc_type=DocType.INITIAL_CASE_DOC
            )
            for i in doc_list
        ]
        repo.add_case_docs(case_docs)
        return ResponseSuccess('docs_added')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def doc_list(repo, case_id):
    try:
        docs = repo.case_doc_list(case_id=case_id)
        return ResponseSuccess(docs)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def create_new_case(repo, beneficiary_id, purpose, title, description):
    try:
        id = repo.create_case(beneficiary_id=beneficiary_id, purpose=purpose, title=title, description=description)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)