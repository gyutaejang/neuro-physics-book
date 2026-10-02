from figstyle import plt, np, save, C

periods = [2, 3, 4, 5]
data = [
    ("14족: CH$_4$, SiH$_4$, GeH$_4$, SnH$_4$", [-161.5, -111.9, -88.5, -52.0], C["gray"], "s", ["CH$_4$", "SiH$_4$", "GeH$_4$", "SnH$_4$"]),
    ("15족: NH$_3$ …", [-33.3, -87.7, -62.5, -17.0], C["green"], "^", ["NH$_3$", "PH$_3$", "AsH$_3$", "SbH$_3$"]),
    ("17족: HF …", [19.5, -85.1, -66.8, -35.4], C["purple"], "D", ["HF", "HCl", "HBr", "HI"]),
    ("16족: H$_2$O, H$_2$S, H$_2$Se, H$_2$Te", [100.0, -60.3, -41.3, -2.2], C["blue"], "o", ["H$_2$O", "H$_2$S", "H$_2$Se", "H$_2$Te"]),
]
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for lab, bp, col, mk, names in data:
    ax.plot(periods, bp, color=col, marker=mk, lw=1.4, ms=5)
    off = {"H$_2$O": (8, -2), "HF": (8, -2), "NH$_3$": (8, 2), "CH$_4$": (8, -4)}
    n0 = names[0]
    ax.annotate(n0, xy=(2, bp[0]), xytext=off.get(n0, (8, 0)), textcoords="offset points",
                fontsize=8.5, color=col, va="center")
    ax.annotate(names[-1], xy=(5, bp[-1]), xytext=(7, 0), textcoords="offset points",
                fontsize=8.5, color=col, va="center")
# 수소 결합이 없었다면 물이 놓였을 자리
ax.plot([2, 3], [-90, -60.3], color=C["blue"], ls=":", lw=1.2)
ax.scatter([2], [-90], facecolor="white", edgecolor=C["blue"], s=30, zorder=4)
ax.annotate("수소 결합이 없다면\n약 −90 °C쯤 (추정)", xy=(2, -90), xytext=(3.05, -152), fontsize=8.5, va="center",
            color=C["blue"], arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
ax.annotate("", xy=(1.9, 98), xytext=(1.9, -86), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.2))
ax.text(1.83, 6, "약 190 °C", color=C["red"], fontsize=8.5, ha="right", va="center", rotation=90)
ax.axhline(37, color=C["gray"], lw=0.6, ls="--")
ax.text(5.55, 41, "체온 37 °C", fontsize=8, color=C["gray"], ha="right", va="bottom")
ax.set_xticks(periods)
ax.set_xticklabels(["2주기", "3주기", "4주기", "5주기"])
ax.set_xlim(1.6, 5.6)
ax.set_ylim(-175, 120)
ax.set_yticks([-150, -100, -50, 0, 50, 100])
ax.set_yticklabels(["−150", "−100", "−50", "0", "50", "100"])
ax.set_ylabel("끓는점 (°C, 1기압)")
fig.tight_layout()
save(fig, __file__)
