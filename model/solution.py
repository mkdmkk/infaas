from pymongo import MongoClient

from INFaaS import constants

ATTRIBUTES = {
    'name', 'alg', 'dataset', 'situations', 'serialized_obj', 'desc', 'accuracy', 'domain',
    'owner', 'visibility', 'auth_users'
}


class SolutionManager:
    """ Manage solutions.
    The form of a solution
        name: human readable name of a solution
        alg: algorithm used; Ex.) logistic regression
        dataset: training/testing data as 2-d array shaped as [# of samples, # of features]
        situations: a list of situation labels for each sample in the dataset
        serialized_obj: serialized created model instance
        desc: description of a solution
        accuracy: accuracy determined after verifying a model with 70% training dataset and 30% testing dataset
        domain: domain of a solution
        owner: id of a user who create the solution
        visibility: public or private
        auth_users: users who are accessible to the solution even though the visibility is private
    """

    def __init__(self):
        self.db = MongoClient().infaas.solutions

    def add_solution(self, solution):
        # if the entered solution is not valid, return False.
        if not self._verify_solution(solution):
            return False

        res = self.db.insert_one(solution)
        if res.acknowledged:
            return True
        return False

    def get_solutions(self, name=None):
        query = {}
        if name:
            query.update({'name': name})
        solutions = self.db.find(query)
        return solutions

    def update_solution(self, solution):
        # if the entered solution is not valid, return False.
        if not self._verify_solution(solution):
            return False

        query = {'_id': solution.get('_id')}
        new = {k: v for k, v in solution.items() if k in ATTRIBUTES}
        res = self.db.replace_one(query, new)
        return True if res.modified_count > 0 else False

    def delete_solution(self, solution):
        query = {'_id': solution.get('_id')}
        res = self.db.delete_one(query)
        return True if res.deleted_count > 0 else False

    @staticmethod
    def _verify_solution(solution):
        if not solution:
            return False
        return False
