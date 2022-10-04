import json


class CaseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "case_state": o.case_state,
                "is_flagged": o.is_flagged,
                "is_urgent": o.is_urgent,
                "beneficiary__id": o.beneficiary__id,
                "purpose": o.purpose,
                "title": o.title,
                "description": o.description,
                "family_details": o.family_details,
                "amount_approved":o.amount_approved,
                "amount_needed":o.amount_needed,
                "avg_monthly_income": o.avg_monthly_income,
                "contact_details": o.contact_details,
                "contact_address": o.contact_address,
                "referred__by": o.referred__by,
                "closed__by": o.closed__by,
                "updated_by": o.updated_by
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)

class CaseDocsJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "doc_type": o.doc_type,
                "doc_id": o.doc_id,
                "doc_name": o.doc_name,
                "doc_url": o.doc_url
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)

class CaseCommentJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "comment": o.comment,
                "comment_id": o.comment_id,
                "comment_data": o.comment_data,
                "commented_by": o.commented_by,
                "comment_type": o.comment_type
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)

class CaseVoteJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "vote_id": o.vote_id,
                "voted_by": o.voted_by,
                "amount_suggested":o.amount_suggested,
                "vote": o.vote,
                "comment": o.comment
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)