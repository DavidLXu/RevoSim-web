import unittest
from update_visitor_stats import parse_page, fetch_countries, aggregate


class VisitorStatsTests(unittest.TestCase):
    def test_real_empty_result(self):
        self.assertEqual(parse_page({'stats': [], 'more': False}), ({}, False))

    def test_malformed_result_is_not_zero_traffic(self):
        for payload in [{}, {'error': 'unauthorized'}, {'stats': [], 'more': True},
                        {'stats': [{'id':'JP','count':-1}], 'more':False},
                        {'stats': [{'id':'JP','count':True}], 'more':False},
                        {'stats': [{'id':'JP','count':1}]*2, 'more':False}]:
            with self.assertRaises(ValueError):
                parse_page(payload)

    def test_pagination(self):
        offsets = []
        def page(offset):
            offsets.append(offset)
            return {'stats': [{'id': 'JP' if offset == 0 else 'US', 'count': 3}], 'more': offset == 0}
        self.assertEqual(fetch_countries(page), {'JP':3, 'US':3})
        self.assertEqual(offsets, [0, 1])

    def test_repeated_page_rejected(self):
        with self.assertRaises(ValueError):
            fetch_countries(lambda _: {'stats':[{'id':'JP','count':1}], 'more':True})

    def test_unknowns_preserve_total(self):
        result = aggregate({'US':5,'JP':3,'ZZ':2}, {'US':'NA','JP':'AS'})
        self.assertEqual((result['NA'], result['AS'], result['UN']), (5,3,2))
        self.assertEqual(sum(result.values()),10)
        self.assertEqual(result['AN'],0)


if __name__ == '__main__':
    unittest.main()
