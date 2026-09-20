"""Publish aggregate GoatCounter location counts; credentials stay in Actions secrets."""
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://davidlxu.goatcounter.com'
START = '2026-09-20T00:00:00Z'
PATH = '/RevoSim-web/'
CONTINENTS = ('AF', 'AS', 'EU', 'NA', 'SA', 'OC', 'AN', 'UN')


def parse_page(payload):
    if not isinstance(payload, dict) or type(payload.get('more')) is not bool or not isinstance(payload.get('stats'), list):
        raise ValueError('Invalid GoatCounter location response')
    countries = {}
    for row in payload['stats']:
        code, count = row.get('id'), row.get('count')
        if not isinstance(code, str) or type(count) is not int or count < 0:
            raise ValueError('Invalid location count')
        code = code.upper()
        # GoatCounter uses an empty/unknown label for unlocated visits.
        if code in ('', 'UNKNOWN', '(UNKNOWN)'):
            code = 'ZZ'
        if not re.fullmatch(r'[A-Z]{2}', code) or code in countries:
            raise ValueError('Unexpected or duplicate country code')
        countries[code] = count
    if payload['more'] and not countries:
        raise ValueError('Empty non-final page')
    return countries, payload['more']


def fetch_countries(request_page):
    countries = {}
    offset = 0
    for _ in range(5):
        batch, more = parse_page(request_page(offset))
        if countries.keys() & batch.keys():
            raise ValueError('Country pagination changed during fetch')
        countries.update(batch)
        if not more:
            return countries
        offset += len(batch)
    raise ValueError('Unexpected number of country pages')


def aggregate(countries, mapping):
    totals = dict.fromkeys(CONTINENTS, 0)
    for country, count in countries.items():
        code = mapping.get(country, 'UN')
        totals[code if code in totals else 'UN'] += count
    return totals


def main():
    token = os.environ.get('GOATCOUNTER_API_TOKEN', '').strip()
    if not token:
        raise RuntimeError('Configure the GOATCOUNTER_API_TOKEN Actions secret')
    now = datetime.now(timezone.utc)
    end = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).isoformat()

    def request_page(offset):
        query = urlencode({'start': START, 'end': end, 'include_paths': PATH,
                           'path_by_name': 'true', 'limit': 100, 'offset': offset})
        request = Request(f'{SITE}/api/v0/stats/locations?{query}', headers={
            'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
            'User-Agent': 'RevoSim-Public-Statistics/2.0'})
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            detail = error.read().decode('utf-8', errors='replace')[:1000]
            raise RuntimeError(f'GoatCounter HTTP {error.code}: {detail}') from None

    countries = fetch_countries(request_page)
    mapping = json.loads((ROOT/'tools/country-continents.json').read_text())['countries']
    known = sum(1 for code, count in countries.items() if count > 0 and code in mapping)
    payload = {'provider': 'GoatCounter', 'site': SITE, 'path': PATH,
               'started_at': START, 'updated_at': now.isoformat(timespec='seconds'),
               'metric': 'GoatCounter location visits; not all-time unique people',
               'total_visits': sum(countries.values()), 'countries_count': known,
               'continents': aggregate(countries, mapping), 'countries': countries}
    output = ROOT/'assets/visitor-stats.json'
    temporary = output.with_suffix('.tmp')
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
    temporary.replace(output)
    print(f"Updated {payload['total_visits']} visits across {known} countries and territories.")


if __name__ == '__main__':
    main()
