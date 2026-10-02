from figstyle import plt, np, save, C

# Ca²⁺ 문턱 모형(개념도): 약한 Ca²⁺ 상승 → 변화 없음, 중간 → LTD, 큰 상승 → LTP
ca = np.linspace(0, 10, 500)
th_d, th_p = 2.0, 5.0
dw = (-0.45 * np.exp(-((ca - 3.5) / 0.9) ** 2)
      + 1.0 / (1 + np.exp(-(ca - 6.6) / 0.55)))

fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.axhline(0, color=C["gray"], lw=0.7)
ax.axvspan(th_d, th_p, color=C["blue"], alpha=0.08, lw=0)
ax.axvspan(th_p, 10, color=C["red"], alpha=0.08, lw=0)
ax.plot(ca, dw * 100, color=C["ink"], lw=1.8)
ax.text(1.0, 12, "변화 없음", ha="center", fontsize=8.5, color=C["gray"])
ax.text(3.5, 12, "LTD", ha="center", fontsize=10, color=C["blue"])
ax.text(3.5, -62, "중간 크기로 길게\n→ 인산가수분해효소\n(칼시뉴린, PP1)\n→ AMPA 수용체 제거",
        ha="center", va="top", fontsize=7.8, color=C["blue"])
ax.text(8.2, 112, "LTP", ha="center", fontsize=10, color=C["red"])
ax.text(8.2, 62, "크고 빠르게\n→ CaMKII 등 인산화효소\n→ AMPA 수용체 삽입",
        ha="center", va="top", fontsize=7.8, color=C["red"])
ax.set_xticks([th_d, th_p])
ax.set_xticklabels(["LTD 문턱", "LTP 문턱"])
ax.set_xlabel("가시 안 Ca²⁺ 상승 크기 (개념적 눈금)")
ax.set_ylabel("시냅스 세기 변화 (%)")
ax.set_xlim(0, 10)
ax.set_ylim(-120, 130)
fig.tight_layout()
save(fig, __file__)
