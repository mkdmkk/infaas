from pymongo import MongoClient

from INFaaS import constants

ATTRIBUTES = {'name', 'desc', 'features', 'situations'}


class DomainManager:
    """ Manage domains.
    The form of a domain
        name: human readable name of a domain; it should be unique.
        desc: description of a domain
        features: a list of features
        situations: a list of possible situations; possible inference results
    """

    def __init__(self):
        self.db = MongoClient().INFaaS.domains

    def add_domain(self, domain):
        verified = self._verify_domain(domain)
        if not verified or not set(domain.keys()) >= ATTRIBUTES:
            raise Exception(constants.MSG_INVALID_PARAMS)

        res = self.db.insert_one(domain)
        if res.acknowledged:
            return True
        return False

    def get_domains(self, name=None):
        query = {}
        if name:
            query.update({'name': name})
        domains = self.db.find(query)
        return domains

    def update_domain(self, domain):
        # if the entered solution is not valid, return False.
        if not self._verify_domain(domain):
            return False

        query = {'_id': domain.get('_id')}
        new = {k: v for k, v in domain.items() if k in ATTRIBUTES}
        res = self.db.replace_one(query, new)
        return True if res.modified_count > 0 else False

    def delete_domain(self, domain):
        query = {'_id': domain.get('_id')}
        res = self.db.delete_one(query)
        return True if res.deleted_count > 0 else False

    @staticmethod
    def _verify_domain(domain):
        if not domain:
            return False
        return True


if __name__ == '__main__':
    m = DomainManager()
    m.add_domain({'name': 'Iris example2', 'desc': "", 'features': ['patal length', 'height'], 'situations': ['1', '2']})