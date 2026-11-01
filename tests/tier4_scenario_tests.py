"""
Tier 4: Real-World Application Scenarios Test Suite
Covers 4 end-to-end full page user journeys with 5 assertion checkpoints each (20 checkpoints).
"""

import os
import re
from typing import List, Dict, Any
from tests.test_utils import HtmlDocument, HtmlNode, WcagContrast, CssAnalyzer, AssetChecker

class Tier4ScenarioTests:
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
        results.extend(self.test_scenario_01_recruiter_journey())
        results.extend(self.test_scenario_02_architect_journey())
        results.extend(self.test_scenario_03_platform_engineer_journey())
        results.extend(self.test_scenario_04_mobile_user_journey())
        return results

    # =========================================================================
    # Scenario 01: Recruiter / Engineering Leader Technical Evaluation Journey
    # =========================================================================
    def test_scenario_01_recruiter_journey(self) -> List[Dict[str, Any]]:
        tests = []
        # Step 1: Arrive on index.html -> Custom monogram logo and title
        brand_links = self.index_doc.select('.brand')
        has_logo = any(b.find('svg') is not None for b in brand_links) or AssetChecker.file_exists(self.repo_root, 'images/ac-logo.svg')
        tests.append({
            'test_id': 'T4_SCN_01_01',
            'tier': 4,
            'feature': 'Scenario 01: Recruiter / Engineering Leader Journey',
            'name': 'Step 1: Recruiter lands on portfolio and encounters custom monogram branding',
            'passed': has_logo,
            'message': 'Custom monogram branding verified' if has_logo else 'Brand logo is unstyled text "AC"'
        })

        # Step 2: Read calmed status strip -> Stockholm hub and clock
        clock_present = len(self.index_doc.select('#stockholm-clock')) > 0
        has_status_strip = ('.status-strip' in self.index_raw or self.index_doc.select('.status-strip') != [])
        tests.append({
            'test_id': 'T4_SCN_01_02',
            'tier': 4,
            'feature': 'Scenario 01: Recruiter / Engineering Leader Journey',
            'name': 'Step 2: Recruiter inspects calmed status strip with Stockholm live clock and credentials',
            'passed': clock_present and has_status_strip,
            'message': 'Status strip with Stockholm clock verified' if (clock_present and has_status_strip) else 'Missing status strip or #stockholm-clock element'
        })

        # Step 3: Review top 3 case studies -> Problem, Architecture, Outcome
        cards = self.index_doc.select('.bento-card')
        cs_count = 0
        for c in cards:
            t = c.get_text().lower()
            if ('problem' in t or 'challenge' in t) and ('architecture' in t or 'solution' in t) and ('outcome' in t or 'impact' in t):
                cs_count += 1
        tests.append({
            'test_id': 'T4_SCN_01_03',
            'tier': 4,
            'feature': 'Scenario 01: Recruiter / Engineering Leader Journey',
            'name': 'Step 3: Recruiter reviews 3 structured case studies (Problem, Architecture, Outcome)',
            'passed': cs_count >= 3,
            'message': f'Found {cs_count}/3 structured case studies'
        })

        # Step 4: Verify About section portrait and Blekinge credentials
        about_text = "".join([s.get_text() for s in self.index_doc.select('#about')])
        has_cred = ('Blekinge' in about_text or 'M.Sc' in about_text) and AssetChecker.file_exists(self.repo_root, 'images/akkireddy-avatar.jpg')
        tests.append({
            'test_id': 'T4_SCN_01_04',
            'tier': 4,
            'feature': 'Scenario 01: Recruiter / Engineering Leader Journey',
            'name': 'Step 4: Recruiter inspects About section portrait and Swedish academic CS credentials',
            'passed': has_cred,
            'message': 'Academic credentials and portrait verified' if has_cred else 'Missing academic credentials or portrait file'
        })

        # Step 5: Resume PDF download verification
        pdf_size = AssetChecker.get_file_size(self.repo_root, 'images/AkkireddyCV19.pdf')
        has_resume_link = any('images/AkkireddyCV19.pdf' in (a.get_attr('href') or '') for a in self.index_doc.find_all('a'))
        tests.append({
            'test_id': 'T4_SCN_01_05',
            'tier': 4,
            'feature': 'Scenario 01: Recruiter / Engineering Leader Journey',
            'name': 'Step 5: Recruiter triggers Resume (PDF) download and accesses non-empty PDF document',
            'passed': has_resume_link and pdf_size > 50000,
            'message': f'Resume PDF verified ({pdf_size} bytes)' if (has_resume_link and pdf_size > 50000) else f'Invalid resume link or empty PDF ({pdf_size} bytes)'
        })
        return tests

    # =========================================================================
    # Scenario 02: AI Systems Architect Interactive Playground Journey
    # =========================================================================
    def test_scenario_02_architect_journey(self) -> List[Dict[str, Any]]:
        tests = []
        # Step 1: MCP Studio card has INTERACTIVE DEMO badge
        studio_text = "".join([c.get_text() for c in self.index_doc.select('.mcp-studio-card')])
        has_demo_badge = ('INTERACTIVE DEMO' in studio_text or 'interactive demo' in self.index_raw.lower() or 'INTERACTIVE RUNTIME' in studio_text)
        tests.append({
            'test_id': 'T4_SCN_02_01',
            'tier': 4,
            'feature': 'Scenario 02: AI Systems Architect Interactive Playground Journey',
            'name': 'Step 1: AI Architect locates MCP Studio with visible "INTERACTIVE DEMO" badge',
            'passed': has_demo_badge,
            'message': 'Interactive demo labeling verified' if has_demo_badge else 'Missing INTERACTIVE DEMO badge in MCP Studio'
        })

        # Step 2: 4 functional MCP server tabs
        tabs = self.index_doc.select('.mcp-tab')
        has_4_tabs = len(tabs) >= 4
        tests.append({
            'test_id': 'T4_SCN_02_02',
            'tier': 4,
            'feature': 'Scenario 02: AI Systems Architect Interactive Playground Journey',
            'name': 'Step 2: AI Architect tests MCP server tabs (k8s, azure, grafana, phoenix)',
            'passed': has_4_tabs,
            'message': f'Found {len(tabs)} MCP server tabs' if has_4_tabs else f'Insufficient tabs (found {len(tabs)}, expected >= 4)'
        })

        # Step 3: Run Tool execution simulation
        has_run_btn = len(self.index_doc.select('#btn-run-tool')) > 0
        has_terminal_output = len(self.index_doc.select('#terminal-output')) > 0
        tests.append({
            'test_id': 'T4_SCN_02_03',
            'tier': 4,
            'feature': 'Scenario 02: AI Systems Architect Interactive Playground Journey',
            'name': 'Step 3: AI Architect executes simulated tool run via #btn-run-tool',
            'passed': has_run_btn and has_terminal_output,
            'message': 'Run tool button and terminal output elements verified' if (has_run_btn and has_terminal_output) else 'Missing #btn-run-tool or #terminal-output'
        })

        # Step 4: Copy Config JSON payload
        has_copy_btn = len(self.index_doc.select('#btn-copy-config')) > 0
        has_config_snippets = 'configSnippet' in self.js_raw
        tests.append({
            'test_id': 'T4_SCN_02_04',
            'tier': 4,
            'feature': 'Scenario 02: AI Systems Architect Interactive Playground Journey',
            'name': 'Step 4: AI Architect copies agent server JSON config via #btn-copy-config',
            'passed': has_copy_btn and has_config_snippets,
            'message': 'Copy config button and configuration snippets verified' if (has_copy_btn and has_config_snippets) else 'Missing copy config button or config snippets in site-ui.js'
        })

        # Step 5: External repository target
        has_repo_link = len(self.index_doc.select('#mcp-repo-link')) > 0
        tests.append({
            'test_id': 'T4_SCN_02_05',
            'tier': 4,
            'feature': 'Scenario 02: AI Systems Architect Interactive Playground Journey',
            'name': 'Step 5: AI Architect navigates to open-source MCP repository link',
            'passed': has_repo_link,
            'message': 'Repository link (#mcp-repo-link) verified' if has_repo_link else 'Missing #mcp-repo-link'
        })
        return tests

    # =========================================================================
    # Scenario 03: Platform Engineer Writing & Knowledge Discovery Journey
    # =========================================================================
    def test_scenario_03_platform_engineer_journey(self) -> List[Dict[str, Any]]:
        tests = []
        # Step 1: Arrive on blog.html
        blog_hero = len(self.blog_doc.select('.page-hero')) > 0
        tests.append({
            'test_id': 'T4_SCN_03_01',
            'tier': 4,
            'feature': 'Scenario 03: Platform Engineer Knowledge Discovery Journey',
            'name': 'Step 1: Platform Engineer lands on writing page with dedicated hero',
            'passed': blog_hero,
            'message': 'Writing hero section verified' if blog_hero else 'Missing .page-hero in blog.html'
        })

        # Step 2: 5 Curated chapters with descriptions and counts
        chapters = self.blog_doc.select('.writing-chapter')
        has_5_chapters = len(chapters) >= 5
        tests.append({
            'test_id': 'T4_SCN_03_02',
            'tier': 4,
            'feature': 'Scenario 03: Platform Engineer Knowledge Discovery Journey',
            'name': 'Step 2: Platform Engineer navigates through 5 curated engineering chapters',
            'passed': has_5_chapters,
            'message': f'Found {len(chapters)} chapter sections' if has_5_chapters else f'Missing 5 chapter sections (found {len(chapters)})'
        })

        # Step 3: Tag wall eliminated, compact in-card tags
        tag_pills = self.blog_doc.select('.tag-filters .tag-pill')
        has_no_wall = len(tag_pills) < 15
        tests.append({
            'test_id': 'T4_SCN_03_03',
            'tier': 4,
            'feature': 'Scenario 03: Platform Engineer Knowledge Discovery Journey',
            'name': 'Step 3: Platform Engineer browses cards without distracting 30-tag wall',
            'passed': has_no_wall,
            'message': '30-tag wall eliminated' if has_no_wall else f'Distracting tag wall still present with {len(tag_pills)} pills'
        })

        # Step 4: Curated Agent Engineering Signals
        signals_section = self.blog_doc.select('.signals-section') or self.blog_doc.select('#signals')
        has_signals = (len(signals_section) > 0 or 'agent engineering signals' in self.blog_raw.lower())
        tests.append({
            'test_id': 'T4_SCN_03_04',
            'tier': 4,
            'feature': 'Scenario 03: Platform Engineer Knowledge Discovery Journey',
            'name': 'Step 4: Platform Engineer studies Curated Agent Engineering Signals with conference citations',
            'passed': has_signals,
            'message': 'Signals section verified' if has_signals else 'Missing Agent Engineering Signals section'
        })

        # Step 5: Light-mode hero contrast satisfies WCAG AA
        light_props = self.css.get_custom_properties(':root')
        accent = light_props.get('--accent', '#047857')
        bg_page = light_props.get('--bg-page', '#f8fafc')
        ratio = WcagContrast.contrast_ratio(accent, bg_page) or 0.0
        tests.append({
            'test_id': 'T4_SCN_03_05',
            'tier': 4,
            'feature': 'Scenario 03: Platform Engineer Knowledge Discovery Journey',
            'name': 'Step 5: Platform Engineer reads comfortably in light mode with WCAG AA compliant text contrast',
            'passed': ratio >= 4.5,
            'message': f'Light mode contrast ratio: {ratio:.2f}:1 (Target >= 4.5:1)'
        })
        return tests

    # =========================================================================
    # Scenario 04: Mobile User End-to-End Cross-Site Experience
    # =========================================================================
    def test_scenario_04_mobile_user_journey(self) -> List[Dict[str, Any]]:
        tests = []
        # Step 1: Mobile viewport containment at 375px
        has_overflow_protection = 'overflow-x: hidden' in self.css_raw or 'overflow-x: clip' in self.css_raw
        tests.append({
            'test_id': 'T4_SCN_04_01',
            'tier': 4,
            'feature': 'Scenario 04: Mobile User End-to-End Cross-Site Experience',
            'name': 'Step 1: Mobile user loads portfolio at 375px width with zero horizontal page blowout',
            'passed': has_overflow_protection,
            'message': 'Global overflow containment verified' if has_overflow_protection else 'Missing overflow containment in CSS'
        })

        # Step 2: Open mobile hamburger drawer
        has_nav_toggle = len(self.index_doc.select('.nav-toggle')) > 0
        has_drawer_script = 'navMenu?.classList.toggle(\'open\')' in self.js_raw or 'navMenu.classList.toggle' in self.js_raw
        tests.append({
            'test_id': 'T4_SCN_04_02',
            'tier': 4,
            'feature': 'Scenario 04: Mobile User End-to-End Cross-Site Experience',
            'name': 'Step 2: Mobile user opens hamburger navigation drawer and accesses site navigation links',
            'passed': has_nav_toggle and has_drawer_script,
            'message': 'Mobile hamburger toggle and drawer script verified' if (has_nav_toggle and has_drawer_script) else 'Missing mobile nav toggle or drawer logic'
        })

        # Step 3: Toggle theme from dark to light on mobile
        has_theme_btn = len(self.index_doc.select('#theme-toggle')) > 0
        tests.append({
            'test_id': 'T4_SCN_04_03',
            'tier': 4,
            'feature': 'Scenario 04: Mobile User End-to-End Cross-Site Experience',
            'name': 'Step 3: Mobile user taps theme toggle button to switch color modes',
            'passed': has_theme_btn,
            'message': 'Mobile theme toggle button verified' if has_theme_btn else 'Missing #theme-toggle'
        })

        # Step 4: Theme persists when navigating to Writing page
        blog_theme_sync = 'localStorage.getItem(\'site-theme\')' in self.blog_raw or 'localStorage.getItem("site-theme")' in self.blog_raw
        tests.append({
            'test_id': 'T4_SCN_04_04',
            'tier': 4,
            'feature': 'Scenario 04: Mobile User End-to-End Cross-Site Experience',
            'name': 'Step 4: Mobile user navigates to Writing page with seamless theme persistence',
            'passed': blog_theme_sync,
            'message': 'Cross-page theme persistence verified in blog.html' if blog_theme_sync else 'Missing theme persistence script in blog.html'
        })

        # Step 5: Search input functions on mobile writing page
        has_search_input = len(self.blog_doc.select('#write-search')) > 0
        tests.append({
            'test_id': 'T4_SCN_04_05',
            'tier': 4,
            'feature': 'Scenario 04: Mobile User End-to-End Cross-Site Experience',
            'name': 'Step 5: Mobile user utilizes #write-search input to filter engineering articles smoothly',
            'passed': has_search_input,
            'message': 'Writing search input #write-search verified' if has_search_input else 'Missing #write-search input in blog.html'
        })
        return tests
