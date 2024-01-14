import logging
import unittest

from paraback.scraping.law_builder import LawBuilder


class LawBuilderTest(unittest.TestCase):
    def test_eWpG_parsing(self):
        law_content = open("./resources/eWpG.html", "r").read()
        law = LawBuilder.build_law(law_content)
        assert(law.abbreviation == "eWpG")

if __name__ == '__main__':
    unittest.main()
