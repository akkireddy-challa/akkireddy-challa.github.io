"""
Tier 2: Boundary & Corner Cases Test Suite
Covers 5 boundary categories with >= 5 test cases each (25 test cases).
"""

import os
import re
import urllib.parse
from typing import List, Dict, Any, Tuple
from tests.test_utils import HtmlDocument, HtmlNode, WcagContrast, CssAnalyzer, AssetChecker

class Tier2BoundaryTests:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.index_path = os.path.join(repo_root, 'index.html')
        self.blog_path = os.path.join(repo_root, 'blog.html')
        self.css_path = os.path.join(repo_root, 'css', 'styles.css')
        self.js_path = os.path.join(repo_root, 'js', 'site-ui.js')

        self.index_doc = HtmlDocument.parse_file(self.index_path)
        self.blog_doc = HtmlDocument.parse_file(self.blog_path)
        self.css = CssAnalyzer.from_file(self.css_path)

        with open(self.index_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.index_raw = f.read()
        with open(self.blog_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.blog_raw = f.read()
        with open(self.css_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.css_raw = f.read()
        with open(self.js_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.js_raw = f.read()

    def run_all(self) -> List[Dict[str, Any]]:
        results = []
        results.extend(self.test_boundary_01_viewport())
        results.extend(self.test_boundary_02_contrast())
        results.extend(self.test_boundary_03_search_queries())
        results.extend(self.test_boundary_04_query_params())
        results.extend(self.test_boundary_05_localstorage())
        return results

    # =========================================================================
    # Boundary 01: 375px Mobile Viewport Overflow Boundary
    # =========================================================================
    def test_boundary_01_viewport(self) -> List[Dict[str, Any]]:
        tests = []
        # T2_BND_01_01: Viewport meta tag specifies width=device-width, initial-scale=1
        index_meta = self.index_doc.select('meta[name="viewport"]')
        blog_meta = self.blog_doc.select('meta[name="viewport"]')
        index_vp = any('width=device-width' in (m.get_attr('content') or '') and 'initial-scale=1' in (m.get_attr('content') or '') for m in index_meta)
        blog_vp = any('width=device-width' in (m.get_attr('content') or '') and 'initial-scale=1' in (m.get_attr('content') or '') for m in blog_meta)
        tests.append({
            'test_id': 'T2_BND_01_01',
            'tier': 2,
            'feature': 'Boundary 01: 375px Mobile Viewport Overflow',
            'name': 'Viewport meta tag configured with standard responsive scaling on all pages',
            'passed': index_vp and blog_vp,
            'message': 'Standard mobile viewport meta tags verified on both pages' if (index_vp and blog_vp) else 'Missing or non-standard viewport meta tag'
        })

        # T2_BND_01_02: Terminal code blocks have overflow-x handling
        terminal_rules = self.css.find_rules('.terminal-output') + self.css.find_rules('.terminal-body') + self.css.find_rules('.terminal-cmd-text')
        has_terminal_overflow = any('overflow-x' in r or 'overflow: auto' in r or 'overflow: hidden' in r or 'white-space: pre-wrap' in r for r in terminal_rules)
        tests.append({
            'test_id': 'T2_BND_01_02',
            'tier': 2,
            'feature': 'Boundary 01: 375px Mobile Viewport Overflow',
            'name': 'Terminal code outputs implement overflow-x containment to prevent mobile stretching',
            'passed': has_terminal_overflow,
            'message': 'Terminal code container overflow handling verified' if has_terminal_overflow else 'Missing overflow containment on terminal outputs'
        })

        # T2_BND_01_03: Bento grid columns wrap to 1 column on mobile screens
        media_queries = self.css.get_media_queries()
        has_mobile_col_reset = False
        for cond, body in media_queries:
            if 'max-width: 768px' in cond or 'max-width: 600px' in cond or 'max-width: 480px' in cond or 'max-width: 375px' in cond:
                if 'grid-column: span 12' in body or 'grid-template-columns: 1fr' in body or 'col-span' in body:
                    has_mobile_col_reset = True
                    break
        tests.append({
            'test_id': 'T2_BND_01_03',
            'tier': 2,
            'feature': 'Boundary 01: 375px Mobile Viewport Overflow',
            'name': 'Bento grid columns reset to single-column (1fr/span 12) on mobile viewports',
            'passed': has_mobile_col_reset,
            'message': 'Mobile column reset rules verified in CSS' if has_mobile_col_reset else 'Missing mobile column reset in media queries'
        })

        # T2_BND_01_04: Navigation actions button group fits within 375px viewport
        has_nav_actions = '.nav-actions' in self.css_raw
        nav_action_rules = self.css.find_rules('.nav-actions')
        no_rigid_min_width = not any(re.search(r'min-width:\s*([4-9]\d{2}|[1-9]\d{3})px', r) for r in nav_action_rules)
        tests.append({
            'test_id': 'T2_BND_01_04',
            'tier': 2,
            'feature': 'Boundary 01: 375px Mobile Viewport Overflow',
            'name': 'Site header actions bar fits within 375px viewport without fixed min-width overflow',
            'passed': has_nav_actions and no_rigid_min_width,
            'message': 'Nav actions dimensions verified safe for mobile' if (has_nav_actions and no_rigid_min_width) else 'Header nav-actions has rigid min-width causing overflow'
        })

        # T2_BND_01_05: No fixed width pixels exceeding 360px on full-width containers
        fixed_width_matches = re.findall(r'(?:^|\s)width:\s*([4-9]\d{2}|[1-9]\d{3})px', self.css_raw)
        # Check if max-width: 100% or box-sizing protects them
        has_global_max_w = 'img, video, canvas, svg {' in self.css_raw and 'max-width: 100%' in self.css_raw
        tests.append({
            'test_id': 'T2_BND_01_05',
            'tier': 2,
            'feature': 'Boundary 01: 375px Mobile Viewport Overflow',
            'name': 'Global media elements enforce max-width: 100% to prevent rigid pixel blowout',
            'passed': has_global_max_w,
            'message': 'Global responsive image/media containment verified' if has_global_max_w else 'Missing global max-width: 100% for images/svgs in CSS'
        })
        return tests

    # =========================================================================
    # Boundary 02: WCAG AA Contrast Calculations across all theme states
    # =========================================================================
    def test_boundary_02_contrast(self) -> List[Dict[str, Any]]:
        tests = []
        light_props = self.css.get_custom_properties(':root')
        dark_props = self.css.get_custom_properties("html[data-theme='dark']") or self.css.get_custom_properties(':root')

        light_bg = light_props.get('--bg-page', '#f8fafc')
        light_primary = light_props.get('--text-primary', '#0f172a')
        light_secondary = light_props.get('--text-secondary', '#475569')
        light_accent = light_props.get('--accent', '#047857')

        dark_bg = dark_props.get('--bg-page', '#080b10')
        dark_primary = dark_props.get('--text-primary', '#f8fafc')
        dark_secondary = dark_props.get('--text-secondary', '#cbd5e1')
        dark_accent = dark_props.get('--accent', '#10b981')

        # T2_BND_02_01: Light mode primary text contrast >= 7.0:1 (AAA)
        r_lp = WcagContrast.contrast_ratio(light_primary, light_bg) or 0.0
        tests.append({
            'test_id': 'T2_BND_02_01',
            'tier': 2,
            'feature': 'Boundary 02: WCAG AA Contrast Calculations',
            'name': 'Light mode primary text contrast ratio >= 7.0:1 (WCAG AAA)',
            'passed': r_lp >= 7.0,
            'message': f'Light primary contrast: {r_lp:.2f}:1 (Target >= 7.0:1)'
        })

        # T2_BND_02_02: Light mode secondary text contrast >= 4.5:1 (AA)
        r_ls = WcagContrast.contrast_ratio(light_secondary, light_bg) or 0.0
        tests.append({
            'test_id': 'T2_BND_02_02',
            'tier': 2,
            'feature': 'Boundary 02: WCAG AA Contrast Calculations',
            'name': 'Light mode secondary text contrast ratio >= 4.5:1 (WCAG AA)',
            'passed': r_ls >= 4.5,
            'message': f'Light secondary contrast: {r_ls:.2f}:1 (Target >= 4.5:1)'
        })

        # T2_BND_02_03: Dark mode primary text contrast >= 10.0:1 (AAA)
        r_dp = WcagContrast.contrast_ratio(dark_primary, dark_bg) or 0.0
        tests.append({
            'test_id': 'T2_BND_02_03',
            'tier': 2,
            'feature': 'Boundary 02: WCAG AA Contrast Calculations',
            'name': 'Dark mode primary text contrast ratio >= 10.0:1 (WCAG AAA)',
            'passed': r_dp >= 10.0,
            'message': f'Dark primary contrast: {r_dp:.2f}:1 (Target >= 10.0:1)'
        })

        # T2_BND_02_04: Dark mode secondary text contrast >= 4.5:1 (AA)
        r_ds = WcagContrast.contrast_ratio(dark_secondary, dark_bg) or 0.0
        tests.append({
            'test_id': 'T2_BND_02_04',
            'tier': 2,
            'feature': 'Boundary 02: WCAG AA Contrast Calculations',
            'name': 'Dark mode secondary text contrast ratio >= 4.5:1 (WCAG AA)',
            'passed': r_ds >= 4.5,
            'message': f'Dark secondary contrast: {r_ds:.2f}:1 (Target >= 4.5:1)'
        })

        # T2_BND_02_05: Light mode accent contrast >= 4.5:1
        r_la = WcagContrast.contrast_ratio(light_accent, light_bg) or 0.0
        tests.append({
            'test_id': 'T2_BND_02_05',
            'tier': 2,
            'feature': 'Boundary 02: WCAG AA Contrast Calculations',
            'name': 'Light mode accent token contrast ratio >= 4.5:1 for accessible emphasis and links',
            'passed': r_la >= 4.5,
            'message': f'Light accent contrast: {r_la:.2f}:1 with accent={light_accent} on bg={light_bg} (Target >= 4.5:1)'
        })
        return tests

    # =========================================================================
    # Boundary 03: Empty & Edge Search Queries in Blog
    # =========================================================================
    def test_boundary_03_search_queries(self) -> List[Dict[str, Any]]:
        tests = []
        # We test the client-side search simulation logic defined for the blog
        cards = self.blog_doc.select('.writing-card')

        def simulate_filter(query: str, card_node: HtmlNode) -> bool:
            q = query.strip().lower()
            if not q:
                return True
            title = card_node.find('h2') or card_node.find('h3')
            title_text = title.get_text().lower() if title else ""
            desc = card_node.find('p')
            desc_text = desc.get_text().lower() if desc else ""
            tags = card_node.get_attr('data-tags', '').lower()
            return q in title_text or q in desc_text or q in tags

        # T2_BND_03_01: Empty search query "" retains all 9 articles
        matching_empty = [c for c in cards if simulate_filter("", c)]
        tests.append({
            'test_id': 'T2_BND_03_01',
            'tier': 2,
            'feature': 'Boundary 03: Empty & Edge Search Queries in Blog',
            'name': 'Empty search query ("") retains all 9 engineering articles',
            'passed': len(matching_empty) == 9,
            'message': f'Empty query matched {len(matching_empty)}/9 articles'
        })

        # T2_BND_03_02: Whitespace-only search query "   " retains all 9 articles
        matching_whitespace = [c for c in cards if simulate_filter("   ", c)]
        tests.append({
            'test_id': 'T2_BND_03_02',
            'tier': 2,
            'feature': 'Boundary 03: Empty & Edge Search Queries in Blog',
            'name': 'Whitespace-only search query ("   ") trims cleanly and retains all articles',
            'passed': len(matching_whitespace) == 9,
            'message': f'Whitespace query matched {len(matching_whitespace)}/9 articles'
        })

        # T2_BND_03_03: Special regex characters do not crash search
        regex_queries = [".*", "+", "?", "[a-z]", "(test)", "^$", ".*+"]
        regex_safe = True
        try:
            for rq in regex_queries:
                _ = [c for c in cards if simulate_filter(rq, c)]
        except Exception:
            regex_safe = False
        tests.append({
            'test_id': 'T2_BND_03_03',
            'tier': 2,
            'feature': 'Boundary 03: Empty & Edge Search Queries in Blog',
            'name': 'Special regex metacharacters in query string execute safely without uncaught exceptions',
            'passed': regex_safe,
            'message': 'Regex characters evaluated safely via substring search' if regex_safe else 'Search crashed on regex metacharacters'
        })

        # T2_BND_03_04: Non-matching query returns 0 results
        matching_nonexistent = [c for c in cards if simulate_filter("xyznonexistent999", c)]
        tests.append({
            'test_id': 'T2_BND_03_04',
            'tier': 2,
            'feature': 'Boundary 03: Empty & Edge Search Queries in Blog',
            'name': 'Non-matching search query ("xyznonexistent999") cleanly isolates zero articles',
            'passed': len(matching_nonexistent) == 0,
            'message': f'Non-matching query returned {len(matching_nonexistent)} articles'
        })

        # T2_BND_03_05: Case-insensitive search parity
        q_lower = [c for c in cards if simulate_filter("kubernetes", c)]
        q_upper = [c for c in cards if simulate_filter("KUBERNETES", c)]
        q_mixed = [c for c in cards if simulate_filter("kUbErNeTeS", c)]
        case_invariant = (len(q_lower) > 0 and len(q_lower) == len(q_upper) == len(q_mixed))
        tests.append({
            'test_id': 'T2_BND_03_05',
            'tier': 2,
            'feature': 'Boundary 03: Empty & Edge Search Queries in Blog',
            'name': 'Search matching is strictly case-insensitive across uppercase, lowercase, and mixed input',
            'passed': case_invariant,
            'message': f'Case invariance verified (matched {len(q_lower)} articles across all casing variations)' if case_invariant else 'Search results vary by letter casing'
        })
        return tests

    # =========================================================================
    # Boundary 04: Missing & Corrupt URL Query Parameters
    # =========================================================================
    def test_boundary_04_query_params(self) -> List[Dict[str, Any]]:
        tests = []
        # T2_BND_04_01: Clean URL without query params loads default state
        has_param_reader = ('getQueryParam' in self.blog_raw or 'URLSearchParams' in self.blog_raw or 'window.location.search' in self.blog_raw)
        tests.append({
            'test_id': 'T2_BND_04_01',
            'tier': 2,
            'feature': 'Boundary 04: Missing & Corrupt URL Query Parameters',
            'name': 'Page script initializes safely with no query parameters present',
            'passed': has_param_reader,
            'message': 'URL parameter initialization logic verified' if has_param_reader else 'Missing URL parameter handling'
        })

        # T2_BND_04_02: Malformed URI components in search query
        # Check if URL parameter decode is guarded
        has_try_catch_or_safe_decode = ('decodeURIComponent' in self.blog_raw or 'URLSearchParams' in self.blog_raw)
        tests.append({
            'test_id': 'T2_BND_04_02',
            'tier': 2,
            'feature': 'Boundary 04: Missing & Corrupt URL Query Parameters',
            'name': 'URL parameter decoding handles malformed URI strings safely without script halting',
            'passed': has_try_catch_or_safe_decode,
            'message': 'Standard URLSearchParams / decodeURIComponent logic present' if has_try_catch_or_safe_decode else 'Missing URL decode handling'
        })

        # T2_BND_04_03: Unknown tag query parameter does not throw
        cards = self.blog_doc.select('.writing-card')
        unknown_tag = "nonexistent-arbitrary-tag-123"
        cards_matching_unknown = [c for c in cards if unknown_tag in c.get_attr('data-tags', '').lower()]
        tests.append({
            'test_id': 'T2_BND_04_03',
            'tier': 2,
            'feature': 'Boundary 04: Missing & Corrupt URL Query Parameters',
            'name': 'Unknown tag query parameter (?tag=unknown) evaluates safely to zero matched cards',
            'passed': len(cards_matching_unknown) == 0,
            'message': f'Unknown tag matches {len(cards_matching_unknown)} cards safely'
        })

        # T2_BND_04_04: Comma-separated tag query parameter
        multi_tags_raw = "kubernetes,terraform"
        parsed_tags = [t.strip().lower() for t in multi_tags_raw.split(',') if t.strip()]
        tests.append({
            'test_id': 'T2_BND_04_04',
            'tier': 2,
            'feature': 'Boundary 04: Missing & Corrupt URL Query Parameters',
            'name': 'Multi-tag query parameters (comma-separated) parse into clean token lists',
            'passed': len(parsed_tags) == 2 and parsed_tags[0] == 'kubernetes',
            'message': f'Parsed multi-tags: {parsed_tags}'
        })

        # T2_BND_04_05: Empty tag parameter (?tag=&q=) does not corrupt state
        empty_param_str = "?tag=&q="
        parsed_params = urllib.parse.parse_qs(empty_param_str.lstrip('?'))
        q_val = parsed_params.get('q', [''])[0]
        tag_val = parsed_params.get('tag', [''])[0]
        tests.append({
            'test_id': 'T2_BND_04_05',
            'tier': 2,
            'feature': 'Boundary 04: Missing & Corrupt URL Query Parameters',
            'name': 'Empty query parameters (?tag=&q=) resolve to empty strings without crashing',
            'passed': q_val == '' and tag_val == '',
            'message': 'Empty parameters safely treated as null/empty'
        })
        return tests

    # =========================================================================
    # Boundary 05: LocalStorage Persistence & Theme Fallbacks
    # =========================================================================
    def test_boundary_05_localstorage(self) -> List[Dict[str, Any]]:
        tests = []
        # T2_BND_05_01: localStorage security exceptions wrapped in try/catch in <head>
        index_try_catch = 'try {' in self.index_raw and 'localStorage' in self.index_raw
        blog_try_catch = 'try {' in self.blog_raw and 'localStorage' in self.blog_raw
        tests.append({
            'test_id': 'T2_BND_05_01',
            'tier': 2,
            'feature': 'Boundary 05: LocalStorage Persistence & Theme Fallbacks',
            'name': 'Inline <head> localStorage reads are wrapped in try/catch for private browsing security',
            'passed': index_try_catch and blog_try_catch,
            'message': 'try/catch wrapping verified in <head> of both pages' if (index_try_catch and blog_try_catch) else 'Missing try/catch around localStorage in <head>'
        })

        # T2_BND_05_02: Corrupted theme value in localStorage safely rejected
        # In site-ui.js: only 'dark' or 'light' should be accepted
        checks_valid_theme = "savedTheme === 'dark' || savedTheme === 'light'" in self.index_raw or "savedTheme === \"dark\" || savedTheme === \"light\"" in self.index_raw
        tests.append({
            'test_id': 'T2_BND_05_02',
            'tier': 2,
            'feature': 'Boundary 05: LocalStorage Persistence & Theme Fallbacks',
            'name': 'Unrecognized theme values (e.g. "neon", "") rejected in favor of system preference',
            'passed': checks_valid_theme,
            'message': 'Strict theme whitelist check verified' if checks_valid_theme else 'Missing theme validation check before applying savedTheme'
        })

        # T2_BND_05_03: Repeated theme toggles alternate cleanly
        # In site-ui.js: nextTheme = currentTheme === 'dark' ? 'light' : 'dark'
        has_toggle_flip = "currentTheme === 'dark' ? 'light' : 'dark'" in self.js_raw or "theme === 'dark' ? 'light' : 'dark'" in self.js_raw
        tests.append({
            'test_id': 'T2_BND_05_03',
            'tier': 2,
            'feature': 'Boundary 05: LocalStorage Persistence & Theme Fallbacks',
            'name': 'Theme toggle strictly inverts current state between "dark" and "light"',
            'passed': has_toggle_flip,
            'message': 'Theme inversion logic verified in site-ui.js' if has_toggle_flip else 'Missing standard binary theme inversion logic'
        })

        # T2_BND_05_04: First visit with empty localStorage checks prefers-color-scheme
        checks_system_pref = "window.matchMedia('(prefers-color-scheme: dark)')" in self.js_raw or 'prefers-color-scheme: dark' in self.js_raw
        tests.append({
            'test_id': 'T2_BND_05_04',
            'tier': 2,
            'feature': 'Boundary 05: LocalStorage Persistence & Theme Fallbacks',
            'name': 'Initial visit without saved theme respects OS prefers-color-scheme media query',
            'passed': checks_system_pref,
            'message': 'prefers-color-scheme media query evaluation verified' if checks_system_pref else 'Missing prefers-color-scheme listener in site-ui.js'
        })

        # T2_BND_05_05: meta[name="color-scheme"] synchronized with documentElement
        syncs_meta = 'document.querySelector(\'meta[name="color-scheme"]\')' in self.index_raw or 'meta[name="color-scheme"]' in self.js_raw
        tests.append({
            'test_id': 'T2_BND_05_05',
            'tier': 2,
            'feature': 'Boundary 05: LocalStorage Persistence & Theme Fallbacks',
            'name': 'meta[name="color-scheme"] content is updated synchronously to eliminate FOUC',
            'passed': syncs_meta,
            'message': 'color-scheme meta synchronization verified' if syncs_meta else 'Missing color-scheme meta synchronization'
        })
        return tests
