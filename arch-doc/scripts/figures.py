#!/usr/bin/env python3
"""demo-doc figure helper.

  check <docs/figures>              Lint every figure SVG against references/diagrams.md.
  inline <page.html> <docs/figures> Replace <!-- figure: fig-NN-name.svg --> placeholders in the
                                    HTML with the SVG inlined (standalone <style> dropped, ids
                                    prefixed so figures don't collide). Writes the page in place.

Standard library only. Run with: python3 -I scripts/figures.py ...
"""
import os
import re
import sys
import xml.dom.minidom

REQUIRED = [
    (r'\sviewBox="0 0 \d+(\.\d+)? \d+(\.\d+)?"', 'viewBox="0 0 W H"'),
    (r'\srole="img"', 'role="img"'),
    (r'\saria-label="[^"]{20,}"', 'aria-label stating the claim (20+ chars)'),
    (r'stroke="currentColor"', 'stroke="currentColor" on the root'),
    (r'<filter id="rough"', 'the rough filter (hand-drawn look)'),
]
FORBIDDEN = [
    (r'<script', '<script>'),
    (r'<foreignObject', '<foreignObject>'),
    (r'<image\b', '<image> (draw it instead)'),
    (r'\shref="https?:', 'external href'),
    (r'#[0-9a-fA-F]{3,6}"', 'literal colour attribute (use currentColor / sk-* classes; literal hex only inside the standalone <style>)'),
]


def body_without_style(svg):
    return re.sub(r'<style[\s\S]*?</style>', '', svg)


def check(folder):
    files = sorted(f for f in os.listdir(folder) if f.endswith('.svg'))
    if not files:
        print(f'no .svg files in {folder}')
        return 1
    bad = 0
    expected = 1
    for f in files:
        path = os.path.join(folder, f)
        svg = open(path, encoding='utf-8').read()
        problems = []
        m = re.match(r'fig-(\d{2})-[a-z0-9-]+\.svg$', f)
        if not m:
            problems.append('name must be fig-NN-short-name.svg')
        elif int(m.group(1)) != expected:
            problems.append(f'numbering gap: expected fig-{expected:02d}')
        expected = int(m.group(1)) + 1 if m else expected + 1
        try:
            xml.dom.minidom.parseString(svg)
        except Exception as e:  # noqa: BLE001
            problems.append(f'not well-formed XML: {e}')
        for pat, what in REQUIRED:
            if not re.search(pat, svg):
                problems.append(f'missing {what}')
        for pat, what in FORBIDDEN:
            if re.search(pat, body_without_style(svg)):
                problems.append(f'contains {what}')
        texts = re.findall(r'<text[^>]*>([^<]*)</text>', svg)
        long = [t for t in texts if len(t) > 48]
        if long:
            problems.append(f'label too long (move it to the caption): "{long[0][:40]}…"')
        status = 'ok ' if not problems else 'FIX'
        print(f'{status} {f}' + ''.join(f'\n    - {p}' for p in problems))
        bad += bool(problems)
    return 1 if bad else 0


def inline_svg(svg, prefix):
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    svg = re.sub(r'<style[\s\S]*?</style>\s*', '', svg)
    for i in set(re.findall(r'\sid="([^"]+)"', svg)):
        svg = svg.replace(f'id="{i}"', f'id="{prefix}-{i}"')
        svg = svg.replace(f'url(#{i})', f'url(#{prefix}-{i})')
        svg = svg.replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    return svg.strip()


def inline(page, folder):
    html = open(page, encoding='utf-8').read()
    missing = []

    def repl(m):
        name = m.group(1).strip()
        path = os.path.join(folder, os.path.basename(name))
        if not os.path.exists(path):
            missing.append(name)
            return m.group(0)
        prefix = 'f' + re.sub(r'[^a-z0-9]', '', os.path.basename(name)[:-4].lower())
        return inline_svg(open(path, encoding='utf-8').read(), prefix)

    out = re.sub(r'<!--\s*figure:\s*([^>]+?)\s*-->', repl, html)
    open(page, 'w', encoding='utf-8').write(out)
    n = len(re.findall(r'<svg[^>]*class="sketch"', out))
    print(f'inlined figures: {n}' + (f'; missing: {", ".join(missing)}' if missing else ''))
    return 1 if missing else 0


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'check':
        sys.exit(check(sys.argv[2]))
    if len(sys.argv) == 4 and sys.argv[1] == 'inline':
        sys.exit(inline(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)
