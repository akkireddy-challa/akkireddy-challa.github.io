"""
E2E Test Suite Utilities
Zero-dependency DOM parser, CSS analyzer, WCAG contrast calculator, and asset checker.
"""

import os
import re
import math
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple, Any

class HtmlNode:
    def __init__(self, tag: str, attrs: Dict[str, str], parent: Optional['HtmlNode'] = None):
        self.tag = tag.lower()
        self.attrs = {k.lower(): v for k, v in attrs.items()}
        self.parent = parent
        self.children: List['HtmlNode'] = []
        self.text_content: str = ""

    def add_child(self, child: 'HtmlNode'):
        self.children.append(child)

    def append_text(self, text: str):
        self.text_content += text

    def get_text(self, recursive: bool = True) -> str:
        if not recursive:
            return self.text_content
        parts = [self.text_content]
        for c in self.children:
            parts.append(c.get_text(recursive=True))
        return " ".join("".join(parts).split())

    def get_attr(self, name: str, default: Optional[str] = None) -> Optional[str]:
        return self.attrs.get(name.lower(), default)

    def has_class(self, class_name: str) -> bool:
        classes = self.attrs.get('class', '').split()
        return class_name in classes

    def find_all(self, tag: Optional[str] = None, attrs: Optional[Dict[str, str]] = None) -> List['HtmlNode']:
        results = []
        if tag is not None and tag != '*':
            tag_match = (self.tag == tag.lower())
        else:
            tag_match = True

        attrs_match = True
        if attrs:
            for k, v in attrs.items():
                k_lower = k.lower()
                if k_lower == 'class':
                    required_classes = set(v.split())
                    node_classes = set(self.attrs.get('class', '').split())
                    if not required_classes.issubset(node_classes):
                        attrs_match = False
                        break
                else:
                    if self.attrs.get(k_lower) != v:
                        attrs_match = False
                        break

        if tag_match and attrs_match and self.tag != '__root__':
            results.append(self)

        for child in self.children:
            results.extend(child.find_all(tag, attrs))
        return results

    def find(self, tag: Optional[str] = None, attrs: Optional[Dict[str, str]] = None) -> Optional['HtmlNode']:
        matches = self.find_all(tag, attrs)
        return matches[0] if matches else None

    def select(self, selector: str) -> List['HtmlNode']:
        """Basic CSS selector engine supporting tag, .class, #id, [attr=val], and compound descendant selectors."""
        selector = selector.strip()
        parts = selector.split()
        current_nodes = [self]

        for part in parts:
            next_nodes = []
            for node in current_nodes:
                matches = node._match_single_selector(part)
                next_nodes.extend(matches)
            # Deduplicate preserving order
            seen = set()
            deduped = []
            for n in next_nodes:
                if id(n) not in seen:
                    seen.add(id(n))
                    deduped.append(n)
            current_nodes = deduped
        return current_nodes

    def _match_single_selector(self, selector_part: str) -> List['HtmlNode']:
        target_tag: Optional[str] = None
        target_id: Optional[str] = None
        target_classes: List[str] = []
        target_attrs: Dict[str, str] = {}

        # Parse attribute selectors [attr="val"] or [attr]
        attr_matches = re.findall(r'\[([a-zA-Z0-9_\-]+)(?:=[\'"]?([^\'"\]]+)[\'"]?)?\]', selector_part)
        for attr_name, attr_val in attr_matches:
            target_attrs[attr_name.lower()] = attr_val if attr_val is not None else ''

        clean_part = re.sub(r'\[[^\]]+\]', '', selector_part)

        # Parse ID
        if '#' in clean_part:
            pieces = clean_part.split('#')
            if pieces[0]:
                target_tag = pieces[0].split('.')[0]
            rest = pieces[1]
            if '.' in rest:
                id_and_classes = rest.split('.')
                target_id = id_and_classes[0]
                target_classes.extend(id_and_classes[1:])
            else:
                target_id = rest
        elif '.' in clean_part:
            pieces = clean_part.split('.')
            if pieces[0]:
                target_tag = pieces[0]
            target_classes.extend(pieces[1:])
        else:
            if clean_part:
                target_tag = clean_part

        results = []
        for candidate in self.find_all(target_tag or '*'):
            if target_id and candidate.attrs.get('id') != target_id:
                continue
            if target_classes:
                node_classes = set(candidate.attrs.get('class', '').split())
                if not set(target_classes).issubset(node_classes):
                    continue
            if target_attrs:
                match_attrs = True
                for ak, av in target_attrs.items():
                    if ak not in candidate.attrs:
                        match_attrs = False
                        break
                    if av and candidate.attrs[ak] != av:
                        match_attrs = False
                        break
                if not match_attrs:
                    continue
            results.append(candidate)
        return results


class _TreeBuildingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = HtmlNode('__root__', {})
        self.current = self.root
        self.void_elements = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }

    def handle_starttag(self, tag, attrs):
        node = HtmlNode(tag, dict(attrs), parent=self.current)
        self.current.add_child(node)
        if tag.lower() not in self.void_elements:
            self.current = node

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        node = self.current
        while node is not None and node != self.root:
            if node.tag == tag_lower:
                self.current = node.parent or self.root
                break
            node = node.parent

    def handle_data(self, data):
        if self.current:
            self.current.append_text(data)


class HtmlDocument:
    @classmethod
    def parse(cls, content: str) -> HtmlNode:
        parser = _TreeBuildingParser()
        parser.feed(content)
        return parser.root

    @classmethod
    def parse_file(cls, filepath: str) -> HtmlNode:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return cls.parse(f.read())


class WcagContrast:
    @staticmethod
    def parse_color(color_str: str) -> Optional[Tuple[int, int, int]]:
        color_str = color_str.strip().lower()
        # Handle Hex
        if color_str.startswith('#'):
            hex_val = color_str.lstrip('#')
            if len(hex_val) == 3:
                r = int(hex_val[0] * 2, 16)
                g = int(hex_val[1] * 2, 16)
                b = int(hex_val[2] * 2, 16)
                return (r, g, b)
            elif len(hex_val) >= 6:
                r = int(hex_val[0:2], 16)
                g = int(hex_val[2:4], 16)
                b = int(hex_val[4:6], 16)
                return (r, g, b)

        # Handle rgb(r, g, b) or rgba(r, g, b, a)
        rgb_match = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
        if rgb_match:
            r = int(rgb_match.group(1))
            g = int(rgb_match.group(2))
            b = int(rgb_match.group(3))
            return (r, g, b)

        return None

    @staticmethod
    def srgb_to_linear(c_srgb: float) -> float:
        c = c_srgb / 255.0
        if c <= 0.04045:
            return c / 12.92
        return math.pow((c + 0.055) / 1.055, 2.4)

    @classmethod
    def relative_luminance(cls, r: int, g: int, b: int) -> float:
        r_lin = cls.srgb_to_linear(r)
        g_lin = cls.srgb_to_linear(g)
        b_lin = cls.srgb_to_linear(b)
        return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

    @classmethod
    def contrast_ratio(cls, color1_str: str, color2_str: str) -> Optional[float]:
        c1 = cls.parse_color(color1_str)
        c2 = cls.parse_color(color2_str)
        if not c1 or not c2:
            return None
        l1 = cls.relative_luminance(*c1)
        l2 = cls.relative_luminance(*c2)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    @classmethod
    def meets_wcag_aa(cls, fg: str, bg: str, is_large_text: bool = False) -> Tuple[bool, float]:
        ratio = cls.contrast_ratio(fg, bg)
        if ratio is None:
            return False, 0.0
        threshold = 3.0 if is_large_text else 4.5
        return ratio >= threshold, ratio

    @classmethod
    def meets_wcag_aaa(cls, fg: str, bg: str, is_large_text: bool = False) -> Tuple[bool, float]:
        ratio = cls.contrast_ratio(fg, bg)
        if ratio is None:
            return False, 0.0
        threshold = 4.5 if is_large_text else 7.0
        return ratio >= threshold, ratio


class CssAnalyzer:
    def __init__(self, css_content: str):
        self.raw_css = css_content
        # Remove comments
        self.clean_css = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    @classmethod
    def from_file(cls, filepath: str) -> 'CssAnalyzer':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return cls(f.read())

    def get_custom_properties(self, scope_selector: str = ':root') -> Dict[str, str]:
        """Extracts CSS custom properties within a specific scope selector."""
        props = {}
        # Find selector blocks
        pattern = re.escape(scope_selector) + r'\s*\{([^}]+)\}'
        for block in re.finditer(pattern, self.clean_css):
            body = block.group(1)
            for line in body.split(';'):
                if ':' in line:
                    parts = line.split(':', 1)
                    prop_name = parts[0].strip()
                    prop_val = parts[1].strip()
                    if prop_name.startswith('--'):
                        props[prop_name] = prop_val
        return props

    def find_rules(self, selector: str) -> List[str]:
        """Finds all rule block bodies for a given selector."""
        pattern = r'(?:^|\})\s*' + re.escape(selector) + r'\s*\{([^}]+)\}'
        matches = []
        for m in re.finditer(pattern, self.clean_css):
            matches.append(m.group(1).strip())
        return matches

    def contains_selector(self, selector: str) -> bool:
        pattern = r'(?:^|\})\s*([^{]+)\{'
        for m in re.finditer(pattern, self.clean_css):
            selectors = [s.strip() for s in m.group(1).split(',')]
            if selector in selectors:
                return True
        return False

    def get_media_queries(self) -> List[Tuple[str, str]]:
        """Returns list of (query_condition, body)"""
        results = []
        pattern = r'@media\s*([^{]+)\{([\s\S]+?\}\s*)\}'
        for m in re.finditer(r'@media\s*([^{]+)\{', self.clean_css):
            start = m.end()
            cond = m.group(1).strip()
            # bracket matching to get full media query body
            depth = 1
            idx = start
            while idx < len(self.clean_css) and depth > 0:
                if self.clean_css[idx] == '{':
                    depth += 1
                elif self.clean_css[idx] == '}':
                    depth -= 1
                idx += 1
            body = self.clean_css[start:idx-1]
            results.append((cond, body))
        return results


class AssetChecker:
    @staticmethod
    def file_exists(repo_root: str, rel_path: str) -> bool:
        full_path = os.path.join(repo_root, rel_path)
        return os.path.exists(full_path) and os.path.isfile(full_path)

    @staticmethod
    def get_file_size(repo_root: str, rel_path: str) -> int:
        full_path = os.path.join(repo_root, rel_path)
        if os.path.exists(full_path):
            return os.path.getsize(full_path)
        return 0

    @staticmethod
    def validate_svg_file(repo_root: str, rel_path: str) -> Tuple[bool, str]:
        full_path = os.path.join(repo_root, rel_path)
        if not os.path.exists(full_path):
            return False, f"File {rel_path} does not exist"
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            if not ('<svg' in content and '</svg>' in content):
                return False, "Does not contain valid <svg>...</svg> envelope"
            return True, "Valid SVG"
        except Exception as e:
            return False, str(e)
