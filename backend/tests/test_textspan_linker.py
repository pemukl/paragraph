import unittest

from paraback.models.law_model import TextSpan, Link
from paraback.linking.textspan_linker import TextspanLinker
from paraback.linking.regex_ts_linker import RegexTSLinker


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
        res = linker.short_to_long_link(shortlink)
        self.assertEqual("DE-eWpG-Par28-Sec4-Sent3",res.url)

    def test_finding(self):
        span = TextSpan(parent_id="DE-eWpG-Par28-Sec2-Enum4-Litb-SubLit1a", text="Im Fall einer Sammeleintragung § 6 Absatz 2 Satz 3 als Inhaber.")
        linker = RegexTSLinker(span)
        linker.link()
        self.assertEqual("DE-eWpG-Par6-Sec2-Sent3", span.links[0].url)
        self.assertEqual(1, len(span.links))
        self.assertEqual(31, int(span.links[0].start_idx))
        self.assertEqual(50, int(span.links[0].stop_idx))

if __name__ == '__main__':
    unittest.main()