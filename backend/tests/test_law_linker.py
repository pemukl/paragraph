import os.path
import unittest

from paraback.linking.law_linker import LawLinker
from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.scraping.law_builder import LawBuilder
from paraback.util import get_project_root


class LawLinkerTest(unittest.TestCase):
    def test_eWpG_linking(self):
        law_content = open(os.path.join(get_project_root(),'tests/resources/eWpG.html'), "r").read()
        law = LawBuilder.build_law(law_content)

        law_linker = LawLinker(law)
        law_linker.link()


if __name__ == '__main__':
    unittest.main()
