#!/usr/bin/env python3
"""책 한 권을 Markdown에서 PDF로 빌드한다.

    python3 tools/build.py physics-1            # build/physics-1.html, dist/physics-1.pdf
    python3 tools/build.py physics-1 --preview  # 위 + build/preview/ 에 페이지 PNG

순서: 그림 스크립트 실행 → 장별 Markdown 변환 → 그림·참조 번호 매기기
→ 표지·차례와 합쳐 HTML 한 장 → Chromium으로 PDF 인쇄.
"""
import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
CHROMIUM = "/opt/pw-browsers/chromium"


def run_figures(book, build_dir, only=None):
    """figures/*.py를 실행해 SVG를 만들고, 손으로 그린 *.svg는 복사한다."""
    src = os.path.join(ROOT, "books", book, "figures")
    out = os.path.join(build_dir, "figures", book)
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, PYTHONPATH=TOOLS)
    failed = []
    for script in sorted(glob.glob(os.path.join(src, f"ch{only}_*.py" if only else "*.py"))):
        name = os.path.splitext(os.path.basename(script))[0]
        target = os.path.join(out, name + ".svg")
        if os.path.exists(target) and os.path.getmtime(target) > max(
                os.path.getmtime(script), os.path.getmtime(os.path.join(TOOLS, "figstyle.py"))):
            continue
        r = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(name)
            print(f"[그림 실패] {name}\n{r.stderr}", file=sys.stderr)
        else:
            sys.stderr.write(r.stderr)
    for svg in glob.glob(os.path.join(src, "*.svg")):
        shutil.copy(svg, out)
    return failed


def md_to_html(text):
    md = markdown.Markdown(extensions=[
        "extra", "admonition", "sane_lists", "toc",
        "pymdownx.arithmatex",
    ], extension_configs={
        "pymdownx.arithmatex": {"generic": True},
        "toc": {"permalink": False, "slugify": lambda s, sep: re.sub(r"\W+", "-", s).strip("-").lower()},
    })
    return md.convert(text)


FIG_RE = re.compile(r'<p>\s*<img alt="([^"]*)" src="figures/([^"]+)"\s*/?>\s*</p>')


def number_figures(body, chap_no, book, fig_index):
    """<img>를 번호 붙은 <figure>로 바꾸고, 그림 이름 → 번호 표를 채운다."""
    count = 0

    def repl(m):
        nonlocal count
        count += 1
        alt, src = m.group(1), m.group(2)
        key = os.path.splitext(os.path.basename(src))[0]
        label = f"{chap_no}.{count}" if chap_no else f"{count}"
        fig_index[key] = label
        return (f'<figure id="fig-{key}"><img src="figures/{book}/{src}" alt="">'
                f'<figcaption><b>그림 {label}</b> {alt}</figcaption></figure>')

    return FIG_RE.sub(repl, body)


def resolve_refs(body, fig_index, problems):
    def repl(m):
        key = m.group(1)
        if key not in fig_index:
            problems.append(f"없는 그림 참조: @fig:{key}")
            return f'<span class="badref">그림 ??({key})</span>'
        return f'<a class="ref" href="#fig-{key}">그림 {fig_index[key]}</a>'

    return re.sub(r"@fig:([A-Za-z0-9_\-]+)", repl, body)


def build_toc(chapters):
    items = []
    for ch in chapters:
        items.append(f'<li class="toc-ch"><a href="#{ch["id"]}">{ch["title"]}</a>')
        if ch["sections"]:
            items.append("<ul>")
            for sid, st in ch["sections"]:
                if ch["numbered"] and not re.match(r"\d", st):
                    continue  # 핵심 정리, 확인 문제 같은 장 끝 절은 차례에서 뺀다
                items.append(f'<li><a href="#{sid}">{st}</a></li>')
            items.append("</ul>")
        items.append("</li>")
    return '<nav class="toc"><h1 class="toc-title">차례</h1><ul>' + "".join(items) + "</ul></nav>"


def build(book, preview=False, only=None):
    meta = json.load(open(os.path.join(ROOT, "books", book, "book.json"), encoding="utf-8"))
    build_dir = os.path.join(ROOT, "build")
    os.makedirs(build_dir, exist_ok=True)
    failed = run_figures(book, build_dir, only)

    problems = [f"그림 스크립트 실패: {f}" for f in failed]
    fig_index = {}
    chapters = []
    names = meta["chapters"]
    if only:
        names = [n for n in names if n.startswith(only + "-")]
        if not names:
            sys.exit(f"{only}로 시작하는 장이 없다")
    tag = f"{book}-ch{only}" if only else book
    for fname in names:
        path = os.path.join(ROOT, "books", book, "chapters", fname)
        if not os.path.exists(path):
            problems.append(f"원고 없음: {fname}")
            continue
        text = open(path, encoding="utf-8").read()
        m = re.match(r"(\d+)-", fname)
        chap_no = int(m.group(1)) if m and int(m.group(1)) > 0 else None
        body = md_to_html(text)
        body = number_figures(body, chap_no, book, fig_index)
        h1 = re.search(r'<h1 id="([^"]+)">(.*?)</h1>', body)
        sections = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
        chapters.append({"id": h1.group(1) if h1 else fname, "title": h1.group(2) if h1 else fname,
                         "sections": sections, "body": body, "file": fname,
                         "numbered": chap_no is not None})
        for src in re.findall(r'src="figures/[^/]+/([^"]+)"', body):
            if not os.path.exists(os.path.join(build_dir, "figures", book, src)):
                problems.append(f"{fname}: 그림 파일 없음 {src}")

    for ch in chapters:
        ch["body"] = resolve_refs(ch["body"], fig_index, problems)

    katex = os.path.join(TOOLS, "node_modules", "katex", "dist")
    if not os.path.exists(katex):
        subprocess.run(["npm", "install", "--silent"], cwd=TOOLS, check=True)

    cover = f"""<section class="cover">
  <div class="series">{html.escape(meta.get("series", ""))}</div>
  <h1 class="cover-title">{html.escape(meta["title"])}</h1>
  <div class="cover-sub">{html.escape(meta.get("subtitle", ""))}</div>
  <div class="cover-note">{html.escape(meta.get("audience", ""))}</div>
  <div class="cover-ver">{html.escape(meta.get("version", ""))}</div>
</section>"""
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<title>{html.escape(meta["title"])}</title>
<link rel="stylesheet" href="file://{katex}/katex.min.css">
<link rel="stylesheet" href="file://{TOOLS}/style.css">
<script src="file://{katex}/katex.min.js"></script>
<script src="file://{katex}/contrib/auto-render.min.js"></script>
</head><body>
{cover}
{build_toc(chapters)}
{"".join(f'<article class="chapter">{c["body"]}</article>' for c in chapters)}
<script>
document.querySelectorAll('.arithmatex').forEach(el => {{
  const t = el.textContent.trim();
  const display = t.startsWith('\\\\[');
  const src = t.replace(/^\\\\[\\[(]/, '').replace(/\\\\[\\])]$/, '');
  try {{ katex.render(src, el, {{displayMode: display, throwOnError: true, strict: false}}); }}
  catch (e) {{ el.classList.add('matherr'); el.title = e.message; window.__matherr = (window.__matherr||[]).concat([e.message + ' :: ' + src]); }}
}});
window.__ready = true;
</script>
</body></html>"""
    html_path = os.path.join(build_dir, f"{tag}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(doc)

    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    # --only 빌드는 확인용이므로 dist/가 아니라 build/에 쓴다.
    pdf_path = os.path.join(build_dir if only else os.path.join(ROOT, "dist"), f"{tag}.pdf")
    footer = ('<div style="width:100%;font-size:8pt;color:#888;text-align:center;'
              'font-family:Noto Sans CJK KR">'
              f'{html.escape(meta["title"])} · <span class="pageNumber"></span></div>')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM if os.path.exists(CHROMIUM) else None)
        page = browser.new_page()
        page.goto("file://" + html_path)
        page.wait_for_function("window.__ready === true")
        page.evaluate("document.fonts.ready.then(() => true)")
        for e in page.evaluate("window.__matherr || []"):
            problems.append("수식 오류: " + e)
        page.pdf(path=pdf_path, format="A4", print_background=True,
                 display_header_footer=True, header_template="<div></div>", footer_template=footer,
                 margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
                 outline=True, tagged=True)
        browser.close()

    pages = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
    npages = re.search(r"Pages:\s+(\d+)", pages)
    print(f"PDF: {os.path.relpath(pdf_path, ROOT)} ({npages.group(1) if npages else '?'}쪽)")

    if preview:
        pdir = os.path.join(build_dir, "preview", tag)
        shutil.rmtree(pdir, ignore_errors=True)
        os.makedirs(pdir)
        subprocess.run(["pdftoppm", "-png", "-r", "60", pdf_path, os.path.join(pdir, "p")], check=True)
        print(f"미리보기: {os.path.relpath(pdir, ROOT)}/")

    if problems:
        print("\n문제 발견:", *problems, sep="\n  - ")
        return 1
    print("문제 없음")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("book")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--only", metavar="NN", help="이 번호의 장 하나만 build/에 빌드한다 (예: 06)")
    a = ap.parse_args()
    sys.exit(build(a.book, a.preview, a.only))
