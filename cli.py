#!/usr/bin/env python

import pprint
from cms.repository.memrepo import MemRepo
from cms.domain.id_type import IDType
from cms.use_cases.member_list import member_list_use_case
from cms.requests.member_list import build_member_list_request

members = [
        {
            "member_id": "i.mem.1111",
            "fname": 'fname1',
            "lname": 'lname1',
            "govt_id": 'abcd1111',
            "id_type": IDType.AADHAAR,
            "phone" : "984561111",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.1111@gmail.com'
         },
         {
            "member_id": "i.mem.2222",
            "fname": 'fname2',
            "lname": 'lname2',
            "govt_id": 'abcd2222',
            "id_type": IDType.AADHAAR,
            "phone" : "984562222",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.2222@gmail.com'
         },
         {
            "member_id": "i.mem.3333",
            "fname": 'fname3',
            "lname": 'lname3',
            "govt_id": 'abcd3333',
            "id_type": IDType.AADHAAR,
            "phone" : "984563333",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.3333@gmail.com'
         },
         {
            "member_id": "i.mem.4444",
            "fname": 'fname4',
            "lname": 'lname4',
            "govt_id": 'abcd4444',
            "id_type": IDType.AADHAAR,
            "phone" : "984564444",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.4444@gmail.com'
         },
]

request = build_member_list_request()
repo = MemRepo(members)
pp = pprint.PrettyPrinter(indent=2)
response = member_list_use_case(repo, request)
pp.pprint([member.to_dict() for member in response.value])
