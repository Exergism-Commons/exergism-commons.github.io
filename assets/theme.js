(() => {
  const STORAGE_KEY = 'ec-theme';
  const COOKIE_KEY = 'ec-theme';
  const root = document.documentElement;

  const readCookie = () => {
    const match = document.cookie.match(new RegExp(`(?:^|; )${COOKIE_KEY}=([^;]+)`));
    return match ? decodeURIComponent(match[1]) : null;
  };

  const readStoredTheme = () => {
    const cookieTheme = readCookie();
    if (cookieTheme === 'dark' || cookieTheme === 'light') return cookieTheme;
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored === 'dark' || stored === 'light') return stored;
    } catch (_) {}
    return null;
  };

  const systemTheme = () => window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  const persistTheme = theme => {
    try { localStorage.setItem(STORAGE_KEY, theme); } catch (_) {}
    const secure = location.protocol === 'https:' ? '; Secure' : '';
    const domain = location.hostname === 'exergism.org' || location.hostname.endsWith('.exergism.org')
      ? '; Domain=.exergism.org'
      : '';
    document.cookie = `${COOKIE_KEY}=${encodeURIComponent(theme)}; Path=/; Max-Age=31536000; SameSite=Lax${domain}${secure}`;
  };

  const applyTheme = theme => {
    root.dataset.ecTheme = theme;
    root.style.colorScheme = 'light';
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#0d0f10' : '#f2f0e9');
    const button = document.querySelector('[data-ec-theme-toggle]');
    if (button) {
      const dark = theme === 'dark';
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      button.innerHTML = `<span aria-hidden="true">${dark ? '☀' : '◐'}</span><span>${dark ? 'Light' : 'Dark'}</span>`;
    }
  };

  const css = document.createElement('style');
  css.id = 'ec-theme-styles';
  css.textContent = `
    html[data-ec-theme="dark"] {
      background: #0d0f10;
      scrollbar-color: #626962 #0d0f10;
    }

    html[data-ec-theme="dark"] body {
      filter: invert(1) hue-rotate(180deg);
    }

    .ec-theme-toggle {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: .45rem;
      min-height: 36px;
      padding: 7px 12px;
      border: 1px solid currentColor;
      border-radius: 999px;
      background: transparent;
      color: inherit;
      font: inherit;
      font-size: .78rem;
      font-weight: 720;
      line-height: 1;
      letter-spacing: .01em;
      cursor: pointer;
      white-space: nowrap;
    }

    .ec-theme-toggle:hover { opacity: .72; }
    .ec-theme-toggle:focus-visible { outline: 2px solid currentColor; outline-offset: 3px; }

    .ec-theme-inline-control {
      display: flex;
      justify-content: flex-end;
      margin: 0 0 24px;
    }

    @media (max-width: 720px) {
      .ec-theme-toggle { min-height: 34px; padding: 7px 10px; font-size: .74rem; }
    }

    @media (prefers-reduced-motion: reduce) {
      .ec-theme-toggle { transition: none !important; }
    }
  `;
  document.head.appendChild(css);

  const explicitTheme = readStoredTheme();
  applyTheme(explicitTheme || systemTheme());

  const mountToggle = () => {
    if (document.querySelector('[data-ec-theme-toggle]')) return;

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ec-theme-toggle';
    button.dataset.ecThemeToggle = '';

    button.addEventListener('click', () => {
      const next = root.dataset.ecTheme === 'dark' ? 'light' : 'dark';
      persistTheme(next);
      applyTheme(next);
    });

    const nav = document.querySelector('.site-header .site-nav, .site-header .nav');
    if (nav) {
      const github = nav.querySelector('.nav-cta, .nav-github');
      if (github) nav.insertBefore(button, github);
      else nav.appendChild(button);
    } else {
      const main = document.querySelector('main');
      if (main) {
        const holder = document.createElement('div');
        holder.className = 'ec-theme-inline-control';
        holder.appendChild(button);
        main.prepend(holder);
      } else {
        document.body.prepend(button);
      }
    }

    applyTheme(root.dataset.ecTheme || systemTheme());
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountToggle, { once: true });
  else mountToggle();

  if (!explicitTheme && window.matchMedia) {
    const media = window.matchMedia('(prefers-color-scheme: dark)');
    media.addEventListener?.('change', event => applyTheme(event.matches ? 'dark' : 'light'));
  }
})();
