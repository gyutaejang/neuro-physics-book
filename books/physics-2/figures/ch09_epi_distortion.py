from figstyle import plt, np, save, C

# EPI 왜곡: 장 불균일 Δf(Hz)가 위상 부호화 방향으로 Δy = Δf / BW_PE 픽셀만큼 신호를 옮긴다.
# 앞쪽(위) 이마굴 근처에 +양의 Δf 덩어리를 둔다. BW_PE ≈ 21 Hz/픽셀(에코 간격 0.5 ms, 96줄).
N = 96
up = 4                       # 신호를 옮길 때 쓰는 세분 격자
y, x = np.mgrid[1.3:-1.3:N * up * 1j, -1.3:1.3:N * up * 1j]
th = np.arctan2(y, x)
r = np.sqrt((x / 0.7) ** 2 + (y / 0.82) ** 2)
wav = 1 + 0.025 * np.sin(14 * th)
img = np.zeros_like(x)
img[r < 0.88] = 0.55
img[r < 0.85 * wav] = 0.75
img[r < 0.72 * wav] = 0.95
for sx in (-1, 1):
    img[np.sqrt(((x - sx * 0.11) / 0.07) ** 2 + ((y - 0.05) / 0.26) ** 2) < 1] = 0.3
# 격자선(왜곡이 잘 보이도록)
grid = ((np.abs((x * 5) % 1 - 0.5) < 0.04) | (np.abs((y * 5) % 1 - 0.5) < 0.04)) & (r < 0.88)
img[grid] *= 0.55

df = 110 * np.exp(-((x / 0.28) ** 2 + ((y - 0.78) / 0.16) ** 2))  # Hz, 이마굴 아래 앞이마엽
BW = 1 / (0.5e-3 * 96)                                              # Hz/픽셀
dy_px = df / BW                                                    # 픽셀(굵은 격자 기준)


def distort(sign):
    """sign=+1: 위상 부호화 '앞으로'(위로) 이동, −1: 반대 방향."""
    out = np.zeros_like(img)
    rows = np.arange(N * up)[:, None] * np.ones((1, N * up))
    new = rows - sign * dy_px * up       # 위로 = 행 번호 감소
    cols = np.arange(N * up)[None, :] * np.ones((N * up, 1))
    ok = (new >= 0) & (new < N * up - 1)
    np.add.at(out, (np.round(new[ok]).astype(int), cols[ok].astype(int)), img[ok])
    return out.reshape(N, up, N, up).mean(axis=(1, 3))


fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.75))
ax = axes[0]
base = img.reshape(N, up, N, up).mean(axis=(1, 3))
ax.imshow(base, cmap="gray", vmin=0, vmax=1)
cs = ax.contour(df.reshape(N, up, N, up).mean(axis=(1, 3)), levels=[20, 50, 90],
                colors=[C["red"]], linewidths=0.8)
ax.clabel(cs, fmt="%d Hz", fontsize=6.5)
ax.set_title("(가) 실제 모양과 장 불균일 Δf", fontsize=8.5)
for k, (sgn, title) in enumerate([(+1, "(나) 위상 부호화 ↑ : 늘어남"), (-1, "(다) 위상 부호화 ↓ : 뭉침")]):
    a = axes[k + 1]
    a.imshow(distort(sgn), cmap="gray", vmin=0, vmax=1)
    a.set_title(title, fontsize=8.5)
for a in axes:
    a.set_xticks([])
    a.set_yticks([])
    for sp in a.spines.values():
        sp.set_visible(False)
axes[0].text(48, 92, f"최대 {df.max():.0f} Hz → {df.max() / BW:.1f} 픽셀", color="white",
             fontsize=7, ha="center")
fig.tight_layout(w_pad=0.4)
save(fig, __file__)
