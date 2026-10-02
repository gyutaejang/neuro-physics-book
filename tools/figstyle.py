"""그림 스크립트 공통 스타일.

각 그림 스크립트는 다음처럼 쓴다.

    from figstyle import plt, np, C, save
    fig, ax = plt.subplots(figsize=(6, 3))
    ...
    save(fig, __file__)

save()는 스크립트 이름과 같은 이름의 SVG를 build/figures/<책>/ 아래에 쓴다.
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# 한글 글꼴. Noto Sans CJK KR이 없으면 나눔고딕으로 대체한다.
plt.rcParams.update({
    "font.family": ["Noto Sans CJK KR", "NanumGothic", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "mathtext.fontset": "dejavusans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.8,
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "legend.frameon": False,
    "svg.fonttype": "path",
    "figure.dpi": 100,
})

# 책 전체에서 같은 의미에는 같은 색을 쓴다.
C = {
    "blue": "#2563a8",     # 주 데이터, 전기장, 양의 값
    "red": "#c2410c",      # 강조, 힘, 음의 값과 대비
    "green": "#3f7f3a",    # 생물학, 이온, 세포
    "purple": "#6d4c9f",   # 자기장, 스핀
    "gray": "#7a7a7a",     # 보조선, 축, 참고
    "light": "#e8eef6",    # 배경 채움
    "ink": "#222222",      # 글자
}


def save(fig, script_path):
    """스크립트 경로를 받아 build/figures/<책>/<이름>.svg로 저장한다."""
    script_path = os.path.abspath(script_path)
    fig_dir = os.path.dirname(script_path)
    book = os.path.basename(os.path.dirname(fig_dir))
    root = os.path.dirname(os.path.dirname(os.path.dirname(fig_dir)))
    out_dir = os.path.join(root, "build", "figures", book)
    os.makedirs(out_dir, exist_ok=True)
    name = os.path.splitext(os.path.basename(script_path))[0]
    out = os.path.join(out_dir, name + ".svg")
    fig.savefig(out, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    print("  wrote", os.path.relpath(out, root), file=sys.stderr)


def log_scale_map(items, xlabel, xlim, figsize=(7, 3.2), color=None, ticks=None):
    """로그 눈금 위에 (값, 이름) 점을 찍는 '크기 지도'.

    items: [(값, "이름"), ...]. 이름이 겹치지 않도록 위아래로 번갈아 단다.
    ticks: [(값, "눈금 글자"), ...]를 주면 그 눈금을 쓴다.
    """
    color = color or C["blue"]
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xscale("log")
    ax.set_xlim(*xlim)
    ax.set_ylim(-1.6, 1.6)
    ax.axhline(0, color=C["gray"], lw=1.2, zorder=1)
    for i, (v, name) in enumerate(sorted(items)):
        up = 1 if i % 2 == 0 else -1
        lvl = up * (0.55 + 0.45 * ((i // 2) % 2))
        ax.plot([v, v], [0, lvl * 0.82], color=C["gray"], lw=0.6, zorder=1)
        ax.scatter([v], [0], s=28, color=color, zorder=3)
        ax.text(v, lvl, name, ha="center", va="bottom" if up > 0 else "top",
                fontsize=8.5, color=C["ink"])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_position(("data", -1.6))
    if ticks:
        ax.set_xticks([t for t, _ in ticks])
        ax.set_xticklabels([s for _, s in ticks])
        ax.minorticks_off()
    ax.set_xlabel(xlabel)
    return fig, ax
