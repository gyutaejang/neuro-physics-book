from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

# 소스 수준 연결성 분석의 단계 도식. 위 줄은 순문제와 역해를 준비하는 단계,
# 아래 줄은 영역 시계열을 만들고 연결성을 계산하는 단계다.
steps = [
    ("전처리한\n센서 데이터", "9장: 필터, ICA,\n나쁜 채널", C["gray"]),
    ("정합", "디지타이저·기준점\n→ 개인 MRI", C["blue"]),
    ("머리 모형과\n소스 공간", "BEM 3층, 피질 표면\n위 수천 개 점", C["blue"]),
    ("리드필드 L", "센서 × 소스\n(물리 2권 11장)", C["blue"]),
    ("역해 K", "MNE·dSPM·eLORETA\n또는 LCMV 빔형성", C["purple"]),
    ("영역 시계열", "아틀라스 ROI,\n부호 정렬·첫 PC", C["purple"]),
    ("누설 보정", "직교화 또는\n지연 0을 버리는 지표", C["red"]),
    ("연결성과 통계", "ImCoh·wPLI·AEC,\n순열 검정(6장)", C["red"]),
]
fig, ax = plt.subplots(figsize=(7.3, 3.0))
ax.set_xlim(0, 4)
ax.set_ylim(0, 2)
ax.axis("off")
w, h = 0.86, 0.5
pos = [(0.08 + i * 1.0, 1.32) for i in range(4)] + [(0.08 + (3 - i) * 1.0, 0.3) for i in range(4)]
for (x, y), (title, note, col) in zip(pos, steps):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="white", ec=col, lw=1.6))
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=8.6,
            color=C["ink"], linespacing=1.05)
    ax.text(x + w / 2, y - 0.04, note, ha="center", va="top", fontsize=7.0, color=C["gray"],
            linespacing=1.1)
arrow = dict(arrowstyle="-|>", color=C["ink"], lw=1.0, mutation_scale=10)
for i in range(3):
    x, y = pos[i]
    ax.annotate("", xy=(x + 1.0, y + h / 2), xytext=(x + w, y + h / 2), arrowprops=arrow)
for i in range(4, 7):
    x, y = pos[i]
    ax.annotate("", xy=(x - 1.0 + w, y + h / 2), xytext=(x, y + h / 2), arrowprops=arrow)
x3, y3 = pos[3]
ax.annotate("", xy=(x3 + w / 2 + 0.25, pos[4][1] + h), xytext=(x3 + w / 2 + 0.25, y3 - 0.33),
            arrowprops=arrow)
ax.text(0.02, 1.97, "순문제 준비", fontsize=8.5, color=C["blue"], va="top")
ax.text(0.02, 0.98, "역문제와 연결성", fontsize=8.5, color=C["purple"], va="top")
save(fig, __file__)
