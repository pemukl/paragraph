import unittest

from paraback.models.law_model import TextSpan, Link
from paraback.linking.textspan_linker import TextspanLinker
from paraback.linking.regex_textspan_linker import RegexTSLinker


class LinkerTest(unittest.TestCase):
    def test_parsing(self):
        res = TextspanLinker.parse_link_to_dict("DE-eWpG-Par28-Sec2-Enum4-Litb-SubLit1a")
        self.assertEqual(res["jurisdiction"], "DE")
        self.assertEqual(res["law"], "eWpG")
        self.assertEqual(res["par"], "28")
        self.assertEqual(res["sec"], "2")
        self.assertEqual(res["enum"], "4")
        self.assertEqual(res["lit"], "b")
        self.assertEqual(res["sublit"], "1a")

    def test_joining(self):
        context = TextSpan(parent_id="DE-eWpG-Par28-Sec2-Enum4-Litb-SubLit1a", text="something")
        shortlink = Link(url="Sec4-Sent3",start_idx=0,stop_idx=9,parent_id=context.id)
        linker = RegexTSLinker(context)
        res = linker.root_link(shortlink)
        self.assertEqual("DE-eWpG-Par28-Sec4-Sent3",res.url)


if __name__ == '__main__':
    unittest.main()
