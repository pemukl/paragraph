import unittest
from unittest.mock import Mock

import pytest

from paraback.llmconnection.name_preprocessor import NamePreprocessor
from paraback.models.law_model import Law



class LawBuilderTest(unittest.TestCase):
    @pytest.mark.slow
    def test_declination(self):

        law = Mock(abbreviation="eWpG", title="Gesetz über elektronische Wertpapiere")
        np = NamePreprocessor(law)
        variants = np.get_variants()
        assert "Gesetzes über elektronische Wertpapiere" in variants

    @pytest.mark.slow
    def test_mult_declination(self):

        law1 = Mock(abbreviation="eWpG", stemmedabbreviation="ewpg", title="Gesetz über elektronische Wertpapiere")
        law2 = Mock(abbreviation="StGB", stemmedabbreviation="stgb", title="Strafgesetzbuch")
        names_dict = NamePreprocessor.get_all_names([law1, law2])
        assert names_dict["Gesetzes über elektronische Wertpapiere"] == "ewpg"
        assert names_dict["Strafgesetzbuch"] == "stgb"



if __name__ == '__main__':
    unittest.main()

