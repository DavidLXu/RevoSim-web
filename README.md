# RevoSim

Project website for **RevoSim: Scalable Multimodal Tactile Simulation for Dexterous Manipulation**.

The site presents five tactile modalities, synchronized contact examples, and manipulation videos with LeRobot data collection support. The paper is coming soon.

Website: [davidlxu.github.io/RevoSim-web](https://davidlxu.github.io/RevoSim-web/)

GitHub Actions publishes the static files from the `main` branch to GitHub Pages. Asset links are relative so the site works under `/RevoSim-web/`.

## Public visitor statistics

GoatCounter records visits to the production project page. Local previews and the old Sites preview do not load analytics. The small footer disclosure is collapsed by default; expanding it loads a public aggregate snapshot and shows a continent map and counts. Collapsing the display does not disable analytics. The disclosure links to GoatCounter's privacy policy.

The dashboard is https://davidlxu.goatcounter.com/. `analytics.js` always records the canonical `/RevoSim-web/` path, so cache-busting query strings and section anchors do not create separate pages.

`tools/update_visitor_stats.py` uses GoatCounter's read-only location statistics API, filtered to `/RevoSim-web/`, from 20 September 2026 (UTC). It publishes only aggregate country and continent counts. Visits are GoatCounter's location metric, not all-time unique people. Totals start with this integration; previous Flag Counter counts are archived separately in `tools/archive/flagcounter-final.json` and are not mixed with GoatCounter data.

The API token is stored only in the repository's GitHub Actions secret `GOATCOUNTER_API_TOKEN`. Its permissions are **Read statistics**, restricted to **davidlxu.goatcounter.com**. To rotate it, create a replacement under GoatCounter → account → API, update the Actions secret, verify a successful refresh, then revoke the old token. Never put tokens in frontend files or commit them.

The Pages workflow refreshes totals hourly at minute 17 UTC, then publishes the static site. GitHub can delay scheduled jobs or disable them after prolonged repository inactivity; use Actions → Publish site and refresh visitor statistics → Run workflow to refresh manually. API errors preserve the previous snapshot and its original timestamp. A missing snapshot displays unavailable, never fabricated zero counts.

Countries and territories are assigned to continents using [GeoNames countryInfo](https://download.geonames.org/export/dump/countryInfo.txt), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Unrecognized countries are retained in an Unknown bucket. Map outlines derive from [Natural Earth 1:110m countries](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson), public domain. Map shading applies each continent's total to its countries; it does not show individual visitor positions.
