from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.5), gridspec_kw=dict(width_ratios=[1, 1.15]))

bands = [(35, 80, "#e8eef6", "정상 기능\n(회백질 약 60–80, 평균 약 50)"),
         (20, 35, "#f6ecd9", "혈류 감소(올리게미아)\nOEF가 올라 보상, 기능 유지"),
         (10, 20, "#f6dccb", "반음영: 전기 활동 정지\nEEG·유발전위 소실, 세포는 생존"),
         (0, 10, "#eec1a8", "핵심 경색: 이온 펌프 실패\n무산소 탈분극, K⁺ 유출, Ca²⁺ 유입")]
for lo, hi, col, lab in bands:
    a1.axhspan(lo, hi, xmin=0, xmax=0.18, color=col, ec=C["gray"], lw=0.5)
    a1.text(0.22, (lo + hi) / 2, lab, va="center", fontsize=7.6, transform=a1.get_yaxis_transform())
for y in (10, 20, 35):
    a1.axhline(y, xmax=0.18, color=C["gray"], lw=0.6)
a1.set_ylim(0, 80)
a1.set_xlim(0, 1)
a1.set_xticks([])
a1.spines["bottom"].set_visible(False)
a1.set_yticks([0, 10, 20, 35, 50, 80])
a1.set_ylabel("뇌혈류 (mL/100 g/분)")
a1.set_title("혈류 문턱 (대략값)", fontsize=10)

# 오른쪽: 문턱은 시간에 따라 오른다 (개념도)
tm = np.logspace(np.log10(5), np.log10(1000), 300)
thr = 18 * (1 - np.exp(-tm / 160))
a2.fill_between(tm, 0, thr, color="#eec1a8", alpha=0.8, lw=0)
a2.fill_between(tm, thr, 20, color="#f6dccb", alpha=0.8, lw=0)
a2.plot(tm, thr, color=C["red"], lw=1.8)
a2.axhline(20, color=C["gray"], lw=0.8, ls="--")
a2.text(6, 21, "기능 정지 문턱 약 20", fontsize=7.5, color=C["gray"], va="bottom")
a2.text(450, 6, "경색", fontsize=9, color=C["red"], ha="center")
a2.text(18, 14.5, "회복 가능\n(반음영)", fontsize=8.5, color=C["ink"], ha="center")
a2.annotate("2–3시간이면\n약 10–12에서 경색", xy=(150, 18 * (1 - np.exp(-150 / 160))), xytext=(7, 8.5),
            fontsize=7.5, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xscale("log")
a2.set_xlim(5, 1000)
a2.set_ylim(0, 30)
a2.set_xticks([10, 30, 60, 180, 600])
a2.set_xticklabels(["10분", "30분", "1시간", "3시간", "10시간"])
a2.minorticks_off()
a2.set_xlabel("허혈 지속 시간")
a2.set_ylabel("뇌혈류 (mL/100 g/분)")
a2.set_title("경색 문턱은 시간이 갈수록 오른다 (개념도)", fontsize=10)
fig.tight_layout()
save(fig, __file__)
