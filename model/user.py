import uuid

from pymongo import MongoClient

ATTRIBUTES = {'email', 'password', 'name', 'apikey', 'status'}
REQ_ATTRIBUTES = {'email', 'password', 'name'}


class UserManager:
    """ Manage users.
    """

    def __init__(self):
        self.db = MongoClient().INFaaS.users

    def add_user(self, user):
        if user.keys() >= REQ_ATTRIBUTES:
            res = self.db.insert_one({k: v for k, v in user.items() if k in ATTRIBUTES})
            return res.acknowledged
        return False

    def get_user(self, email=None, password=None, apikey=None, status=None):
        query = {}
        if email:
            query.update({'email': email})
        if password:
            query.update({'password': password})
        if apikey:
            query.update({'apikey': apikey})
        if status:
            query.update({'status': status})
        return self.db.find_one(query)

    def update_user(self, user):
        # if the entered solution is not valid, return False.
        if not self._verify_user(user):
            return False

        query = {'_id': user.get('_id')}
        new = {k: v for k, v in user.items() if k in ATTRIBUTES}
        res = self.db.replace_one(query, new)
        return True if res.modified_count > 0 else False

    def generate_apikey(self, user):
        email = user.get('email')
        if not email:
            return False
        apikey = str(uuid.uuid5(uuid.NAMESPACE_URL, email))
        self.db.update_one({'email': email}, {'$set': {'apikey': apikey}})

    @staticmethod
    def _verify_user(user):
        if not user:
            return False
        return True


if __name__ == '__main__':
    m = UserManager()
    # m.add_user({'email': "mkdmkk@gmail.com", 'password': '1234', 'name': "Moon Kwon Kim"})
    m.generate_apikey({'email': "mkdmkk@gmail.com", 'password': '1234', 'name': "Moon Kwon Kim"})
    print(m.get_user(email="mkdmkk@gmail.com"))
