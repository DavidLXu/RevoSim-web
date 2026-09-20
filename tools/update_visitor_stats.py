"""Aggregate this site's public Flag Counter country totals; never load its tracking image."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
COUNTER = 'E6wN'
HOST = 'https://s01.flagcounter.com'
CONTINENTS = {'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America',
              'SA': 'South America', 'OC': 'Oceania', 'AN': 'Antarctica', 'UN': 'Unknown'}


def parse_page(html):
    coverage = re.search(r'Countries\s+(\d+)\s*-\s*(\d+)\s+of\s+(\d+)\.', html)
    if not coverage:
        raise ValueError('Country table missing; keep the last successful snapshot')
    first, last, total = map(int, coverage.groups())
    rows = re.findall(
        rf'href=[\'\"]?/factbook/([a-z0-9]{{2}})/{COUNTER}\b[^>]*>.*?</a>\s*</font>\s*</td>'
        r'\s*<td\b[^>]*>\s*<font\b[^>]*>\s*([\d,]+)\s*</font>',
        html, re.IGNORECASE | re.DOTALL)
    countries = {code.upper(): int(count.replace(',', '')) for code, count in rows}
    if len(countries) != last-first+1:
        raise ValueError('Incomplete or duplicate country rows')
    return countries, first, last, total


def fetch_countries():
    countries = {}
    previous_last = 0
    for page in range(1, 9):
        url = f'{HOST}/countries/{COUNTER}/' + (str(page) if page > 1 else '')
        request = Request(url, headers={'User-Agent': 'RevoSim-Visitor-Summary/1.0 (github.com/DavidLXu/RevoSim-web)'})
        with urlopen(request, timeout=30) as response:
            html = response.read().decode('utf-8')
        batch, first, last, total = parse_page(html)
        if first != previous_last+1 or countries.keys() & batch.keys():
            raise ValueError('Country pagination changed during fetch')
        countries.update(batch)
        previous_last = last
        if last == total:
            return countries
    raise ValueError('Unexpected number of country pages')


def aggregate(countries, mapping):
    totals = {code: 0 for code in CONTINENTS}
    for country, count in countries.items():
        code = mapping.get(country, 'UN')
        totals[code if code in totals else 'UN'] += count
    assert sum(totals.values()) == sum(countries.values())
    return totals


def main():
    countries = fetch_countries()
    mapping = json.loads((ROOT/'tools/country-continents.json').read_text())['countries']
    output = ROOT/'assets/visitor-stats.json'
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    previous = json.loads(output.read_text()) if output.exists() else {}
    total = sum(countries.values())
    if total < previous.get('total_visits', 0):
        raise ValueError('Counter decreased or reset; keep previous snapshot for review')
    payload = {'provider': 'Flag Counter', 'counter_id': COUNTER,
               'statistics_url': f'https://info.flagcounter.com/{COUNTER}',
               'started_at': previous.get('started_at', now), 'updated_at': now,
               'metric': 'Recorded visits; repeat visitors may count again after 24 hours',
               'total_visits': total, 'countries_count': len(countries),
               'continents': aggregate(countries, mapping), 'countries': countries}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
    print(f'Updated {total} recorded visits across {len(countries)} countries.')


if __name__ == '__main__':
    main()
