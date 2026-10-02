from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch

# 확산 MRI 분석 파이프라인의 순서. 위 줄은 전처리(8.1절), 아래 줄은 모형과 분석.
steps = [
    ("원자료 점검", "b값·b-벡터 표, 헤더,\n볼륨별 눈 점검", "8.1"),
    ("잡음 제거", "MP-PCA\n(다른 처리 전에)", "8.1"),
    ("깁스 제거", "경계 옆\n물결 무늬", "8.1"),
    ("왜곡 추정", "역위상 b = 0 쌍으로\n변위장 계산", "8.1"),
    ("맴돌이·움직임", "볼륨별 정합,\nb-벡터 회전,\n이상 슬라이스 대체", "8.1"),
    ("편향장·마스크·정합", "B1 편향 보정,\n뇌 마스크, T1 정합", "8.1"),
    ("모형 적합", "텐서(FA, MD)\nCSD(섬유 방향 분포)\nNODDI·DKI", "8.2, 8.4, 8.7"),
    ("분석", "TBSS·트랙 프로파일\n트랙토그래피·연결체", "8.3, 8.5, 8.6"),
]
fig, ax = plt.subplots(figsize=(7.3, 3.0))
ax.set_xlim(0, 4)
ax.set_ylim(-0.12, 2.0)
ax.axis("off")
w, h = 0.86, 0.78
pos = [(0.5 + k, 1.52) for k in range(4)] + [(3.5 - k, 0.42) for k in range(4)]
for k, ((t, sub, sec), (x, y)) in enumerate(zip(steps, pos)):
    col = C["blue"] if k < 6 else C["green"]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=C["light"] if k < 6 else "#e9f2e7", ec=col, lw=1.1))
    ax.text(x, y + 0.24, f"{k + 1}. {t}", ha="center", va="center", fontsize=8.8, color=C["ink"])
    ax.text(x, y - 0.07, sub, ha="center", va="center", fontsize=7.3, color=C["ink"], linespacing=1.25)
    ax.text(x + w / 2 - 0.02, y - h / 2 - 0.025, sec + "절", ha="right", va="top", fontsize=6.6,
            color=C["gray"])
arrow = dict(arrowstyle="-|>", color=C["gray"], lw=1.0, mutation_scale=9)
for k in range(3):
    ax.annotate("", xy=(pos[k + 1][0] - w / 2 - 0.01, 1.52), xytext=(pos[k][0] + w / 2 + 0.01, 1.52),
                arrowprops=arrow)
    ax.annotate("", xy=(pos[k + 5][0] + w / 2 + 0.01, 0.42), xytext=(pos[k + 4][0] - w / 2 - 0.01, 0.42),
                arrowprops=arrow)
ax.annotate("", xy=(3.5, 0.42 + h / 2 + 0.01), xytext=(3.5, 1.52 - h / 2 - 0.12), arrowprops=arrow)
save(fig, __file__)
