from application.activity import app1
from database import MongoDBManager
import domainman
import solutionman
import userman


if __name__ == "__main__":
    dbManager = MongoDBManager()
    dbManager.drop_collections()
    dbManager.init_collections()

    userman.post_user1()

    domainman.post_domain1()
    domainman.post_domain2()

    solutionman.post_solution1()
    solutionman.post_solution2()
    solutionman.post_solution3()

    app1.request()
