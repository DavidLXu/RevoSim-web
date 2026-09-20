'use strict';
(() => {
  const section = document.querySelector('#visitors');
  if (!section) return;
  const details = section.querySelector('details');
  const status = section.querySelector('[data-visitor-status]');
  let loaded = false, loading = false;
  async function load() {
    if (!details.open || loaded || loading) return;
    loading = true;
    status.textContent = 'Loading statistics…';
    try {
      const response = await fetch('assets/visitor-stats.json', {cache: 'no-store'});
      if (!response.ok) throw new Error('Statistics unavailable');
      const stats = await response.json();
      const codes = ['AF', 'AS', 'EU', 'NA', 'SA', 'OC', 'AN', 'UN'];
      const validCount = value => Number.isSafeInteger(value) && value >= 0;
      if (stats.provider !== 'GoatCounter' || !validCount(stats.total_visits) ||
          !validCount(stats.countries_count) || !codes.every(code => validCount(stats.continents?.[code])) ||
          codes.reduce((sum, code) => sum + stats.continents[code], 0) !== stats.total_visits ||
          !Number.isFinite(Date.parse(stats.updated_at))) throw new Error('Invalid statistics');
      const number = new Intl.NumberFormat('en-US');
      section.querySelector('[data-total-visits]').textContent = number.format(stats.total_visits);
      section.querySelector('[data-total-countries]').textContent = number.format(stats.countries_count);
      codes.forEach(code => {
        section.querySelector(`[data-continent="${code}"]`).textContent = number.format(stats.continents[code]);
      });
      const max = Math.max(1, ...codes.filter(code => code !== 'UN').map(code => stats.continents[code]));
      section.querySelectorAll('[data-map-continent]').forEach(path => {
        const count = stats.continents[path.dataset.mapContinent];
        path.style.fill = count ? `rgba(28, 102, 127, ${0.25 + 0.65 * count / max})` : '';
      });
      section.querySelector('[data-unknown-region]').hidden = stats.continents.UN === 0;
      const date = new Date(stats.updated_at);
      const formatted = new Intl.DateTimeFormat('en-GB', {dateStyle:'medium',timeStyle:'short',timeZone:'UTC'}).format(date);
      status.textContent = `Updated ${formatted} UTC · refreshed approximately hourly`;
      if (Date.now() - date.getTime() > 6 * 60 * 60 * 1000) {
        status.textContent = `Last successful update: ${formatted} UTC. Newer visits are not yet included.`;
      }
      loaded = true;
    } catch (_) {
      status.textContent = 'Statistics are temporarily unavailable. Please try again later.';
    } finally {
      loading = false;
    }
  }
  details.addEventListener('toggle', load);
  load();
})();
