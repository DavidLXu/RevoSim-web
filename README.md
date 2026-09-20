# RevoSim

Project website for **RevoSim: Scalable Multimodal Tactile Simulation for Dexterous Manipulation**.

The site presents five tactile modalities, synchronized contact examples, and manipulation videos with LeRobot data collection support. The paper is coming soon.

Website: [davidlxu.github.io/RevoSim-web](https://davidlxu.github.io/RevoSim-web/)

GitHub Actions publishes the static files from the `main` branch to GitHub Pages. Asset links are relative so the site works under `/RevoSim-web/`.

## Public visitor statistics

The footer embeds the site's own [Flag Counter map](https://info.flagcounter.com/E6wN). Loading this image records a visit; repeat visitors may count again after 24 hours. The counter starts from setup and cannot recover earlier traffic. Free counters may be removed by the provider after 30 days without a new visitor. Its statistics pages may include advertising.

`tools/update_visitor_stats.py` reads the public country totals (not the tracking image) and creates `assets/visitor-stats.json`. Countries and territories are assigned to seven continents using [GeoNames countryInfo](https://download.geonames.org/export/dump/countryInfo.txt), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Unknown codes remain in an explicit Unknown bucket. No IP addresses or private credentials are saved to this repository.

The Pages workflow refreshes totals hourly at minute 17 UTC, then publishes the static site. GitHub may delay scheduled jobs or disable them after prolonged repository inactivity; use Actions → Publish site and refresh visitor statistics → Run workflow to refresh manually. If the provider fails or changes its table format, the last successful snapshot stays available, with its original update timestamp. The counter's management account was not registered; its public statistics and regeneration link remain available through the link above.
