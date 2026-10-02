from matplotlib.patches import FancyBboxPatch
from figstyle import plt, np, save, C

# 2-조직 구획 모형과 시간-방사능 곡선 (라클로프라이드 비슷한 가역 추적자, 붕괴 보정된 값)
dt = 0.005
t = np.arange(0, 90 + dt, dt)
A1, A2, A3, l1, l2, l3 = 851.1, 21.88, 20.81, 4.134, 0.1191, 0.01043   # 펑(Feng) 형태 입력 함수
Cp = np.maximum((A1 * t - A2 - A3) * np.exp(-l1 * t) + A2 * np.exp(-l2 * t) + A3 * np.exp(-l3 * t), 0)


def tcm(K1, k2, k3, k4):
    a, b = np.zeros_like(t), np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (K1 * Cp[i - 1] - (k2 + k3) * a[i - 1] + k4 * b[i - 1])
        b[i] = b[i - 1] + dt * (k3 * a[i - 1] - k4 * b[i - 1])
    return a, b


nd, sp = tcm(0.1, 0.4, 0.24, 0.08)
ref, _ = tcm(0.1, 0.4, 0.0, 0.0)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2), gridspec_kw=dict(width_ratios=[1, 1.15]))
# (가) 구획 도식
boxes = {"P": (0.02, 0.55, "혈장\n$C_P$", C["gray"]), "ND": (0.38, 0.55, "유리 + 비특이\n$C_{ND}$", C["green"]),
         "S": (0.74, 0.55, "특이 결합\n$C_S$", C["blue"])}
for k, (x0, y0, lab, col) in boxes.items():
    a1.add_patch(FancyBboxPatch((x0, y0), 0.24, 0.26, boxstyle="round,pad=0.01", facecolor="white",
                                edgecolor=col, lw=1.5))
    a1.text(x0 + 0.12, y0 + 0.13, lab, ha="center", va="center", fontsize=8)


def arrow(x0, x1, y, lab, above=True):
    a1.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1))
    a1.text((x0 + x1) / 2, y + (0.035 if above else -0.035), lab, ha="center",
            va="bottom" if above else "top", fontsize=8.5)


arrow(0.265, 0.375, 0.73, "$K_1$")
arrow(0.375, 0.265, 0.63, "$k_2$", above=False)
arrow(0.625, 0.735, 0.73, "$k_3$")
arrow(0.735, 0.625, 0.63, "$k_4$", above=False)
a1.add_patch(plt.Rectangle((0.34, 0.47), 0.68, 0.42, fill=False, ls="--", ec=C["gray"], lw=0.8))
a1.text(0.68, 0.43, "PET가 보는 것: 두 칸의 합 $C_T$", ha="center", va="top", fontsize=8, color=C["gray"])
a1.text(0.0, 0.25, "참조 영역(예: 소뇌)에는 특이 결합 칸이 없다.\n"
        "$V_{ND} = K_1/k_2$,  $BP_{ND} = k_3/k_4$\n"
        "$V_T = V_{ND}\\,(1 + BP_{ND})$", fontsize=8, va="top", linespacing=1.6)
a1.set_xlim(0, 1.04)
a1.set_ylim(0, 0.95)
a1.axis("off")
a1.set_title("(가) 2-조직 구획 모형", fontsize=9.5)

# (나) 곡선
a2.plot(t, Cp, color=C["gray"], lw=1.2, label="혈장 $C_P$ (대사물 보정)")
a2.plot(t, nd + sp, color=C["blue"], lw=2, label="목표 영역 $C_T$ (선조체)")
a2.plot(t, sp, color=C["blue"], lw=1, ls="--", label="그중 특이 결합 $C_S$")
a2.plot(t, ref, color=C["green"], lw=1.8, label="참조 영역 (소뇌)")
a2.set_xlim(0, 90)
a2.set_ylim(0, 40)
a2.set_xlabel("주사 뒤 시간 (분)")
a2.set_ylabel("방사능 농도 (상대 단위)")
a2.annotate(f"혈장 정점 약 {Cp.max():.0f}", xy=(t[Cp.argmax()] + 0.6, 39.5), xytext=(6, 36), fontsize=7.6,
            color=C["gray"], va="center", arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.legend(fontsize=7.6, loc="upper right", bbox_to_anchor=(1, 0.97))
a2.set_title("(나) 시간-방사능 곡선 ($BP_{ND}$ = 3)", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
