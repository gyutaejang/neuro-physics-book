from matplotlib.patches import Rectangle

from figstyle import plt, np, save, C

# 층별 fMRI 도식: 피질 깊이에 따른 신경 활동과 GE-BOLD.
# 깊은 층의 탈산소Hb가 상행 정맥을 타고 표면 쪽으로 흘러가 표면 쪽 신호가 부풀려진다.
d = np.linspace(0, 2.5, 501)  # 연질막(0)에서 백질 경계(2.5 mm)까지
neural = np.exp(-0.5 * ((d - 1.2) / 0.22) ** 2)
dd = d[1] - d[0]
drain = np.array([neural[i:].sum() * dd for i in range(len(d))])  # 더 깊은 곳에서 올라온 몫
ge = neural + 5.0 * drain + 1.0 * np.exp(-d / 0.12) * drain[0]
ge = ge / ge.max()
spec = np.convolve(neural, np.ones(90) / 90, mode="same")
spec = spec / spec.max()

fig, (a0, a1) = plt.subplots(1, 2, figsize=(7.0, 3.4), gridspec_kw=dict(width_ratios=[0.8, 1.4]))
# 왼쪽: 피질 단면과 상행 정맥
a0.set_xlim(0, 3)
a0.set_ylim(2.75, -0.45)
a0.axis("off")
a0.add_patch(Rectangle((0, 0), 3, 2.5, fc="#f1f4ee", ec="none"))
bd = [0, 0.25, 0.95, 1.45, 1.95, 2.5]
for y0, y1, nm in zip(bd[:-1], bd[1:], ["1", "2/3", "4", "5", "6"]):
    a0.axhline(y0, color=C["gray"], lw=0.4)
    a0.text(0.08, (y0 + y1) / 2, nm, fontsize=7.5, color=C["gray"], va="center")
a0.add_patch(Rectangle((0.25, -0.35), 2.6, 0.3, fc="#ddd3ec", ec=C["purple"], lw=1))
a0.text(1.55, -0.2, "연질막 정맥", ha="center", va="center", fontsize=7.5, color=C["purple"])
a0.add_patch(Rectangle((1.9, -0.05), 0.16, 2.35, fc="#ddd3ec", ec=C["purple"], lw=0.8))
for y in (2.1, 1.6, 1.1, 0.6):
    a0.annotate("", xy=(1.98, y - 0.35), xytext=(1.98, y),
                arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=0.8, mutation_scale=7))
for y in (1.0, 1.2, 1.4):
    a0.annotate("", xy=(1.88, y), xytext=(1.0, y),
                arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.6, mutation_scale=6))
a0.add_patch(plt.Circle((0.75, 1.2), 0.2, color=C["green"], alpha=0.6))
a0.text(0.75, 1.6, "활성\n(4층)", fontsize=7.5, ha="center", va="top", color=C["green"])
a0.text(2.15, 0.6, "상행\n정맥", fontsize=7.5, color=C["purple"], va="center")
a0.text(1.5, 2.66, "백질", ha="center", fontsize=7.5, color=C["gray"])

# 오른쪽: 깊이 프로파일
a1.plot(neural, d, color=C["green"], lw=2, label="실제 신경 활동")
a1.plot(ge, d, color=C["blue"], lw=2, label="GE-BOLD (배출 정맥 효과)")
a1.plot(spec, d, color=C["red"], lw=1.4, ls="--", label="정맥에 덜 민감한 방법\n(VASO, 스핀 에코 등)")
a1.set_ylim(2.5, 0)
a1.set_xlim(0, 1.08)
a1.set_ylabel("피질 깊이 (mm, 0 = 표면)")
a1.set_xlabel("정규화한 신호")
a1.legend(fontsize=7.6, loc="lower right")
a1.set_title("깊이에 따른 반응 (도식)", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
