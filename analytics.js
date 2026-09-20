'use strict';
// Only the public project page records visits; previews do not contact the provider.
if (location.hostname === 'davidlxu.github.io' && location.pathname.startsWith('/RevoSim-web/')) {
  window.goatcounter = {path: '/RevoSim-web/'};
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://gc.zgo.at/count.js';
  script.dataset.goatcounter = 'https://davidlxu.goatcounter.com/count';
  document.head.appendChild(script);
}
