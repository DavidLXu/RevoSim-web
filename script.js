'use strict';
const heroVideo = document.querySelector('#hero-video');
const motionToggle = document.querySelector('#motion-toggle');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let manuallyPaused = false;

function updateMotionLabel() {
  motionToggle.textContent = heroVideo.paused ? 'Play background' : 'Pause background';
}
function playHero() {
  if (!heroVideo.getAttribute('src')) heroVideo.src = heroVideo.dataset.heroSrc;
  heroVideo.play().catch(() => { updateMotionLabel(); });
}
motionToggle.hidden = false;
motionToggle.addEventListener('click', () => {
  if (heroVideo.paused) { manuallyPaused = false; playHero(); }
  else { manuallyPaused = true; heroVideo.pause(); }
});
heroVideo.addEventListener('play', updateMotionLabel);
heroVideo.addEventListener('pause', updateMotionLabel);
heroVideo.addEventListener('error', () => { motionToggle.hidden = true; });
reducedMotion.addEventListener('change', () => {
  if (reducedMotion.matches) heroVideo.pause();
  else if (!manuallyPaused && !document.hidden) playHero();
});
const heroObserver = new IntersectionObserver(([entry]) => {
  if (!entry.isIntersecting || document.hidden) heroVideo.pause();
  else if (!reducedMotion.matches && !manuallyPaused) playHero();
}, { threshold: 0.12 });
heroObserver.observe(document.querySelector('.hero'));
document.addEventListener('visibilitychange', () => {
  if (document.hidden) heroVideo.pause();
  else if (!reducedMotion.matches && !manuallyPaused && document.querySelector('.hero').getBoundingClientRect().bottom > 0) playHero();
});
document.querySelectorAll('.demos video').forEach((video) => {
  video.addEventListener('play', () => {
    document.querySelectorAll('.demos video').forEach((other) => { if (other !== video) other.pause(); });
  });
});
updateMotionLabel();

const copyCitation = document.querySelector('#copy-citation');
const bibtex = document.querySelector('#bibtex');
const citationStatus = document.querySelector('#citation-status');
if (copyCitation && bibtex && citationStatus) {
  copyCitation.hidden = false;
  copyCitation.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(bibtex.textContent);
      citationStatus.textContent = 'BibTeX copied.';
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(bibtex);
      selection.removeAllRanges();
      selection.addRange(range);
      citationStatus.textContent = 'Citation selected. Press Ctrl+C or ⌘C to copy.';
    }
  });
}
