import unittest
from update_visitor_stats import parse_page, aggregate


def row(code, count):
    return f'<a href=/factbook/{code}/E6wN><u>Country</u></a></font></td><td width=1%><font face=arial size=2>{count}</font></td>'


class VisitorStatsTests(unittest.TestCase):
    def test_country_totals_ignore_region_rows(self):
        html = 'Countries 1 - 2 of 2.' + row('us', '1,024') + '<tr><td>California</td><td>400</td></tr>' + row('jp', '9')
        self.assertEqual(parse_page(html), ({'US': 1024, 'JP': 9}, 1, 2, 2))

    def test_incomplete_and_duplicate_rows_are_rejected(self):
        for html in ['Countries 1 - 2 of 2.'+row('us','5'),
                     'Countries 1 - 2 of 2.'+row('us','5')+row('us','8'),
                     '<html>Temporarily unavailable</html>']:
            with self.assertRaises(ValueError):
                parse_page(html)

    def test_later_page_range(self):
        self.assertEqual(parse_page('Countries 51 - 51 of 51.'+row('au','7'))[1:], (51, 51, 51))

    def test_unknowns_preserve_total(self):
        result = aggregate({'US':5,'JP':3,'ZZ':2}, {'US':'NA','JP':'AS'})
        self.assertEqual((result['NA'],result['AS'],result['UN']), (5,3,2))
        self.assertEqual(sum(result.values()),10)
        self.assertEqual(result['AN'],0)


if __name__ == '__main__':
    unittest.main()
