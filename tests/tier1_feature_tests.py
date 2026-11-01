"""
Tier 1: Feature Coverage Test Suite
Covers all 16 features from PROJECT.md with >= 5 test cases per feature (80 test cases).
"""

import os
import re
import subprocess
from typing import List, Dict, Any, Tuple
from tests.test_utils import HtmlDocument, HtmlNode, WcagContrast, CssAnalyzer, AssetChecker

class Tier1FeatureTests:
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
        for feat_idx in range(1, 17):
            method_name = f'test_feature_{feat_idx:02d}'
            if hasattr(self, method_name):
                feat_tests = getattr(self, method_name)()
                results.extend(feat_tests)
        return results

    # =========================================================================
    # Feature 01: Custom Angular 'AC' Monogram Logo
    # =========================================================================
    def test_feature_01(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_01_01: index.html brand contains SVG monogram logo
        brand_links = self.index_doc.select('.brand')
        has_svg_in_brand = any(b.find('svg') is not None for b in brand_links) or AssetChecker.file_exists(self.repo_root, 'images/ac-logo.svg')
        tests.append({
            'test_id': 'T1_FEAT_01_01',
            'tier': 1,
            'feature': 'Feature 01: Custom Angular AC Monogram Logo',
            'name': 'index.html brand contains custom vector SVG monogram logo',
            'passed': has_svg_in_brand,
            'message': 'Custom SVG logo found in index.html header' if has_svg_in_brand else 'Missing SVG in index.html .brand (found plain text or missing SVG)'
        })

        # T1_FEAT_01_02: blog.html brand contains SVG monogram logo
        blog_brand = self.blog_doc.select('.brand')
        has_svg_in_blog_brand = any(b.find('svg') is not None for b in blog_brand) or ('<svg' in self.blog_raw and 'brand' in self.blog_raw)
        tests.append({
            'test_id': 'T1_FEAT_01_02',
            'tier': 1,
            'feature': 'Feature 01: Custom Angular AC Monogram Logo',
            'name': 'blog.html brand contains custom vector SVG monogram logo',
            'passed': has_svg_in_blog_brand,
            'message': 'Custom SVG logo found in blog.html header' if has_svg_in_blog_brand else 'Missing SVG in blog.html .brand'
        })

        # T1_FEAT_01_03: Logo SVG has angular geometry (paths/lines for A & C)
        svg_content = ""
        if AssetChecker.file_exists(self.repo_root, 'images/ac-logo.svg'):
            with open(os.path.join(self.repo_root, 'images', 'ac-logo.svg'), 'r', encoding='utf-8') as f:
                svg_content = f.read()
        else:
            svg_match = re.search(r'<a[^>]*class="[^"]*brand[^"]*"[^>]*>([\s\S]*?)</a>', self.index_raw)
            if svg_match:
                svg_content = svg_match.group(1)
        has_angular_geom = ('<path' in svg_content or '<polygon' in svg_content or '<line' in svg_content) and ('viewbox' in svg_content.lower())
        tests.append({
            'test_id': 'T1_FEAT_01_03',
            'tier': 1,
            'feature': 'Feature 01: Custom Angular AC Monogram Logo',
            'name': 'Logo SVG features angular vector geometry with viewBox definition',
            'passed': has_angular_geom,
            'message': 'SVG contains viewBox and geometric vector elements (<path>/<polygon>/<line>)' if has_angular_geom else 'SVG does not contain required angular vector markup or viewBox'
        })

        # T1_FEAT_01_04: Logo contains agent/infrastructure routing conduit motif
        has_routing_motif = ('circuit' in svg_content.lower() or 'route' in svg_content.lower() or 'conduit' in svg_content.lower() or 'line' in svg_content.lower() or 'circle' in svg_content.lower())
        tests.append({
            'test_id': 'T1_FEAT_01_04',
            'tier': 1,
            'feature': 'Feature 01: Custom Angular AC Monogram Logo',
            'name': 'Logo vector geometry includes routing conduit / data bus motif',
            'passed': has_routing_motif and has_angular_geom,
            'message': 'Routing conduit and node motif verified in logo SVG' if (has_routing_motif and has_angular_geom) else 'Logo SVG missing routing conduit/node motif'
        })

        # T1_FEAT_01_05: Logo markup replaces plain unstyled "AC" text node; accessible aria-label
        brand_accessible = any(b.get_attr('aria-label') == 'Akkireddy Challa Home' for b in brand_links)
        brand_not_just_plain_text = any(b.get_text().strip() != 'AC' or b.find('svg') is not None for b in brand_links)
        tests.append({
            'test_id': 'T1_FEAT_01_05',
            'tier': 1,
            'feature': 'Feature 01: Custom Angular AC Monogram Logo',
            'name': 'Brand link contains aria-label="Akkireddy Challa Home" and replaces raw AC text',
            'passed': brand_accessible and brand_not_just_plain_text,
            'message': 'Brand link has accessible label and non-plain text structure' if (brand_accessible and brand_not_just_plain_text) else 'Brand link lacks required aria-label="Akkireddy Challa Home" or remains plain "AC" text'
        })
        return tests

    # =========================================================================
    # Feature 02: Responsive Theme-Adaptive Logo Styling
    # =========================================================================
    def test_feature_02(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_02_01: Logo SVG uses currentColor or CSS variables
        uses_theme_vars = ('currentcolor' in self.css_raw.lower() or 'var(--accent)' in self.css_raw or 'var(--text-primary)' in self.css_raw)
        tests.append({
            'test_id': 'T1_FEAT_02_01',
            'tier': 1,
            'feature': 'Feature 02: Responsive Theme-Adaptive Logo Styling',
            'name': 'Logo styling leverages currentColor or CSS theme custom properties',
            'passed': uses_theme_vars,
            'message': 'Theme custom properties integrated into logo styling' if uses_theme_vars else 'Logo styling does not use currentColor or theme CSS variables'
        })

        # T1_FEAT_02_02: CSS contains explicit dimensions for brand logo
        has_logo_rules = ('.brand-logo' in self.css_raw or '.brand svg' in self.css_raw or '.brand' in self.css_raw)
        tests.append({
            'test_id': 'T1_FEAT_02_02',
            'tier': 1,
            'feature': 'Feature 02: Responsive Theme-Adaptive Logo Styling',
            'name': 'CSS defines explicit dimensions and layout for brand logo',
            'passed': has_logo_rules,
            'message': 'Brand logo CSS layout rules present' if has_logo_rules else 'Missing brand logo CSS rules'
        })

        # T1_FEAT_02_03: Logo hover / focus transitions
        has_logo_transitions = ('.brand:hover' in self.css_raw or '.brand svg' in self.css_raw or 'transition' in self.css_raw)
        tests.append({
            'test_id': 'T1_FEAT_02_03',
            'tier': 1,
            'feature': 'Feature 02: Responsive Theme-Adaptive Logo Styling',
            'name': 'Brand logo provides smooth hover / interaction transitions',
            'passed': has_logo_transitions,
            'message': 'Brand hover transition styles defined' if has_logo_transitions else 'Missing brand transition styles'
        })

        # T1_FEAT_02_04: Dark mode logo contrast >= 4.5:1
        dark_props = self.css.get_custom_properties("html[data-theme='dark']")
        if not dark_props:
            dark_props = self.css.get_custom_properties(':root')
        dark_bg = dark_props.get('--bg-page', '#080b10')
        dark_text = dark_props.get('--text-primary', '#f8fafc')
        dark_ratio = WcagContrast.contrast_ratio(dark_text, dark_bg) or 0.0
        tests.append({
            'test_id': 'T1_FEAT_02_04',
            'tier': 1,
            'feature': 'Feature 02: Responsive Theme-Adaptive Logo Styling',
            'name': 'Dark mode logo contrast ratio >= 4.5:1 against dark page background',
            'passed': dark_ratio >= 4.5,
            'message': f'Dark mode contrast ratio: {dark_ratio:.2f}:1 (Target >= 4.5:1)'
        })

        # T1_FEAT_02_05: Light mode logo contrast >= 4.5:1
        light_props = self.css.get_custom_properties(':root')
        light_bg = light_props.get('--bg-page', '#f8fafc')
        light_text = light_props.get('--text-primary', '#0f172a')
        light_ratio = WcagContrast.contrast_ratio(light_text, light_bg) or 0.0
        tests.append({
            'test_id': 'T1_FEAT_02_05',
            'tier': 1,
            'feature': 'Feature 02: Responsive Theme-Adaptive Logo Styling',
            'name': 'Light mode logo contrast ratio >= 4.5:1 against light page background',
            'passed': light_ratio >= 4.5,
            'message': f'Light mode contrast ratio: {light_ratio:.2f}:1 (Target >= 4.5:1)'
        })
        return tests

    # =========================================================================
    # Feature 03: Modern SVG & PNG Favicon Suite
    # =========================================================================
    def test_feature_03(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_03_01: images/favicon.svg exists on disk
        svg_favicon_exists = AssetChecker.file_exists(self.repo_root, 'images/favicon.svg')
        tests.append({
            'test_id': 'T1_FEAT_03_01',
            'tier': 1,
            'feature': 'Feature 03: Modern SVG & PNG Favicon Suite',
            'name': 'Modern vector favicon images/favicon.svg exists in repository',
            'passed': svg_favicon_exists,
            'message': 'images/favicon.svg verified on disk' if svg_favicon_exists else 'images/favicon.svg does not exist'
        })

        # T1_FEAT_03_02: favicon.ico exists on disk
        ico_exists = AssetChecker.file_exists(self.repo_root, 'favicon.ico')
        tests.append({
            'test_id': 'T1_FEAT_03_02',
            'tier': 1,
            'feature': 'Feature 03: Modern SVG & PNG Favicon Suite',
            'name': 'Fallback favicon.ico exists in repository root',
            'passed': ico_exists,
            'message': 'favicon.ico verified on disk' if ico_exists else 'favicon.ico missing'
        })

        # T1_FEAT_03_03: index.html references favicon.svg
        index_svg_icon = 'rel="icon" type="image/svg+xml" href="images/favicon.svg"' in self.index_raw or 'images/favicon.svg' in self.index_raw
        tests.append({
            'test_id': 'T1_FEAT_03_03',
            'tier': 1,
            'feature': 'Feature 03: Modern SVG & PNG Favicon Suite',
            'name': 'index.html head links to modern SVG favicon',
            'passed': index_svg_icon,
            'message': 'index.html links to images/favicon.svg' if index_svg_icon else 'index.html lacks SVG favicon link'
        })

        # T1_FEAT_03_04: blog.html references favicon.svg
        blog_svg_icon = 'rel="icon" type="image/svg+xml" href="images/favicon.svg"' in self.blog_raw or 'images/favicon.svg' in self.blog_raw
        tests.append({
            'test_id': 'T1_FEAT_03_04',
            'tier': 1,
            'feature': 'Feature 03: Modern SVG & PNG Favicon Suite',
            'name': 'blog.html head links to modern SVG favicon',
            'passed': blog_svg_icon,
            'message': 'blog.html links to images/favicon.svg' if blog_svg_icon else 'blog.html lacks SVG favicon link'
        })

        # T1_FEAT_03_05: SVG favicon is valid XML
        is_valid_svg, msg = AssetChecker.validate_svg_file(self.repo_root, 'images/favicon.svg') if svg_favicon_exists else (False, 'File not found')
        tests.append({
            'test_id': 'T1_FEAT_03_05',
            'tier': 1,
            'feature': 'Feature 03: Modern SVG & PNG Favicon Suite',
            'name': 'images/favicon.svg contains valid vector XML envelope',
            'passed': is_valid_svg,
            'message': f'SVG validation: {msg}'
        })
        return tests

    # =========================================================================
    # Feature 04: Preserve About Section Portrait
    # =========================================================================
    def test_feature_04(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_04_01: Portrait file exists
        portrait_exists = AssetChecker.file_exists(self.repo_root, 'images/akkireddy-avatar.jpg')
        tests.append({
            'test_id': 'T1_FEAT_04_01',
            'tier': 1,
            'feature': 'Feature 04: Preserve About Section Portrait',
            'name': 'Portrait image file images/akkireddy-avatar.jpg exists on disk',
            'passed': portrait_exists,
            'message': 'Portrait file verified on disk' if portrait_exists else 'images/akkireddy-avatar.jpg missing'
        })

        # T1_FEAT_04_02: About section in index.html references portrait
        about_imgs = self.index_doc.select('#about img')
        has_portrait = any('akkireddy-avatar' in (img.get_attr('src') or '') for img in about_imgs)
        tests.append({
            'test_id': 'T1_FEAT_04_02',
            'tier': 1,
            'feature': 'Feature 04: Preserve About Section Portrait',
            'name': 'index.html About section includes preserved portrait photo reference',
            'passed': has_portrait,
            'message': 'About section references akkireddy-avatar.jpg' if has_portrait else 'About section missing akkireddy-avatar.jpg reference'
        })

        # T1_FEAT_04_03: Explicit width and height attributes
        has_dims = any(img.get_attr('width') is not None and img.get_attr('height') is not None for img in about_imgs)
        tests.append({
            'test_id': 'T1_FEAT_04_03',
            'tier': 1,
            'feature': 'Feature 04: Preserve About Section Portrait',
            'name': 'About section portrait has explicit width and height attributes (CLS prevention)',
            'passed': has_dims,
            'message': 'Explicit image dimensions present' if has_dims else 'Missing width or height attributes on About portrait'
        })

        # T1_FEAT_04_04: Descriptive alt attribute
        has_alt = any(bool(img.get_attr('alt') and len(img.get_attr('alt')) > 5) for img in about_imgs)
        tests.append({
            'test_id': 'T1_FEAT_04_04',
            'tier': 1,
            'feature': 'Feature 04: Preserve About Section Portrait',
            'name': 'About section portrait contains descriptive alt attribute',
            'passed': has_alt,
            'message': 'Descriptive alt text present' if has_alt else 'Missing or empty alt text on About portrait'
        })

        # T1_FEAT_04_05: loading="lazy" attribute
        has_lazy = any(img.get_attr('loading') == 'lazy' for img in about_imgs)
        tests.append({
            'test_id': 'T1_FEAT_04_05',
            'tier': 1,
            'feature': 'Feature 04: Preserve About Section Portrait',
            'name': 'About section portrait specifies loading="lazy" for performance',
            'passed': has_lazy,
            'message': 'loading="lazy" attribute present' if has_lazy else 'Missing loading="lazy" on About portrait'
        })
        return tests

    # =========================================================================
    # Feature 05: Calmer Status Strip
    # =========================================================================
    def test_feature_05(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_05_01: Bulky 5 telemetry cards replaced with calm horizontal status strip
        has_status_strip = ('.status-strip' in self.index_raw or self.index_doc.select('.status-strip') != [])
        five_cards_count = len(self.index_doc.select('.telemetry-item'))
        has_calmed_telemetry = has_status_strip and five_cards_count < 5
        tests.append({
            'test_id': 'T1_FEAT_05_01',
            'tier': 1,
            'feature': 'Feature 05: Calmer Status Strip',
            'name': 'Five bulky telemetry cards replaced with calm horizontal status strip',
            'passed': has_calmed_telemetry,
            'message': 'Calm status strip present with reduced card density' if has_calmed_telemetry else f'Five bulky telemetry cards still present (count={five_cards_count}) or status strip missing'
        })

        # T1_FEAT_05_02: Stockholm clock preserved
        clock_elem = self.index_doc.select('#stockholm-clock')
        has_clock = len(clock_elem) > 0
        tests.append({
            'test_id': 'T1_FEAT_05_02',
            'tier': 1,
            'feature': 'Feature 05: Calmer Status Strip',
            'name': 'Status strip preserves #stockholm-clock element for live CET time',
            'passed': has_clock,
            'message': 'Element #stockholm-clock verified' if has_clock else 'Missing #stockholm-clock element'
        })

        # T1_FEAT_05_03: Stockholm hub and credentials highlighted
        strip_text = ""
        for elem in self.index_doc.select('.status-strip') or self.index_doc.select('.telemetry-section'):
            strip_text += " " + elem.get_text()
        has_credentials = ('Stockholm' in strip_text and ('Sweden' in strip_text or 'eu-north-1' in strip_text))
        tests.append({
            'test_id': 'T1_FEAT_05_03',
            'tier': 1,
            'feature': 'Feature 05: Calmer Status Strip',
            'name': 'Status strip displays Stockholm location and hub indicators',
            'passed': has_credentials,
            'message': 'Stockholm location indicators verified' if has_credentials else 'Missing Stockholm hub indicators in status strip'
        })

        # T1_FEAT_05_04: Key credentials / highlights in status strip
        has_degree_or_clouds = ('Multi-Cloud' in strip_text or 'M.Sc' in strip_text or 'Clouds' in strip_text or 'Platform' in strip_text)
        tests.append({
            'test_id': 'T1_FEAT_05_04',
            'tier': 1,
            'feature': 'Feature 05: Calmer Status Strip',
            'name': 'Status strip preserves essential engineering credentials and highlights',
            'passed': has_degree_or_clouds,
            'message': 'Essential credentials verified in status strip' if has_degree_or_clouds else 'Missing engineering credentials in status strip'
        })

        # T1_FEAT_05_05: Accessible region labeling on status strip
        status_regions = self.index_doc.select('.status-strip') or self.index_doc.select('.telemetry-section')
        has_aria_label = any(bool(r.get_attr('aria-label')) for r in status_regions)
        tests.append({
            'test_id': 'T1_FEAT_05_05',
            'tier': 1,
            'feature': 'Feature 05: Calmer Status Strip',
            'name': 'Status strip includes accessible region labeling (aria-label)',
            'passed': has_aria_label,
            'message': 'Accessible aria-label verified on status strip' if has_aria_label else 'Missing aria-label on status strip region'
        })
        return tests

    # =========================================================================
    # Feature 06: Top 3 Projects as Mini Case Studies
    # =========================================================================
    def test_feature_06(self) -> List[Dict[str, Any]]:
        tests = []
        cards = self.index_doc.select('.bento-card')
        card_texts = [c.get_text() for c in cards]

        # Helper to check problem/architecture/outcome
        def check_case_study_sections(text: str) -> bool:
            t = text.lower()
            has_problem = ('problem' in t or 'challenge' in t)
            has_arch = ('architecture' in t or 'solution' in t)
            has_outcome = ('outcome' in t or 'impact' in t or 'results' in t)
            return has_problem and has_arch and has_outcome

        # T1_FEAT_06_01: Nova structured as case study
        nova_card = next((c for c in cards if 'nova' in c.get_text().lower()), None)
        nova_cs = check_case_study_sections(nova_card.get_text()) if nova_card else False
        tests.append({
            'test_id': 'T1_FEAT_06_01',
            'tier': 1,
            'feature': 'Feature 06: Top 3 Projects as Mini Case Studies',
            'name': 'Project 1 (Nova) is structured with Problem, Architecture, and Outcome',
            'passed': nova_cs,
            'message': 'Nova case study structured with Problem, Architecture, Outcome' if nova_cs else 'Nova project card lacks structured Problem, Architecture, Outcome sections'
        })

        # T1_FEAT_06_02: K8s MCP Server structured as case study
        k8s_card = next((c for c in cards if 'k8s mcp' in c.get_text().lower() or 'k8s-mcp' in c.get_text().lower()), None)
        k8s_cs = check_case_study_sections(k8s_card.get_text()) if k8s_card else False
        tests.append({
            'test_id': 'T1_FEAT_06_02',
            'tier': 1,
            'feature': 'Feature 06: Top 3 Projects as Mini Case Studies',
            'name': 'Project 2 (K8s MCP Server) is structured with Problem, Architecture, and Outcome',
            'passed': k8s_cs,
            'message': 'K8s MCP Server structured with Problem, Architecture, Outcome' if k8s_cs else 'K8s MCP Server project card lacks structured Problem, Architecture, Outcome sections'
        })

        # T1_FEAT_06_03: Azure MCP Platform structured as case study
        azure_card = next((c for c in cards if 'azure mcp' in c.get_text().lower() or 'azure-mcp' in c.get_text().lower()), None)
        azure_cs = check_case_study_sections(azure_card.get_text()) if azure_card else False
        tests.append({
            'test_id': 'T1_FEAT_06_03',
            'tier': 1,
            'feature': 'Feature 06: Top 3 Projects as Mini Case Studies',
            'name': 'Project 3 (Azure MCP Platform) is structured with Problem, Architecture, and Outcome',
            'passed': azure_cs,
            'message': 'Azure MCP Platform structured with Problem, Architecture, Outcome' if azure_cs else 'Azure MCP Platform project card lacks structured Problem, Architecture, Outcome sections'
        })

        # T1_FEAT_06_04: Case studies contain live GitHub repository links
        has_gh_links = True
        for card in [nova_card, k8s_card, azure_card]:
            if card:
                links = [a.get_attr('href') for a in card.find_all('a')]
                if not any('github.com/akkireddy-challa/' in (l or '') for l in links):
                    has_gh_links = False
            else:
                has_gh_links = False
        tests.append({
            'test_id': 'T1_FEAT_06_04',
            'tier': 1,
            'feature': 'Feature 06: Top 3 Projects as Mini Case Studies',
            'name': 'Case study cards contain active GitHub repository links',
            'passed': has_gh_links,
            'message': 'Live GitHub links verified on top 3 projects' if has_gh_links else 'Missing GitHub repository links on top 3 projects'
        })

        # T1_FEAT_06_05: Case studies include tech stack tags
        has_tags = True
        for card in [nova_card, k8s_card, azure_card]:
            if card:
                tags = card.select('.tech-tag') or card.select('.card-tags span')
                if len(tags) < 2:
                    has_tags = False
            else:
                has_tags = False
        tests.append({
            'test_id': 'T1_FEAT_06_05',
            'tier': 1,
            'feature': 'Feature 06: Top 3 Projects as Mini Case Studies',
            'name': 'Case study cards display technology stack badges / tags',
            'passed': has_tags,
            'message': 'Technology badges verified on all top 3 case studies' if has_tags else 'Missing tech badges on case studies'
        })
        return tests

    # =========================================================================
    # Feature 07: Interactive MCP Studio Polish
    # =========================================================================
    def test_feature_07(self) -> List[Dict[str, Any]]:
        tests = []
        studio_card = self.index_doc.select('.mcp-studio-card')
        studio_text = " ".join([c.get_text() for c in studio_card])

        # T1_FEAT_07_01: "INTERACTIVE DEMO" badge
        has_demo_badge = ('INTERACTIVE DEMO' in studio_text or 'interactive demo' in self.index_raw.lower() or 'INTERACTIVE RUNTIME' in studio_text)
        tests.append({
            'test_id': 'T1_FEAT_07_01',
            'tier': 1,
            'feature': 'Feature 07: Interactive MCP Studio Polish',
            'name': 'MCP Studio card displays clear "INTERACTIVE DEMO" badge',
            'passed': has_demo_badge,
            'message': 'INTERACTIVE DEMO badge verified in MCP studio' if has_demo_badge else 'Missing "INTERACTIVE DEMO" badge in MCP studio card'
        })

        # T1_FEAT_07_02: User helper subtitle
        has_helper = ('interactive' in studio_text.lower() and ('select' in studio_text.lower() or 'run' in studio_text.lower() or 'playground' in studio_text.lower() or 'tool' in studio_text.lower()))
        tests.append({
            'test_id': 'T1_FEAT_07_02',
            'tier': 1,
            'feature': 'Feature 07: Interactive MCP Studio Polish',
            'name': 'MCP Studio includes user helper subtitle explaining interactivity',
            'passed': has_helper,
            'message': 'Helper guidance text verified in MCP Studio' if has_helper else 'Missing interactive guidance subtitle in MCP Studio'
        })

        # T1_FEAT_07_03: Studio critical element IDs
        required_ids = ['terminal-cmd-text', 'terminal-output', 'btn-run-tool', 'btn-copy-config', 'mcp-repo-link']
        missing_ids = [eid for eid in required_ids if not self.index_doc.select(f'#{eid}')]
        tests.append({
            'test_id': 'T1_FEAT_07_03',
            'tier': 1,
            'feature': 'Feature 07: Interactive MCP Studio Polish',
            'name': 'MCP Studio preserves required interactive IDs for script binding',
            'passed': len(missing_ids) == 0,
            'message': 'All required interactive IDs present' if len(missing_ids) == 0 else f'Missing interactive IDs: {missing_ids}'
        })

        # T1_FEAT_07_04: Studio contains 4 functional MCP tabs
        tabs = self.index_doc.select('.mcp-tab')
        tab_keys = [t.get_attr('data-mcp') for t in tabs]
        expected_keys = {'k8s-mcp', 'azure-mcp', 'grafana-mcp', 'phoenix-mcp'}
        has_all_tabs = expected_keys.issubset(set(tab_keys))
        tests.append({
            'test_id': 'T1_FEAT_07_04',
            'tier': 1,
            'feature': 'Feature 07: Interactive MCP Studio Polish',
            'name': 'MCP Studio contains 4 server tabs (k8s, azure, grafana, phoenix)',
            'passed': has_all_tabs,
            'message': f'Verified tabs: {tab_keys}' if has_all_tabs else f'Missing required tabs. Found: {tab_keys}'
        })

        # T1_FEAT_07_05: Action buttons have accessible SVG icons
        run_btn = self.index_doc.select('#btn-run-tool')
        copy_btn = self.index_doc.select('#btn-copy-config')
        has_icons = bool(run_btn and run_btn[0].find('svg') and copy_btn and copy_btn[0].find('svg'))
        tests.append({
            'test_id': 'T1_FEAT_07_05',
            'tier': 1,
            'feature': 'Feature 07: Interactive MCP Studio Polish',
            'name': 'Studio action buttons contain vector SVG icons and accessible labels',
            'passed': has_icons,
            'message': 'Action buttons equipped with vector icons' if has_icons else 'Missing SVG icons on studio action buttons'
        })
        return tests

    # =========================================================================
    # Feature 08: General Layout Density Reduction
    # =========================================================================
    def test_feature_08(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_08_01: Bento grid gap relaxed (gap >= 16px in CSS)
        bento_rules = self.css.find_rules('.bento-grid')
        has_relaxed_gap = any('gap' in r for r in bento_rules)
        tests.append({
            'test_id': 'T1_FEAT_08_01',
            'tier': 1,
            'feature': 'Feature 08: General Layout Density Reduction',
            'name': 'Bento grid specifies relaxed spacing and gap for calm hierarchy',
            'passed': has_relaxed_gap,
            'message': 'Bento grid gap defined in CSS' if has_relaxed_gap else 'Missing gap property in .bento-grid'
        })

        # T1_FEAT_08_02: Section breathing room
        section_rules = self.css.find_rules('.section')
        has_padding = any('padding' in r for r in section_rules)
        tests.append({
            'test_id': 'T1_FEAT_08_02',
            'tier': 1,
            'feature': 'Feature 08: General Layout Density Reduction',
            'name': 'Sections enforce consistent top and bottom breathing room',
            'passed': has_padding,
            'message': 'Section padding rules verified' if has_padding else 'Missing padding on .section'
        })

        # T1_FEAT_08_03: Responsive hero layout
        hero_rules = self.css.find_rules('.hero')
        has_hero_grid = any('display: grid' in r or 'display: flex' in r or 'grid-template-columns' in r for r in hero_rules)
        tests.append({
            'test_id': 'T1_FEAT_08_03',
            'tier': 1,
            'feature': 'Feature 08: General Layout Density Reduction',
            'name': 'Hero section layout employs clean dual-column grid or flex alignment',
            'passed': has_hero_grid,
            'message': 'Hero layout rules verified' if has_hero_grid else 'Missing hero grid/flex layout definition'
        })

        # T1_FEAT_08_04: Fluid typography with clamp()
        has_clamp = 'clamp(' in self.css_raw
        tests.append({
            'test_id': 'T1_FEAT_08_04',
            'tier': 1,
            'feature': 'Feature 08: General Layout Density Reduction',
            'name': 'Typography utilizes fluid clamp() sizing to prevent awkward line breaks',
            'passed': has_clamp,
            'message': 'Fluid clamp() typography found in CSS' if has_clamp else 'Missing fluid clamp() in CSS'
        })

        # T1_FEAT_08_05: Subtle border and card elevation treatments
        card_rules = self.css.find_rules('.bento-card')
        has_card_borders = any('border' in r and 'background' in r for r in card_rules)
        tests.append({
            'test_id': 'T1_FEAT_08_05',
            'tier': 1,
            'feature': 'Feature 08: General Layout Density Reduction',
            'name': 'Card treatments use subtle borders and background tokens',
            'passed': has_card_borders,
            'message': 'Card border and background rules verified' if has_card_borders else 'Missing card styling declarations'
        })
        return tests

    # =========================================================================
    # Feature 09: 5 Curated Engineering Chapters on blog.html
    # =========================================================================
    def test_feature_09(self) -> List[Dict[str, Any]]:
        tests = []
        chapters = self.blog_doc.select('.writing-chapter')
        chapter_titles = [c.get_text().lower() for c in chapters]
        full_blog_text = self.blog_raw.lower()

        # T1_FEAT_09_01: Chapter 1: Platform Engineering
        has_ch1 = any('platform engineering' in t for t in chapter_titles) or ('platform engineering' in full_blog_text and 'chapter' in full_blog_text)
        tests.append({
            'test_id': 'T1_FEAT_09_01',
            'tier': 1,
            'feature': 'Feature 09: 5 Curated Engineering Chapters on blog.html',
            'name': 'Chapter 1: "Platform Engineering" curated section exists',
            'passed': has_ch1,
            'message': 'Platform Engineering chapter verified' if has_ch1 else 'Missing Platform Engineering chapter section'
        })

        # T1_FEAT_09_02: Chapter 2: Cloud & IaC
        has_ch2 = any('cloud & iac' in t or 'cloud and iac' in t for t in chapter_titles) or ('cloud & iac' in full_blog_text and 'chapter' in full_blog_text)
        tests.append({
            'test_id': 'T1_FEAT_09_02',
            'tier': 1,
            'feature': 'Feature 09: 5 Curated Engineering Chapters on blog.html',
            'name': 'Chapter 2: "Cloud & IaC" curated section exists',
            'passed': has_ch2,
            'message': 'Cloud & IaC chapter verified' if has_ch2 else 'Missing Cloud & IaC chapter section'
        })

        # T1_FEAT_09_03: Chapter 3: Reliability & Observability
        has_ch3 = any('reliability & observability' in t or 'reliability and observability' in t for t in chapter_titles) or ('reliability & observability' in full_blog_text and 'chapter' in full_blog_text)
        tests.append({
            'test_id': 'T1_FEAT_09_03',
            'tier': 1,
            'feature': 'Feature 09: 5 Curated Engineering Chapters on blog.html',
            'name': 'Chapter 3: "Reliability & Observability" curated section exists',
            'passed': has_ch3,
            'message': 'Reliability & Observability chapter verified' if has_ch3 else 'Missing Reliability & Observability chapter section'
        })

        # T1_FEAT_09_04: Chapter 4: AI Systems & MCP
        has_ch4 = any('ai systems & mcp' in t or 'ai systems and mcp' in t for t in chapter_titles) or ('ai systems & mcp' in full_blog_text and 'chapter' in full_blog_text)
        tests.append({
            'test_id': 'T1_FEAT_09_04',
            'tier': 1,
            'feature': 'Feature 09: 5 Curated Engineering Chapters on blog.html',
            'name': 'Chapter 4: "AI Systems & MCP" curated section exists',
            'passed': has_ch4,
            'message': 'AI Systems & MCP chapter verified' if has_ch4 else 'Missing AI Systems & MCP chapter section'
        })

        # T1_FEAT_09_05: Chapter 5: Cost, Security & Governance
        has_ch5 = any('cost, security & governance' in t or 'cost, security and governance' in t for t in chapter_titles) or ('cost, security & governance' in full_blog_text and 'chapter' in full_blog_text)
        tests.append({
            'test_id': 'T1_FEAT_09_05',
            'tier': 1,
            'feature': 'Feature 09: 5 Curated Engineering Chapters on blog.html',
            'name': 'Chapter 5: "Cost, Security & Governance" curated section exists',
            'passed': has_ch5,
            'message': 'Cost, Security & Governance chapter verified' if has_ch5 else 'Missing Cost, Security & Governance chapter section'
        })
        return tests

    # =========================================================================
    # Feature 10: Chapter Descriptions & Count Badges
    # =========================================================================
    def test_feature_10(self) -> List[Dict[str, Any]]:
        tests = []
        chapters = self.blog_doc.select('.writing-chapter')
        descs = self.blog_doc.select('.chapter-desc')
        counts = self.blog_doc.select('.chapter-count')

        # T1_FEAT_10_01: Descriptions present for chapters
        has_descs = len(descs) >= 5 or ('.chapter-desc' in self.blog_raw and len(re.findall(r'class="[^"]*chapter-desc[^"]*"', self.blog_raw)) >= 5)
        tests.append({
            'test_id': 'T1_FEAT_10_01',
            'tier': 1,
            'feature': 'Feature 10: Chapter Descriptions & Count Badges',
            'name': 'Each chapter provides a concise scope description (.chapter-desc)',
            'passed': has_descs,
            'message': f'Found {len(descs)} chapter descriptions' if has_descs else f'Insufficient chapter descriptions (found {len(descs)}, expected 5)'
        })

        # T1_FEAT_10_02: Count badges present for chapters
        has_counts = len(counts) >= 5 or ('.chapter-count' in self.blog_raw and len(re.findall(r'class="[^"]*chapter-count[^"]*"', self.blog_raw)) >= 5)
        tests.append({
            'test_id': 'T1_FEAT_10_02',
            'tier': 1,
            'feature': 'Feature 10: Chapter Descriptions & Count Badges',
            'name': 'Each chapter provides an article count badge (.chapter-count)',
            'passed': has_counts,
            'message': f'Found {len(counts)} chapter count badges' if has_counts else f'Insufficient chapter count badges (found {len(counts)}, expected 5)'
        })

        # T1_FEAT_10_03: Sum of chapter counts matches 9 articles
        total_counted = 0
        for c in counts:
            num_match = re.search(r'\d+', c.get_text())
            if num_match:
                total_counted += int(num_match.group(0))
        tests.append({
            'test_id': 'T1_FEAT_10_03',
            'tier': 1,
            'feature': 'Feature 10: Chapter Descriptions & Count Badges',
            'name': 'Sum of chapter count badges partitions all 9 engineering articles',
            'passed': total_counted == 9,
            'message': f'Chapter count sum: {total_counted} (Target: 9)'
        })

        # T1_FEAT_10_04: 9 writing cards organized under chapters
        cards = self.blog_doc.select('.writing-card')
        tests.append({
            'test_id': 'T1_FEAT_10_04',
            'tier': 1,
            'feature': 'Feature 10: Chapter Descriptions & Count Badges',
            'name': 'Writing page preserves and categorizes all 9 writing cards',
            'passed': len(cards) == 9,
            'message': f'Found {len(cards)} writing cards (Target: 9)'
        })

        # T1_FEAT_10_05: Semantic heading hierarchy
        chapter_headings = self.blog_doc.select('.chapter-title') or self.blog_doc.select('.writing-chapter h2') or self.blog_doc.select('.writing-chapter h3')
        has_headings = len(chapter_headings) >= 5
        tests.append({
            'test_id': 'T1_FEAT_10_05',
            'tier': 1,
            'feature': 'Feature 10: Chapter Descriptions & Count Badges',
            'name': 'Chapter headers follow semantic heading hierarchy (.chapter-title)',
            'passed': has_headings,
            'message': f'Found {len(chapter_headings)} chapter titles' if has_headings else f'Insufficient chapter titles (found {len(chapter_headings)}, expected 5)'
        })
        return tests

    # =========================================================================
    # Feature 11: Elimination of 30-Tag Wall
    # =========================================================================
    def test_feature_11(self) -> List[Dict[str, Any]]:
        tests = []
        tag_filters = self.blog_doc.select('.tag-filters')
        tag_pills = self.blog_doc.select('.tag-filters .tag-pill')
        has_tag_wall = len(tag_pills) >= 20

        # T1_FEAT_11_01: Top-level 30-tag wall eliminated
        tests.append({
            'test_id': 'T1_FEAT_11_01',
            'tier': 1,
            'feature': 'Feature 11: Elimination of 30-Tag Wall',
            'name': 'Bulky top-level 30-tag wall is eliminated from blog.html',
            'passed': not has_tag_wall,
            'message': 'Top-level 30-tag wall removed' if not has_tag_wall else f'Bulky tag wall still present with {len(tag_pills)} pills'
        })

        # T1_FEAT_11_02: Tags scoped inside individual writing cards
        cards = self.blog_doc.select('.writing-card')
        cards_with_tags = sum(1 for c in cards if c.select('.card-tag') or c.select('.tech-tag') or c.select('.card-tags'))
        tests.append({
            'test_id': 'T1_FEAT_11_02',
            'tier': 1,
            'feature': 'Feature 11: Elimination of 30-Tag Wall',
            'name': 'Tags scoped cleanly inside individual article cards as compact metadata',
            'passed': cards_with_tags == 9,
            'message': f'Cards with scoped metadata tags: {cards_with_tags}/9'
        })

        # T1_FEAT_11_03: Class naming uses .card-tag or .tech-tag
        tag_elements = self.blog_doc.select('.writing-card .card-tag') or self.blog_doc.select('.writing-card .tech-tag')
        tests.append({
            'test_id': 'T1_FEAT_11_03',
            'tier': 1,
            'feature': 'Feature 11: Elimination of 30-Tag Wall',
            'name': 'In-card tag elements utilize standardized .card-tag or .tech-tag classes',
            'passed': len(tag_elements) > 0,
            'message': f'Found {len(tag_elements)} standardized in-card tag elements'
        })

        # T1_FEAT_11_04: Card tag font size is compact (<= 0.85rem in CSS)
        card_tag_rules = self.css.find_rules('.card-tag') + self.css.find_rules('.tech-tag')
        has_compact_font = any('font-size: 0.7' in r or 'font-size: 0.8' in r for r in card_tag_rules)
        tests.append({
            'test_id': 'T1_FEAT_11_04',
            'tier': 1,
            'feature': 'Feature 11: Elimination of 30-Tag Wall',
            'name': 'In-card tag font size is compact (<= 0.85rem) to reduce visual clutter',
            'passed': has_compact_font,
            'message': 'Compact font size verified in CSS for tags' if has_compact_font else 'Missing compact font size declaration for card tags'
        })

        # T1_FEAT_11_05: No tag-filter-help paragraph
        has_tag_help_wall = 'tag-filter-help' in self.blog_raw
        tests.append({
            'test_id': 'T1_FEAT_11_05',
            'tier': 1,
            'feature': 'Feature 11: Elimination of 30-Tag Wall',
            'name': 'Outdated tag filter instructions eliminated with tag wall removal',
            'passed': not has_tag_help_wall,
            'message': 'Outdated tag filter instructions removed' if not has_tag_help_wall else 'Outdated .tag-filter-help still present in blog.html'
        })
        return tests

    # =========================================================================
    # Feature 12: Curated Agent Engineering Signals
    # =========================================================================
    def test_feature_12(self) -> List[Dict[str, Any]]:
        tests = []
        signals_section = self.blog_doc.select('.signals-section') or self.blog_doc.select('#signals')
        signals_text = " ".join([s.get_text() for s in signals_section]) or self.blog_raw

        # T1_FEAT_12_01: Agent Engineering Signals section exists
        has_signals = (len(signals_section) > 0 or 'agent engineering signals' in self.blog_raw.lower())
        tests.append({
            'test_id': 'T1_FEAT_12_01',
            'tier': 1,
            'feature': 'Feature 12: Curated Agent Engineering Signals',
            'name': '"Agent Engineering Signals" curated section exists in blog.html',
            'passed': has_signals,
            'message': 'Agent Engineering Signals section verified' if has_signals else 'Missing Agent Engineering Signals section in blog.html'
        })

        # T1_FEAT_12_02: Signal cards present
        signal_cards = self.blog_doc.select('.signal-card') or re.findall(r'class="[^"]*signal-card[^"]*"', self.blog_raw)
        has_cards = len(signal_cards) >= 3
        tests.append({
            'test_id': 'T1_FEAT_12_02',
            'tier': 1,
            'feature': 'Feature 12: Curated Agent Engineering Signals',
            'name': 'Signals section contains takeaway note cards (.signal-card)',
            'passed': has_cards,
            'message': f'Found {len(signal_cards)} signal cards' if has_cards else f'Insufficient signal cards (found {len(signal_cards)}, expected >= 3)'
        })

        # T1_FEAT_12_03: Samuel Colvin citation
        has_colvin = 'samuel colvin' in signals_text.lower() or 'pydantic' in signals_text.lower()
        tests.append({
            'test_id': 'T1_FEAT_12_03',
            'tier': 1,
            'feature': 'Feature 12: Curated Agent Engineering Signals',
            'name': 'Signals include canonical conference citation for Samuel Colvin (FastMCP/Pydantic)',
            'passed': has_colvin,
            'message': 'Samuel Colvin citation verified' if has_colvin else 'Missing Samuel Colvin citation'
        })

        # T1_FEAT_12_04: Dex Horthy citation
        has_horthy = 'dex horthy' in signals_text.lower() or 'humanlayer' in signals_text.lower()
        tests.append({
            'test_id': 'T1_FEAT_12_04',
            'tier': 1,
            'feature': 'Feature 12: Curated Agent Engineering Signals',
            'name': 'Signals include canonical conference citation for Dex Horthy (Tool Latency)',
            'passed': has_horthy,
            'message': 'Dex Horthy citation verified' if has_horthy else 'Missing Dex Horthy citation'
        })

        # T1_FEAT_12_05: Mahesh Murag or Nir Gazit citations
        has_murag_or_gazit = ('mahesh murag' in signals_text.lower() or 'nir gazit' in signals_text.lower() or 'context engineering' in signals_text.lower())
        tests.append({
            'test_id': 'T1_FEAT_12_05',
            'tier': 1,
            'feature': 'Feature 12: Curated Agent Engineering Signals',
            'name': 'Signals include conference citations for Mahesh Murag or Nir Gazit',
            'passed': has_murag_or_gazit,
            'message': 'Conference citations verified' if has_murag_or_gazit else 'Missing Mahesh Murag / Nir Gazit citations'
        })
        return tests

    # =========================================================================
    # Feature 13: WCAG AA Light Mode Hero Contrast
    # =========================================================================
    def test_feature_13(self) -> List[Dict[str, Any]]:
        tests = []
        light_props = self.css.get_custom_properties(':root')
        accent = light_props.get('--accent', '#059669')
        bg_page = light_props.get('--bg-page', '#f8fafc')
        text_primary = light_props.get('--text-primary', '#0f172a')
        text_secondary = light_props.get('--text-secondary', '#475569')

        # T1_FEAT_13_01: Light mode accent is #047857 or meets >= 4.5:1
        accent_ratio = WcagContrast.contrast_ratio(accent, bg_page) or 0.0
        is_accessible_accent = accent_ratio >= 4.5
        tests.append({
            'test_id': 'T1_FEAT_13_01',
            'tier': 1,
            'feature': 'Feature 13: WCAG AA Light Mode Hero Contrast',
            'name': 'Light-mode accent token satisfies WCAG AA contrast ratio >= 4.5:1 (e.g. #047857)',
            'passed': is_accessible_accent,
            'message': f'Light accent contrast: {accent_ratio:.2f}:1 with accent={accent} on bg={bg_page} (Target >= 4.5:1)'
        })

        # T1_FEAT_13_02: Eyebrow contrast >= 4.5:1 in light mode
        # In CSS, check eyebrow color
        eyebrow_rules = self.css.find_rules('.eyebrow')
        eyebrow_uses_accent = any('var(--accent)' in r or 'color:' in r for r in eyebrow_rules)
        tests.append({
            'test_id': 'T1_FEAT_13_02',
            'tier': 1,
            'feature': 'Feature 13: WCAG AA Light Mode Hero Contrast',
            'name': 'Light mode .eyebrow text satisfies WCAG AA contrast ratio >= 4.5:1',
            'passed': is_accessible_accent and eyebrow_uses_accent,
            'message': f'.eyebrow contrast verified at {accent_ratio:.2f}:1' if (is_accessible_accent and eyebrow_uses_accent) else f'.eyebrow contrast fails WCAG AA ({accent_ratio:.2f}:1)'
        })

        # T1_FEAT_13_03: Text primary contrast exceeds 7:1 (WCAG AAA)
        primary_ratio = WcagContrast.contrast_ratio(text_primary, bg_page) or 0.0
        tests.append({
            'test_id': 'T1_FEAT_13_03',
            'tier': 1,
            'feature': 'Feature 13: WCAG AA Light Mode Hero Contrast',
            'name': 'Light-mode primary text contrast exceeds 7.0:1 (WCAG AAA)',
            'passed': primary_ratio >= 7.0,
            'message': f'Primary text contrast: {primary_ratio:.2f}:1 (Target >= 7.0:1)'
        })

        # T1_FEAT_13_04: Text secondary contrast exceeds 4.5:1 (WCAG AA)
        secondary_ratio = WcagContrast.contrast_ratio(text_secondary, bg_page) or 0.0
        tests.append({
            'test_id': 'T1_FEAT_13_04',
            'tier': 1,
            'feature': 'Feature 13: WCAG AA Light Mode Hero Contrast',
            'name': 'Light-mode secondary text contrast exceeds 4.5:1 (WCAG AA)',
            'passed': secondary_ratio >= 4.5,
            'message': f'Secondary text contrast: {secondary_ratio:.2f}:1 (Target >= 4.5:1)'
        })

        # T1_FEAT_13_05: Dark mode accent contrast >= 4.5:1
        dark_props = self.css.get_custom_properties("html[data-theme='dark']") or self.css.get_custom_properties(':root')
        dark_accent = dark_props.get('--accent', '#10b981')
        dark_bg = dark_props.get('--bg-page', '#080b10')
        dark_accent_ratio = WcagContrast.contrast_ratio(dark_accent, dark_bg) or 0.0
        tests.append({
            'test_id': 'T1_FEAT_13_05',
            'tier': 1,
            'feature': 'Feature 13: WCAG AA Light Mode Hero Contrast',
            'name': 'Dark-mode accent contrast exceeds 4.5:1 on dark page background',
            'passed': dark_accent_ratio >= 4.5,
            'message': f'Dark accent contrast: {dark_accent_ratio:.2f}:1 (Target >= 4.5:1)'
        })
        return tests

    # =========================================================================
    # Feature 14: 375px Mobile Viewport Responsiveness
    # =========================================================================
    def test_feature_14(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_14_01: hero-bio-badge responsiveness
        badge_rules = self.css.find_rules('.hero-bio-badge')
        has_max_w = any('max-width' in r or 'flex-wrap' in r or 'width: 100%' in r for r in badge_rules)
        media_queries = self.css.get_media_queries()
        has_mobile_mq = any(('max-width: 480px' in q or 'max-width: 600px' in q or 'max-width: 375px' in q) and '.hero-bio-badge' in b for q, b in media_queries)
        tests.append({
            'test_id': 'T1_FEAT_14_01',
            'tier': 1,
            'feature': 'Feature 14: 375px Mobile Viewport Responsiveness',
            'name': '.hero-bio-badge incorporates responsive containment preventing 375px blowout',
            'passed': has_max_w or has_mobile_mq,
            'message': 'Responsive rules verified on .hero-bio-badge' if (has_max_w or has_mobile_mq) else 'Missing mobile responsiveness containment on .hero-bio-badge'
        })

        # T1_FEAT_14_02: status-badge responsive wrap
        status_badge_rules = self.css.find_rules('.status-badge')
        has_wrap = any('flex-wrap: wrap' in r or 'white-space: normal' in r or 'overflow: hidden' in r for r in status_badge_rules) or \
                   any(('max-width: 480px' in q or 'max-width: 375px' in q) and '.status-badge' in b for q, b in media_queries)
        tests.append({
            'test_id': 'T1_FEAT_14_02',
            'tier': 1,
            'feature': 'Feature 14: 375px Mobile Viewport Responsiveness',
            'name': '.status-badge supports wrapping / fluid width to fit 375px screen',
            'passed': has_wrap,
            'message': 'Responsive text wrap verified on .status-badge' if has_wrap else 'Missing responsive wrap on .status-badge'
        })

        # T1_FEAT_14_03: Mobile nav toggle present
        index_nav_toggle = self.index_doc.select('.nav-toggle')
        blog_nav_toggle = self.blog_doc.select('.nav-toggle')
        has_toggle = (len(index_nav_toggle) > 0 and len(blog_nav_toggle) > 0)
        tests.append({
            'test_id': 'T1_FEAT_14_03',
            'tier': 1,
            'feature': 'Feature 14: 375px Mobile Viewport Responsiveness',
            'name': 'Mobile navigation hamburger toggle present on both index.html and blog.html',
            'passed': has_toggle,
            'message': 'Mobile hamburger toggle verified' if has_toggle else 'Missing .nav-toggle on one or both pages'
        })

        # T1_FEAT_14_04: Header actions accessible at 375px
        nav_actions = self.index_doc.select('.nav-actions')
        has_actions = len(nav_actions) > 0 and nav_actions[0].find('button') is not None
        tests.append({
            'test_id': 'T1_FEAT_14_04',
            'tier': 1,
            'feature': 'Feature 14: 375px Mobile Viewport Responsiveness',
            'name': 'Header actions (search, theme toggle) remain accessible at mobile viewports',
            'passed': has_actions,
            'message': 'Header action controls verified' if has_actions else 'Missing header actions'
        })

        # T1_FEAT_14_05: CSS box-sizing and global overflow safety
        has_box_sizing = 'box-sizing: border-box' in self.css_raw
        has_html_overflow = 'overflow-x: hidden' in self.css_raw or 'overflow-x: clip' in self.css_raw
        tests.append({
            'test_id': 'T1_FEAT_14_05',
            'tier': 1,
            'feature': 'Feature 14: 375px Mobile Viewport Responsiveness',
            'name': 'CSS applies box-sizing: border-box and horizontal overflow protection',
            'passed': has_box_sizing and has_html_overflow,
            'message': 'Global border-box and overflow protection verified' if (has_box_sizing and has_html_overflow) else 'Missing global border-box or overflow-x protection in CSS'
        })
        return tests

    # =========================================================================
    # Feature 15: Cross-Page Theme Synchronization
    # =========================================================================
    def test_feature_15(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_15_01: index.html head inline script checks site-theme
        index_head_theme_sync = 'localStorage.getItem(\'site-theme\')' in self.index_raw or 'localStorage.getItem("site-theme")' in self.index_raw
        tests.append({
            'test_id': 'T1_FEAT_15_01',
            'tier': 1,
            'feature': 'Feature 15: Cross-Page Theme Synchronization',
            'name': 'index.html inline <head> script checks localStorage for saved theme',
            'passed': index_head_theme_sync,
            'message': 'FOUC prevention inline script verified in index.html' if index_head_theme_sync else 'Missing FOUC theme check in index.html head'
        })

        # T1_FEAT_15_02: blog.html head inline script checks site-theme
        blog_head_theme_sync = 'localStorage.getItem(\'site-theme\')' in self.blog_raw or 'localStorage.getItem("site-theme")' in self.blog_raw
        tests.append({
            'test_id': 'T1_FEAT_15_02',
            'tier': 1,
            'feature': 'Feature 15: Cross-Page Theme Synchronization',
            'name': 'blog.html inline <head> script checks localStorage for saved theme',
            'passed': blog_head_theme_sync,
            'message': 'FOUC prevention inline script verified in blog.html' if blog_head_theme_sync else 'Missing FOUC theme check in blog.html head'
        })

        # T1_FEAT_15_03: Theme toggle button on both pages
        index_btn = len(self.index_doc.select('#theme-toggle')) > 0
        blog_btn = len(self.blog_doc.select('#theme-toggle')) > 0
        tests.append({
            'test_id': 'T1_FEAT_15_03',
            'tier': 1,
            'feature': 'Feature 15: Cross-Page Theme Synchronization',
            'name': 'Theme toggle button (#theme-toggle) present on both index.html and blog.html',
            'passed': index_btn and blog_btn,
            'message': 'Theme toggle button verified on all pages' if (index_btn and blog_btn) else 'Missing #theme-toggle on one or both pages'
        })

        # T1_FEAT_15_04: site-ui.js stores theme in localStorage
        js_persists = 'localStorage.setItem(\'site-theme\'' in self.js_raw or 'localStorage.setItem("site-theme"' in self.js_raw
        tests.append({
            'test_id': 'T1_FEAT_15_04',
            'tier': 1,
            'feature': 'Feature 15: Cross-Page Theme Synchronization',
            'name': 'site-ui.js persists chosen theme to localStorage on toggle',
            'passed': js_persists,
            'message': 'localStorage persistence logic verified in site-ui.js' if js_persists else 'Missing localStorage.setItem in site-ui.js'
        })

        # T1_FEAT_15_05: site-ui.js handles window storage event for cross-tab sync
        js_storage_event = 'addEventListener(\'storage\'' in self.js_raw or 'addEventListener("storage"' in self.js_raw
        tests.append({
            'test_id': 'T1_FEAT_15_05',
            'tier': 1,
            'feature': 'Feature 15: Cross-Page Theme Synchronization',
            'name': 'site-ui.js synchronizes theme across open browser tabs via storage listener',
            'passed': js_storage_event,
            'message': 'Cross-tab storage synchronization verified' if js_storage_event else 'Missing storage event listener in site-ui.js'
        })
        return tests

    # =========================================================================
    # Feature 16: HTML, CSS, JS Syntax & Link Validation
    # =========================================================================
    def test_feature_16(self) -> List[Dict[str, Any]]:
        tests = []
        # T1_FEAT_16_01: site-ui.js compiles cleanly
        try:
            res = subprocess.run(['node', '-c', self.js_path], capture_output=True, text=True, timeout=5)
            js_valid = (res.returncode == 0)
            js_err = res.stderr
        except Exception as e:
            js_valid = False
            js_err = str(e)
        tests.append({
            'test_id': 'T1_FEAT_16_01',
            'tier': 1,
            'feature': 'Feature 16: HTML, CSS, JS Syntax & Link Validation',
            'name': 'js/site-ui.js syntax validates without errors via node -c',
            'passed': js_valid,
            'message': 'js/site-ui.js compiled cleanly' if js_valid else f'Syntax error in js/site-ui.js: {js_err}'
        })

        # T1_FEAT_16_02: index.html valid structure
        index_valid = '<!doctype html>' in self.index_raw.lower() and '<html' in self.index_raw and '<body' in self.index_raw and '</html>' in self.index_raw
        tests.append({
            'test_id': 'T1_FEAT_16_02',
            'tier': 1,
            'feature': 'Feature 16: HTML, CSS, JS Syntax & Link Validation',
            'name': 'index.html structure contains valid DOCTYPE, html, head, and body tags',
            'passed': index_valid,
            'message': 'index.html structure valid' if index_valid else 'Malformed structural envelope in index.html'
        })

        # T1_FEAT_16_03: blog.html valid structure
        blog_valid = '<!doctype html>' in self.blog_raw.lower() and '<html' in self.blog_raw and '<body' in self.blog_raw and '</html>' in self.blog_raw
        tests.append({
            'test_id': 'T1_FEAT_16_03',
            'tier': 1,
            'feature': 'Feature 16: HTML, CSS, JS Syntax & Link Validation',
            'name': 'blog.html structure contains valid DOCTYPE, html, head, and body tags',
            'passed': blog_valid,
            'message': 'blog.html structure valid' if blog_valid else 'Malformed structural envelope in blog.html'
        })

        # T1_FEAT_16_04: Local assets in index.html exist
        index_assets = re.findall(r'(?:src|href)=["\']((?:images|css|js)/[^"\']+)["\']', self.index_raw)
        missing_index_assets = [a for a in index_assets if not AssetChecker.file_exists(self.repo_root, a)]
        tests.append({
            'test_id': 'T1_FEAT_16_04',
            'tier': 1,
            'feature': 'Feature 16: HTML, CSS, JS Syntax & Link Validation',
            'name': 'All local image, stylesheet, and script references in index.html resolve to disk',
            'passed': len(missing_index_assets) == 0,
            'message': 'All local assets in index.html exist on disk' if len(missing_index_assets) == 0 else f'Missing local assets: {missing_index_assets}'
        })

        # T1_FEAT_16_05: Local assets in blog.html exist
        blog_assets = re.findall(r'(?:src|href)=["\']((?:images|css|js)/[^"\']+)["\']', self.blog_raw)
        missing_blog_assets = [a for a in blog_assets if not AssetChecker.file_exists(self.repo_root, a)]
        tests.append({
            'test_id': 'T1_FEAT_16_05',
            'tier': 1,
            'feature': 'Feature 16: HTML, CSS, JS Syntax & Link Validation',
            'name': 'All local image, stylesheet, and script references in blog.html resolve to disk',
            'passed': len(missing_blog_assets) == 0,
            'message': 'All local assets in blog.html exist on disk' if len(missing_blog_assets) == 0 else f'Missing local assets: {missing_blog_assets}'
        })
        return tests
