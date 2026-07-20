(() => {
    const root = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle?.querySelector('.theme-icon');
    const themeText = themeToggle?.querySelector('.theme-text');

    const getSavedTheme = () => {
        try {
            return localStorage.getItem('site-theme');
        } catch {
            return null;
        }
    };

    const saveTheme = theme => {
        try {
            localStorage.setItem('site-theme', theme);
        } catch {
            // Theme still works when browser storage is unavailable.
        }
    };

    const updateThemeControl = theme => {
        if (!themeToggle) return;

        if (themeIcon) themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        if (themeText) themeText.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
        themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    };

    const applyTheme = (theme, persist = false) => {
        root.dataset.theme = theme;
        updateThemeControl(theme);
        if (persist) saveTheme(theme);
    };

    const savedTheme = getSavedTheme();
    const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    applyTheme(savedTheme || preferredTheme);

    themeToggle?.addEventListener('click', () => {
        applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
    });

    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.getElementById('primary-navigation');

    const closeMenu = ({ returnFocus = false } = {}) => {
        if (!navToggle || !navMenu) return;
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open navigation');
        navMenu.classList.remove('open');
        if (returnFocus) navToggle.focus();
    };

    navToggle?.addEventListener('click', () => {
        if (!navMenu) return;
        const expanded = navToggle.getAttribute('aria-expanded') === 'true';
        if (expanded) {
            closeMenu();
            return;
        }
        navToggle.setAttribute('aria-expanded', 'true');
        navToggle.setAttribute('aria-label', 'Close navigation');
        navMenu.classList.add('open');
    });

    navMenu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && navMenu?.classList.contains('open')) closeMenu({ returnFocus: true });
    });

    const article = document.querySelector('.article');
    const readingProgress = document.querySelector('[data-reading-progress]');

    if (article && readingProgress) {
        const updateReadingProgress = () => {
            const articleStart = article.offsetTop;
            const articleEnd = articleStart + article.offsetHeight - window.innerHeight;
            const ratio = articleEnd <= articleStart ? 1 : Math.min(1, Math.max(0, (window.scrollY - articleStart) / (articleEnd - articleStart)));
            readingProgress.style.setProperty('--reading-progress', ratio);
        };

        updateReadingProgress();
        window.addEventListener('scroll', updateReadingProgress, { passive: true });
        window.addEventListener('resize', updateReadingProgress);
    }
})();
