import unittest
from paraback.linking.hybrid_textspan_linker import HybridTSLinker
from paraback.models.law_model import TextSpan, Link

def get_links(text):
    span = TextSpan(parent_id="DE-eWpG-Par28-Sec2-Enum4-Litb-SubLit1a", text=text)
    linker = HybridTSLinker(span)
    linker.link()
    return span.links

class LinkerTest(unittest.TestCase):

    def test_one_reference_internal(self):
        links = get_links("Im Fall einer Sammeleintragung § 6 Absatz 2 Satz 3 als Inhaber. Eine Eintragung in das Handelsregister wird dann wirksam.")
        self.assertEqual("DE-eWpG-Par6-Sec2-Sent3", links[0].url)
        self.assertEqual(1, len(links))
        self.assertEqual(31, int(links[0].start_idx))
        self.assertEqual(50, int(links[0].stop_idx))

    def test_one_reference_external(self):
        links = get_links("Im Fall einer Sammeleintragung § 6 Absatz 2 Satz 3 des Depotgesetzes. Eine Eintragung in das Handelsregister wird dann wirksam.")
        self.assertEqual("DE-DepotG-Par6-Sec2-Sent3", links[0].url)
        self.assertEqual(1, len(links))
        self.assertEqual(31, int(links[0].start_idx))
        self.assertEqual(68, int(links[0].stop_idx))

if __name__ == '__main__':
    unittest.main()