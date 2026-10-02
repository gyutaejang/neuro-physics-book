from scipy.ndimage import gaussian_filter

from figstyle import plt, np, save, C

# 2 mm 복셀 48³ 합성 볼륨. 백색 잡음(σ = 1) 위에 작은 활성(FWHM 5 mm)과 큰 활성(FWHM 12 mm).
v = 2.0
n = 48
k = 2 * np.sqrt(2 * np.log(2))                 # FWHM = 2.355 σ
z, y, x = np.mgrid[:n, :n, :n] * v
c = n * v / 2


def blob(cx, cy, fwhm, amp):
    s = fwhm / k
    return amp * np.exp(-((x - cx) ** 2 + (y - cy) ** 2 + (z - c) ** 2) / (2 * s ** 2))


sig = blob(30, 48, 5, 1.6) + blob(66, 48, 12, 0.7)
rng = np.random.default_rng(3)
noise = rng.normal(0, 1, sig.shape)
fw_show = [0, 4, 8, 14]


def zmap(fw):
    if fw == 0:
        return sig + noise
    s = fw / k / v
    sd = np.sqrt(np.sum(gaussian_filter(_delta, s) ** 2))     # 평활화 뒤 잡음 표준편차
    return gaussian_filter(sig + noise, s) / sd


_delta = np.zeros((41, 41, 41))
_delta[20, 20, 20] = 1


def gain(fw_sig, fws):
    """평활화 FWHM에 따른 봉우리 SNR (평활화 안 함 = 1). 3차원, 이산 커널로 정확히 계산."""
    s0 = blob(c, c, fw_sig, 1.0)
    out = []
    for fw in fws:
        if fw == 0:
            out.append(1.0)
            continue
        s = fw / k / v
        pk = gaussian_filter(s0, s)[n // 2, n // 2, n // 2]
        sd = np.sqrt(np.sum(gaussian_filter(_delta, s) ** 2))
        out.append(pk / sd)
    return np.array(out)


fws = np.arange(0, 20.5, 0.5)            # 인덱스 i ↔ FWHM i/2 mm
g5, g12 = gain(5, fws), gain(12, fws)
print("small best", fws[g5.argmax()], g5.max().round(2), " at 8:", g5[16].round(2), " at 14:", g5[28].round(2))
print("large best", fws[g12.argmax()], g12.max().round(2), " at 4:", g12[8].round(2), " at 8:", g12[16].round(2))

fig = plt.figure(figsize=(7.4, 3.3))
gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 0.22, 2.25], wspace=0.06, hspace=0.25,
                      left=0.02, right=0.93, top=0.86, bottom=0.14)
mid = n // 2
for i, fw in enumerate(fw_show):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    im = zmap(fw)[mid]
    ax.imshow(im, cmap="RdBu_r", vmin=-5, vmax=5, origin="lower", extent=(0, n * v, 0, n * v))
    for cx, fw_s in ((30, 5), (66, 12)):
        ax.add_patch(plt.Circle((cx, 48), fw_s / 2, fill=False, ec=C["ink"], lw=0.8, ls="--"))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("평활화 없음" if fw == 0 else f"FWHM {fw} mm", fontsize=9, pad=2)
ax = fig.add_subplot(gs[:, 3])
g5, g12 = 1.6 * g5, 0.7 * g12                    # 기대 봉우리 z (진폭 1.6σ, 0.7σ)
print("z small", g5[[0, 8, 10, 16, 28]].round(2), "z large", g12[[0, 8, 16, 24, 40]].round(2))
ax.plot(fws, g5, color=C["red"], lw=1.8, label="작은 활성 (FWHM 5 mm, 진폭 1.6σ)")
ax.plot(fws, g12, color=C["blue"], lw=1.8, label="큰 활성 (FWHM 12 mm, 진폭 0.7σ)")
ax.text(19.8, 3.25, "z = 3.1", fontsize=7.5, color=C["gray"], ha="right", va="bottom")
for g, col in ((g5, C["red"]), (g12, C["blue"])):
    i = g.argmax()
    ax.scatter([fws[i]], [g[i]], color=col, s=18, zorder=3)
ax.axhline(3.1, color=C["gray"], lw=0.8, ls="--")
ax.set_xlabel("평활화 커널 FWHM (mm)")
ax.set_ylabel("활성 중심의 기대 z", fontsize=9)
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()
ax.spines["right"].set_visible(True)
ax.spines["left"].set_visible(False)
ax.legend(fontsize=7.5, loc="center right", bbox_to_anchor=(1.0, 0.64))
ax.set_xlim(0, 20)
ax.set_title("(나) 커널 ≈ 활성 크기일 때 z가 최대", fontsize=9.5)
fig.text(0.23, 0.95, "(가) 가운데 단면의 z 지도 (점선: 실제 활성)", ha="center", fontsize=9.5)
save(fig, __file__)
