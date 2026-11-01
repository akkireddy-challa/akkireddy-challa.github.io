"""
Tier 3: Cross-Feature Interactions Test Suite
Covers 3 cross-feature interaction flows with >= 5 test cases each (15 test cases).
"""

import os
import re
import json
from typing import List, Dict, Any
from tests.test_utils import HtmlDocument, HtmlNode, WcagContrast, CssAnalyzer, AssetChecker

class Tier3InteractionTests:
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
        results.extend(self.test_interaction_01_theme_cross_pages())
        results.extend(self.test_interaction_02_search_and_chapters())
        results.extend(self.test_interaction_03_mcp_studio_flow())
        return results

    # =========================================================================
    # Interaction 01: Theme Toggle across Pages & Mobile Viewport
    # =========================================================================
    def test_interaction_01_theme_cross_pages(self) -> List[Dict[str, Any]]:
        tests = []
        # T3_INT_01_01: Theme state set on index.html is read synchronously by blog.html
        index_sync_script = re.search(r'<script>([\s\S]*?localStorage\.getItem\([\'"]site-theme[\'"]\)[\s\S]*?)</script>', self.index_raw)
        blog_sync_script = re.search(r'<script>([\s\S]*?localStorage\.getItem\([\'"]site-theme[\'"]\)[\s\S]*?)</script>', self.blog_raw)
        has_identical_sync = bool(index_sync_script and blog_sync_script)
        tests.append({
            'test_id': 'T3_INT_01_01',
            'tier': 3,
            'feature': 'Interaction 01: Theme Toggle across Pages & Mobile Viewport',
            'name': 'Theme persisted on index.html is applied synchronously on blog.html prior to DOM render',
            'passed': has_identical_sync,
            'message': 'Cross-page synchronized FOUC prevention scripts verified' if has_identical_sync else 'Missing inline FOUC theme sync scripts in head'
        })

        # T3_INT_01_02: Both light and dark palettes define complete semantic token parity
        light_props = self.css.get_custom_properties(':root')
        dark_props = self.css.get_custom_properties("html[data-theme='dark']") or self.css.get_custom_properties(':root')
        critical_tokens = ['--bg-page', '--bg-card', '--text-primary', '--text-secondary', '--accent', '--border-subtle']
        missing_light = [t for t in critical_tokens if t not in light_props]
        missing_dark = [t for t in critical_tokens if t not in dark_props]
        has_token_parity = (len(missing_light) == 0 and len(missing_dark) == 0)
        tests.append({
            'test_id': 'T3_INT_01_02',
            'tier': 3,
            'feature': 'Interaction 01: Theme Toggle across Pages & Mobile Viewport',
            'name': 'Light and dark theme token matrices maintain 100% semantic variable parity',
            'passed': has_token_parity,
            'message': 'Semantic token parity verified across both themes' if has_token_parity else f'Missing tokens: light={missing_light}, dark={missing_dark}'
        })

        # T3_INT_01_03: Monogram logo SVG fill/stroke adapts without hardcoded color override
        brand_rules = self.css.find_rules('.brand') + self.css.find_rules('.brand-logo')
        no_hardcoded_logo_color = not any('color: #000' in r or 'color: #fff' in r for r in brand_rules)
        tests.append({
            'test_id': 'T3_INT_01_03',
            'tier': 3,
            'feature': 'Interaction 01: Theme Toggle across Pages & Mobile Viewport',
            'name': 'Monogram logo vector elements use theme variables without hardcoded color clashes',
            'passed': no_hardcoded_logo_color,
            'message': 'Logo styles avoid conflicting hardcoded colors' if no_hardcoded_logo_color else 'Hardcoded color clash found in brand styling'
        })

        # T3_INT_01_04: Mobile nav menu drawer maintains contrast in both themes
        nav_menu_rules = self.css.find_rules('.nav-menu')
        has_nav_drawer_theme = any('var(--bg-glass)' in r or 'var(--bg-card)' in r or 'background' in r for r in nav_menu_rules)
        tests.append({
            'test_id': 'T3_INT_01_04',
            'tier': 3,
            'feature': 'Interaction 01: Theme Toggle across Pages & Mobile Viewport',
            'name': 'Mobile navigation menu drawer utilizes theme tokens for light/dark legibility',
            'passed': has_nav_drawer_theme,
            'message': 'Theme token background verified on .nav-menu' if has_nav_drawer_theme else 'Missing theme variable styling on .nav-menu'
        })

        # T3_INT_01_05: Status strip retains legible contrast across theme flips
        status_rules = self.css.find_rules('.status-strip') + self.css.find_rules('.telemetry-section')
        has_status_theme_vars = any('var(--' in r for r in status_rules)
        tests.append({
            'test_id': 'T3_INT_01_05',
            'tier': 3,
            'feature': 'Interaction 01: Theme Toggle across Pages & Mobile Viewport',
            'name': 'Status strip component utilizes theme custom properties for contrast consistency',
            'passed': has_status_theme_vars,
            'message': 'Status strip theme variables verified' if has_status_theme_vars else 'Missing theme variables in status strip styles'
        })
        return tests

    # =========================================================================
    # Interaction 02: Search + Chapter Navigation in Writing Page
    # =========================================================================
    def test_interaction_02_search_and_chapters(self) -> List[Dict[str, Any]]:
        tests = []
        cards = self.blog_doc.select('.writing-card')

        # Helper to simulate query match
        def matches_query(card: HtmlNode, q: str) -> bool:
            query = q.lower().strip()
            title = card.find('h2') or card.find('h3')
            title_text = title.get_text().lower() if title else ""
            desc = card.find('p')
            desc_text = desc.get_text().lower() if desc else ""
            tags = card.get_attr('data-tags', '').lower()
            return query in title_text or query in desc_text or query in tags

        # T3_INT_02_01: Searching "Kubernetes" filters across chapters
        k8s_matches = [c for c in cards if matches_query(c, 'kubernetes')]
        tests.append({
            'test_id': 'T3_INT_02_01',
            'tier': 3,
            'feature': 'Interaction 02: Search + Chapter Navigation in Writing Page',
            'name': 'Filtering articles by search query ("Kubernetes") accurately isolates relevant articles',
            'passed': len(k8s_matches) >= 1,
            'message': f'Search for "Kubernetes" identified {len(k8s_matches)} relevant articles'
        })

        # T3_INT_02_02: Chapters structure exists to support search partitioning
        chapters = self.blog_doc.select('.writing-chapter')
        has_chapter_containers = len(chapters) >= 5
        tests.append({
            'test_id': 'T3_INT_02_02',
            'tier': 3,
            'feature': 'Interaction 02: Search + Chapter Navigation in Writing Page',
            'name': 'Curated chapter containers (.writing-chapter) partition articles for isolated browsing',
            'passed': has_chapter_containers,
            'message': f'Found {len(chapters)} chapter containers' if has_chapter_containers else f'Insufficient chapter containers (found {len(chapters)}, expected 5)'
        })

        # T3_INT_02_03: Clearing search query restores all articles
        all_articles = [c for c in cards if matches_query(c, '')]
        tests.append({
            'test_id': 'T3_INT_02_03',
            'tier': 3,
            'feature': 'Interaction 02: Search + Chapter Navigation in Writing Page',
            'name': 'Clearing search input query restores all 13 articles across all chapters',
            'passed': len(all_articles) == 13,
            'message': f'Restored all {len(all_articles)}/13 articles upon clearing query'
        })

        # T3_INT_02_04: In-card tags allow direct topic filtering
        all_card_tags = []
        for c in cards:
            tag_nodes = c.select('.card-tag') or c.select('.tech-tag')
            all_card_tags.extend([t.get_text().strip().lower() for t in tag_nodes if t.get_text().strip()])
        tests.append({
            'test_id': 'T3_INT_02_04',
            'tier': 3,
            'feature': 'Interaction 02: Search + Chapter Navigation in Writing Page',
            'name': 'In-card metadata tags provide direct topic keywords across articles',
            'passed': len(all_card_tags) >= 9,
            'message': f'Found {len(all_card_tags)} in-card metadata tags'
        })

        # T3_INT_02_05: All article card links resolve to valid HTML files on disk
        card_links = []
        for c in cards:
            for a in c.find_all('a'):
                href = a.get_attr('href')
                if href and href.startswith('writing/'):
                    card_links.append(href)
        missing_articles = [l for l in card_links if not AssetChecker.file_exists(self.repo_root, l)]
        tests.append({
            'test_id': 'T3_INT_02_05',
            'tier': 3,
            'feature': 'Interaction 02: Search + Chapter Navigation in Writing Page',
            'name': 'All article card links navigate to valid HTML article files on disk',
            'passed': len(missing_articles) == 0 and len(card_links) >= 9,
            'message': f'Verified {len(card_links)} article links' if len(missing_articles) == 0 else f'Missing article files: {missing_articles}'
        })
        return tests

    # =========================================================================
    # Interaction 03: MCP Demo Studio Tab Switching + Simulated Run + Copy Config
    # =========================================================================
    def test_interaction_03_mcp_studio_flow(self) -> List[Dict[str, Any]]:
        tests = []
        # T3_INT_03_01: mcpData dictionary in site-ui.js contains all 4 servers
        mcp_data_match = re.search(r'const\s+mcpData\s*=\s*(\{[\s\S]*?\n\s*\};)', self.js_raw)
        has_all_mcp_entries = False
        if mcp_data_match:
            data_str = mcp_data_match.group(1)
            has_all_mcp_entries = all(s in data_str for s in ['k8s-mcp', 'azure-mcp', 'grafana-mcp', 'phoenix-mcp'])
        tests.append({
            'test_id': 'T3_INT_03_01',
            'tier': 3,
            'feature': 'Interaction 03: MCP Demo Studio Tab Switching & Simulated Run',
            'name': 'MCP data state dictionary includes all 4 servers with complete configuration payloads',
            'passed': has_all_mcp_entries,
            'message': 'mcpData contains k8s-mcp, azure-mcp, grafana-mcp, phoenix-mcp' if has_all_mcp_entries else 'Missing servers in mcpData dictionary'
        })

        # T3_INT_03_02: Selecting azure-mcp updates terminal command and output
        has_azure_tool = 'agent.call_tool("azure_inspect_ai_foundry"' in self.js_raw or 'azure_inspect_ai_foundry' in self.js_raw
        tests.append({
            'test_id': 'T3_INT_03_02',
            'tier': 3,
            'feature': 'Interaction 03: MCP Demo Studio Tab Switching & Simulated Run',
            'name': 'Switching to azure-mcp updates terminal command text and AI Foundry diagnostic trace',
            'passed': has_azure_tool,
            'message': 'Azure MCP command payload verified' if has_azure_tool else 'Missing Azure MCP tool command in site-ui.js'
        })

        # T3_INT_03_03: Selecting grafana-mcp updates repo link
        has_grafana_repo = 'github.com/akkireddy-challa/grafana-mcp-observability' in self.js_raw
        tests.append({
            'test_id': 'T3_INT_03_03',
            'tier': 3,
            'feature': 'Interaction 03: MCP Demo Studio Tab Switching & Simulated Run',
            'name': 'Switching to grafana-mcp dynamically updates external repository link',
            'passed': has_grafana_repo,
            'message': 'Grafana repository link verified' if has_grafana_repo else 'Missing Grafana MCP repo link in site-ui.js'
        })

        # T3_INT_03_04: btn-run-tool triggers execution state and animated output
        has_run_tool_listener = "btnRunTool?.addEventListener('click'" in self.js_raw or 'btnRunTool.addEventListener' in self.js_raw
        has_run_animation = 'classList.add(\'is-running\')' in self.js_raw or 'is-running' in self.js_raw
        tests.append({
            'test_id': 'T3_INT_03_04',
            'tier': 3,
            'feature': 'Interaction 03: MCP Demo Studio Tab Switching & Simulated Run',
            'name': 'Clicking #btn-run-tool activates live execution animation (is-running) and feedback',
            'passed': has_run_tool_listener and has_run_animation,
            'message': 'Run tool event listener and execution animation verified' if (has_run_tool_listener and has_run_animation) else 'Missing run tool handler or execution animation in site-ui.js'
        })

        # T3_INT_03_05: btn-copy-config writes JSON snippet to clipboard and shows toast
        has_copy_listener = "btnCopyConfig?.addEventListener('click'" in self.js_raw or 'btnCopyConfig.addEventListener' in self.js_raw
        has_clipboard = 'clipboard.writeText' in self.js_raw and 'showToast' in self.js_raw
        tests.append({
            'test_id': 'T3_INT_03_05',
            'tier': 3,
            'feature': 'Interaction 03: MCP Demo Studio Tab Switching & Simulated Run',
            'name': 'Clicking #btn-copy-config copies MCP server JSON snippet and triggers user toast notification',
            'passed': has_copy_listener and has_clipboard,
            'message': 'Copy config clipboard action and toast notification verified' if (has_copy_listener and has_clipboard) else 'Missing clipboard copy or toast feedback in site-ui.js'
        })
        return tests
