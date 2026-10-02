from figstyle import plt, np, save, C

# MEGA-PRESS 모의 스펙트럼 (3 T, 127.7 MHz, TE = 68 ms ≈ 1/(2J)).
f0 = 127.7          # MHz → 1 ppm = 127.7 Hz
J = 7.3             # GABA C4–C3 결합 상수 (Hz)
lw = 6.0            # 선폭 (Hz)
ppm = np.linspace(1.5, 4.2, 3000)
hz = ppm * f0


def lor(center_ppm, amp, width=lw):
    x = (hz - center_ppm * f0) / (width / 2)
    return amp / (1 + x ** 2)


def triplet(center, amp, outer_sign):
    # 1:2:1 세겹선. outer_sign = −1이면 바깥 두 선이 뒤집힌다 (TE = 1/(2J)).
    return (lor(center, amp * 0.5) + outer_sign * (lor(center - J / f0, amp * 0.25) + lor(center + J / f0, amp * 0.25)))


# 농도 × 수소 수 (상대 단위). 크레아틴 8 mM × 3H = 24, GABA 1 mM × 2H = 2.
base = (lor(2.01, 30) + lor(3.03, 24) + lor(3.92, 16) + lor(3.21, 13)
        + lor(3.56, 6, 14) + lor(2.35, 5, 18) + lor(2.1, 4, 20) + lor(3.75, 5, 14)
        + lor(2.28, 1.2, 12))
gaba_c3 = lor(1.89, 1.6, 14)
off = base + gaba_c3 + triplet(3.01, 2, -1)
# ON: 1.9 ppm 편집 펄스. GABA C4의 결합 진화가 되돌려져 바깥 선이 바로 서고,
# C3(1.89)과 근처 NAA(2.01) 일부가 펄스에 맞는다. Glx 3.75도 함께 편집된다.
on = (base - lor(2.01, 4) + lor(3.75, 1.5, 12)) + 0.0 * gaba_c3 + triplet(3.01, 2, +1)
diff = on - off

fig = plt.figure(figsize=(7.4, 3.1))
gs = fig.add_gridspec(1, 3, width_ratios=[0.75, 1.3, 1.3], wspace=0.32)

# (가) GABA 3.0 ppm 세겹선의 선 하나하나
a0 = fig.add_subplot(gs[0])
xs = np.array([-J, 0, J])
for k, (lab, h, col) in enumerate([("OFF", [-0.5, 1, -0.5], C["gray"]),
                                   ("ON", [0.5, 1, 0.5], C["blue"]),
                                   ("차이", [1, 0, 1], C["red"])]):
    y0 = -k * 2.0
    a0.axhline(y0, color=C["gray"], lw=0.5)
    a0.vlines(xs, y0, y0 + np.array(h), color=col, lw=2.2)
    a0.text(-17, y0 + 0.35, lab, fontsize=8.5, color=col, ha="left")
a0.set_xlim(-18, 13)
a0.set_ylim(-5, 1.3)
a0.set_yticks([])
a0.spines["left"].set_visible(False)
a0.set_xlabel("3.01 ppm 기준 (Hz)", fontsize=8.5)
a0.set_xticks([-7.3, 0, 7.3])
a0.set_xticklabels(["−J", "0", "+J"])
a0.set_title("(가) GABA 세겹선", fontsize=9.5)

# (나) OFF와 ON 스펙트럼
a1 = fig.add_subplot(gs[1])
a1.axvspan(1.9 - 0.35, 1.9 + 0.35, color=C["light"], zorder=0)
a1.text(1.72, 20, "편집\n펄스\n(ON)", fontsize=8, ha="center", color=C["blue"])
a1.plot(ppm, off, color=C["gray"], lw=1.2, label="OFF")
a1.plot(ppm, on, color=C["blue"], lw=0.9, label="ON")
for p, lab, y in [(2.01, "NAA", 31), (3.03, "Cr", 25.5), (3.21, "Cho", 14.5), (3.92, "Cr", 17.5)]:
    a1.text(p, y, lab, fontsize=8, ha="center")
a1.set_xlim(4.2, 1.5)
a1.set_ylim(-2, 41)
a1.set_yticks([])
a1.set_xlabel("화학적 이동 (ppm)")
a1.legend(fontsize=8, loc="upper left")
a1.set_title("(나) 두 스펙트럼은 거의 같다", fontsize=9.5)

# (다) 차이 스펙트럼
a2 = fig.add_subplot(gs[2])
a2.axhline(0, color=C["gray"], lw=0.5)
a2.plot(ppm, diff, color=C["red"], lw=1.3)
a2.text(3.01, 1.3, "GABA+\n3.0 ppm", fontsize=8, ha="center", color=C["red"])
a2.text(3.75, 1.75, "Glx\n3.75", fontsize=8, ha="center")
a2.text(1.93, -3.2, "NAA 일부\n(펄스에 맞음)", fontsize=8, ha="left", va="center")
a2.text(3.03, -1.0, "Cr, Cho는 지워진다", fontsize=8, ha="center", color=C["gray"])
a2.set_xlim(4.2, 1.5)
a2.set_ylim(-4.6, 2.8)
a2.set_yticks([])
a2.set_xlabel("화학적 이동 (ppm)")
a2.set_title("(다) ON − OFF (세로 확대)", fontsize=9.5)
a2.spines["left"].set_visible(False)
a1.spines["left"].set_visible(False)
save(fig, __file__)
