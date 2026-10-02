from figstyle import plt, np, save, C

# 고속 스핀 에코(TSE): 90° 뒤 180° 펄스 열, 에코마다 다른 위상 부호화 줄을 채운다.
ETL, esp, T2 = 12, 10.0, 100.0          # 에코 수, 에코 간격(ms), 회백질 T2
# 선형 순서: 1번 에코가 −k_max, 12번 에코가 +k_max 띠를 채운다.
# 그러면 7번째 에코(TE 70 ms)가 k-공간 중심(k_y = 0 바로 위 띠)을 채운다.
order = list(range(ETL))
center_echo = 7

fig = plt.figure(figsize=(7.2, 3.0))
gsp = fig.add_gridspec(1, 2, width_ratios=[2.4, 1], wspace=0.35)
ax = fig.add_subplot(gsp[0])
te = esp * np.arange(1, ETL + 1)
cmap = plt.cm.viridis(np.linspace(0.05, 0.9, ETL))
ax.plot([0, 0], [0, 1.1], color=C["purple"], lw=2.5)
ax.text(0, 1.14, "90°", ha="center", fontsize=8)
for i in range(ETL):
    xp = esp / 2 + i * esp
    ax.plot([xp, xp], [0, 0.8], color=C["purple"], lw=1.6)
amp = np.exp(-te / T2)
ax.bar(te, amp, width=3.2, color=cmap, edgecolor="none")
tt = np.linspace(0, 130, 300)
ax.plot(tt, np.exp(-tt / T2), color=C["blue"], ls="--", lw=0.9)
ax.text(118, np.exp(-118 / T2) + 0.06, "$e^{-t/T_2}$", color=C["blue"], fontsize=8.5)
ax.annotate("유효 TE = 70 ms\n(k-공간 중심)", xy=(te[center_echo - 1], amp[center_echo - 1]),
            xytext=(78, 0.85), fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8),
            color=C["red"])
ax.text(30, 1.13, "보라 세로선: 180° 재초점 펄스", fontsize=8, color=C["purple"])
ax.set_xlim(-6, 132)
ax.set_ylim(0, 1.25)
ax.set_xlabel("90° 펄스 뒤 시간 (ms)")
ax.set_ylabel("에코 크기")
ax.set_title(f"(가) 에코 열: 에코 {ETL}개, 간격 {esp:.0f} ms", fontsize=9.5, loc="left")

ax2 = fig.add_subplot(gsp[1])
for echo_idx, band in enumerate(order):
    ax2.add_patch(plt.Rectangle((0, band), 1, 1, color=cmap[echo_idx]))
    ax2.text(0.5, band + 0.5, f"{echo_idx + 1}", ha="center", va="center",
             fontsize=7.5, color="white" if echo_idx < 8 else C["ink"])
ax2.set_xlim(0, 1)
ax2.set_ylim(0, ETL)
ax2.set_xticks([])
ax2.set_yticks([0, ETL / 2, ETL])
ax2.set_yticklabels(["$-k_{max}$", "0", "$+k_{max}$"])
ax2.axhline(ETL / 2, color=C["red"], lw=1.0)
ax2.set_title("(나) 에코 번호별 $k_y$ 띠", fontsize=9.5, loc="left")
ax2.spines["bottom"].set_visible(False)
save(fig, __file__)
