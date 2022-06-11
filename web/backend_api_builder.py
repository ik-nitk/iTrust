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
