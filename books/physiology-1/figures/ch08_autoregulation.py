from figstyle import plt, np, save, C

MAP = np.linspace(20, 200, 600)


def curve(p, lo, hi, base=50.0, k=0.35):
    """평탄부 [lo, hi]에서 base, 아래로는 압력에 비례해 줄고 위로는 비례해 는다 (모서리를 부드럽게)."""
    below = base * p / lo
    above = base * p / hi
    f = -np.log(np.exp(-k * below) + np.exp(-k * base)) / k      # 부드러운 최솟값
    return np.log(np.exp(k * f) + np.exp(k * above)) / k        # 부드러운 최댓값


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3))
n = curve(MAP, 60, 150)
h = curve(MAP, 85, 180)
a1.axvspan(60, 150, color=C["light"], zorder=0)
a1.plot(MAP, n, color=C["blue"], lw=1.9, label="정상 혈압인 사람")
a1.plot(MAP, h, color=C["red"], lw=1.6, ls="--", label="만성 고혈압 (오른쪽 이동)")
a1.text(105, 53.5, "자동 조절 평탄부\n약 60–150 mmHg", ha="center", va="bottom", fontsize=8, color=C["blue"])
a1.text(26, 3, "압력 수동\n(혈관 최대 확장)", fontsize=7.5, color=C["gray"], ha="left", va="bottom")
a1.text(160, 74, "돌파\n(과관류)", fontsize=7.5, color=C["gray"], ha="left")
a1.axhline(20, color=C["gray"], lw=0.6, ls=":")
a1.text(198, 21, "기능 정지 문턱 약 20", fontsize=7, color=C["gray"], ha="right", va="bottom")
a1.set_xlabel("평균 동맥압 (mmHg)")
a1.set_ylabel("뇌혈류 (mL/100 g/분)")
a1.set_title("자동 조절 곡선 (개념도)")
a1.set_xlim(20, 200)
a1.set_ylim(0, 85)
a1.legend(fontsize=7.5, loc="upper left")

# 오른쪽: 혈류를 지키는 데 필요한 혈관 반지름 (푸아죄유, 저항 ∝ r^-4)
p = np.linspace(60, 150, 200)
r = (90 / p) ** 0.25
a2.plot(p, r * 100, color=C["blue"], lw=1.9)
for pp in (60, 90, 150):
    rr = (90 / pp) ** 0.25 * 100
    a2.scatter([pp], [rr], color=C["red"], s=22, zorder=3)
    a2.annotate(f"{rr:.0f} %", xy=(pp, rr), xytext=(pp + (4 if pp < 150 else -3), rr + (1.5 if pp < 150 else -2.5)),
                fontsize=8, ha="left" if pp < 150 else "right")
a2.axhline(100, color=C["gray"], lw=0.6, ls=":")
a2.set_xlabel("평균 동맥압 (mmHg)")
a2.set_ylabel("필요한 저항 혈관 반지름 (%)")
a2.set_title("반지름 ±10 %로 혈류를 지킨다")
a2.set_xlim(55, 155)
a2.set_ylim(85, 115)
a2.text(150, 112, "기준: 90 mmHg = 100 %\n저항 ∝ 1/r⁴", ha="right", va="top", fontsize=7.8, color=C["gray"])
fig.tight_layout()
save(fig, __file__)
