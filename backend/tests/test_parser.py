import logging
import os
import unittest

from paraback.saving.mongo_connector import MongoConnector
from paraback.scraping.law_builder import LawBuilder
from paraback.util import get_project_root


class LawBuilderTest(unittest.TestCase):
    def test_eWpG_parsing(self):
        path = os.path.join(get_project_root(), 'tests/resources/eWpG.html')
        law_content = open(path, "r").read()
        law = LawBuilder.build_law(law_content)
        assert(law.abbreviation == "eWpG")

if __name__ == '__main__':
    unittest.main()
