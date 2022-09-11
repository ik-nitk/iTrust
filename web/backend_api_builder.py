class BackendApiBuilder:
    """ Responsible for Building parametrised endpoints for backend application """

    def __init__(self):
        self.host = "application"
        self.port = 8000
        self.base = 'http://{}:{}/api/v1/'.format(self.host, self.port)

    @property
    def members(self):
        """
        Generates endpoint for creating members resource
        :return: create members endpoint
        """
        return self.base + 'members'

    def member_id(self, member_id):
        """
        Generates endpoint for retrieving/updating task with given member_id
        :param member_id: unique member id
        :return: member endpoint
        """
        return self.members + '/{}'.format(member_id)

    @property
    def member_search(self):
        return self.members + '/search'

    @property
    def beneficiaries(self):
        """
        Generates endpoint for creating beneficiaries resource
        :return: create beneficiaries endpoint
        """
        return self.base + 'beneficiaries'

    def beneficiary_id(self, beneficiary_id):
        """
        Generates endpoint for retrieving/updating task with given beneficiary_id
        :param beneficiary_id: unique beneficiary id
        :return: member endpoint
        """
        return self.beneficiaries + '/{}'.format(beneficiary_id)

    @property
    def beneficiary_search(self):
        return self.beneficiaries + '/search'

    @property
    def cases(self):
        """
        Generates endpoint for creating cases resource
        :return: create cases endpoint
        """
        return self.base + 'cases'

    def case_initial_docs(self, case_id):
        return self.cases + '/{}'.format(case_id) + '/add_initial_documents'

    def case_verification_details(self, case_id):
         return self.cases + '/{}'.format(case_id) + '/add_case_verification_details'

    def publish_case(self, case_id):
        return self.cases + '/{}'.format(case_id) + '/publish'

    def case_doc_list(self, case_id, doc_type):
        return self.case_id(case_id) + '/docs?doc_type={}'.format(doc_type)

    def case_comment_list(self, case_id, comment_type=None):
        if comment_type == None:
            return self.case_id(case_id) + '/comments'
        return self.case_id(case_id) + '/comments?comment_type={}'.format(comment_type)

    def case_id(self, case_id):
        """
        Generates endpoint for retrieving/updating task with given cases_id
        :param cases_id: unique cases id
        :return: case endpoint
        """
        return self.cases + '/{}'.format(case_id)
