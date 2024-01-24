import logging
import os
import unittest

from paraback.models.law_model import Law
from paraback.saving.mongo_connector import MongoConnector
from paraback.util import get_project_root
import json


class LawBuilderTest(unittest.TestCase):
    def test_db_rw(self):
        path = os.path.join(get_project_root(), 'tests/resources/eWpG.json')
        with open(path, "r") as f:
            law_content = f.read()
        law = Law.model_validate(json.loads(law_content))

        io = MongoConnector()
        io.write(law)
        res = io.read(law.stemmedabbreviation)

        assert(res.longname == law.longname)



if __name__ == '__main__':
    unittest.main()
