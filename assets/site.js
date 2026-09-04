(() => {
  const themeScript = document.createElement('script');
  themeScript.src = '/assets/theme.js';
  themeScript.dataset.ecTheme = '';
  document.head.appendChild(themeScript);

  const wordmarkStylesheet = document.createElement('link');
  wordmarkStylesheet.rel = 'stylesheet';
  wordmarkStylesheet.href = '/assets/wordmark.css';
  wordmarkStylesheet.dataset.commonsWordmark = '';
  document.head.appendChild(wordmarkStylesheet);

  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  const year = document.querySelector('[data-year]');

  if (year) year.textContent = new Date().getFullYear();

  const updateHeader = () => {
    if (!header) return;
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };

  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });

    nav.addEventListener('click', event => {
      if (!(event.target instanceof HTMLAnchorElement)) return;
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });

    // The collapsed mobile navigation is an enhancement, never the baseline.
    // Add the marker only after the controls and their handlers are available.
    document.documentElement.classList.add('js');
  }
})();
