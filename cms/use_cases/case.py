from common.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

import os
from cms.domain.case_state import CaseState
from cms.domain.case_docs import CaseDocs
from cms.domain.doc_type import DocType
from cms.domain.comment_type import CommentType
from nanoid import generate
from cms.domain.case_votes import VoteType

MINIMUM_CASE_APPROVER_STR = os.environ.get("MINIMUM_CASE_APPROVER", "2")
MINIMUM_CASE_APPROVER = int(MINIMUM_CASE_APPROVER_STR)

def case_list_use_case(repo, request):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        cases = repo.case_list(filters=request.filters)
        return ResponseSuccess(cases)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def publish_case_use_case(repo, case_id, updated_by):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        if case.case_state is not CaseState.DRAFT:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Publishing non Draft case is not allowed!!")
        ## change case state to publish.
        repo.update_case_state(case_id, CaseState.PUBLISHED, updated_by)
        return ResponseSuccess('case_published')
    except Exception as e:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

def add_case_verification_details(repo, case_id, comment, verification_by):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        if case.case_state is not CaseState.PUBLISHED:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Verification comments now not allowed")
        comment_id = repo.create_case_comment(case_id, comment_type=CommentType.VERIFICATION_COMMENTS, comment=comment, comment_data={}, c_by=verification_by)
        repo.update_case_state(case_id, CaseState.VERIFICATION, verification_by)
        return ResponseSuccess(comment_id)
    except Exception as e:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


def close_case_with_details(repo, case_id, comment, closed_by):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        member = repo.find_member(closed_by)
        if not member.is_core:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Non Core member cannot close the case")
        comment_id = repo.create_case_comment(case_id, comment_type=CommentType.CLOSING_COMMENTS, comment=comment, comment_data={}, c_by=closed_by)
        repo.update_case_state(case_id, CaseState.CLOSE, closed_by)
        return ResponseSuccess(comment_id)
    except Exception as e:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

def comment_list(repo, case_id, comment_type):
    try:
        comments = repo.case_comment_list(case_id, comment_type)
        return ResponseSuccess(comments)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def add_vote(repo, case_id, vote, comment, amount_suggested, created_by):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        if  case.case_state is not CaseState.VOTING and case.case_state is not CaseState.VERIFICATION:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Voting not allowed")
        vote_id = repo.upsert_case_vote(case_id, vote,comment, amount_suggested, created_by)
        if case.case_state is CaseState.VERIFICATION:
            repo.update_case_state(case_id, CaseState.VOTING, created_by)
        votes = repo.case_vote_list(case_id)
        total_approved = len([v for v in votes if v.is_core and v.vote is VoteType.APPROVE])
        total_rejected = len([v for v in votes if v.is_core and v.vote is VoteType.REJECT])
        if total_approved >= MINIMUM_CASE_APPROVER or total_rejected >= MINIMUM_CASE_APPROVER:
            if total_approved > total_rejected:
                repo.update_case_state(case_id, CaseState.APPROVED, created_by)
            else:
                repo.update_case_state(case_id, CaseState.REJECTED, created_by)
        return ResponseSuccess(vote_id)
    except Exception as e:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

def vote_list(repo, case_id):
    try:
        votes = repo.case_vote_list(case_id)
        return ResponseSuccess(votes)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def add_initial_documents_use_case(repo, case_id, created_by, doc_list):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        if case.case_state is not CaseState.DRAFT:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Adding documents after case is published is not allowed")
        case_docs = [
            CaseDocs(
                case_id=case_id,
                doc_id=f"i.doc.{generate()}",
                doc_url=i["doc_url"],
                doc_name=i["doc_name"],
                doc_type=DocType.INITIAL_CASE_DOC,
                updated__by=created_by
            )
            for i in doc_list
        ]
        repo.add_case_docs(case_docs)
        return ResponseSuccess('docs_added')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)


def add_payment_details_use_case(repo, case_id, comment, amount_paid, created_by, doc_list):
    try:
        case = repo.find_case(case_id)
        if case is None:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Case not found")
        if case.case_state is not CaseState.APPROVED:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Payment for non approved case is not allowed")
        member = repo.find_member(created_by)
        if not member.is_core:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, "Non Core member cannot add payment details")
        case_docs = [
            CaseDocs(
                case_id=case_id,
                doc_id=f"i.doc.{generate()}",
                doc_url=i["doc_url"],
                doc_name=i["doc_name"],
                doc_type=DocType.CASE_PAYMENT_RECEIPTS,
                updated__by=created_by
            )
            for i in doc_list
        ]
        repo.add_case_docs(case_docs)
        repo.update_approved_amount(case_id, amount_paid, created_by)
        comment_id = repo.create_case_comment(case_id, comment_type=CommentType.PAYMENT_COMMENTS, comment=comment, comment_data={}, c_by=created_by)
        repo.update_case_state(case_id, CaseState.PAYMENT_DONE, created_by)
        return ResponseSuccess(comment_id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def doc_list(repo, case_id, doc_type=DocType.INITIAL_CASE_DOC):
    try:
        docs = repo.case_doc_list(case_id, doc_type)
        return ResponseSuccess(docs)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def create_new_case(repo, beneficiary_id, purpose, title, description, amount_needed, created_by):
    try:
        id = repo.create_case(beneficiary_id=beneficiary_id, purpose=purpose, title=title, created_by=created_by, description=description,amount_needed = amount_needed)
        return ResponseSuccess(id)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

def view_case(repo, case_id):
    try:
        case = repo.find_case(case_id)
        if case is None:
            raise Exception("Case not found")
        return ResponseSuccess(case)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)