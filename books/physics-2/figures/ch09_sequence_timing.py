from figstyle import plt, np, save, C

# 스핀 에코(SE)와 그래디언트 에코(GRE)의 펄스 시퀀스 타이밍 도식.
# 줄: RF, 슬라이스 선택 경사, 위상 부호화 경사, 읽기(주파수 부호화) 경사, 신호.


def trap(t, t0, dur, amp, ramp=0.6):
    """t0에서 시작해 dur 동안 이어지는 사다리꼴 경사."""
    y = np.clip((t - t0) / ramp, 0, 1) * np.clip((t0 + dur - t) / ramp, 0, 1)
    return amp * y


def sinc_pulse(t, tc, width, amp):
    u = (t - tc) / (width / 4)
    y = amp * np.sinc(u) * (np.abs(t - tc) <= width / 2)
    return y


rows = ["RF", "슬라이스", "위상", "읽기", "신호"]
offs = {r: -1.6 * i for i, r in enumerate(rows)}
t = np.linspace(-2, 34, 4000)

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9), sharey=True)
for ax in axes:
    ax.set_xlim(-6.0, 34)
    ax.set_ylim(offs["신호"] - 1.0, 2.0)
    ax.axis("off")
    for r, y0 in offs.items():
        ax.plot([-1.5, 33.5], [y0, y0], color=C["gray"], lw=0.5)
for r, y0 in offs.items():
    axes[0].text(-5.8, y0 + 0.15, r, fontsize=8.5, ha="left", va="bottom", color=C["ink"])

# ---------- (가) 스핀 에코 ----------
ax = axes[0]
TE = 22.0
rf = sinc_pulse(t, 2, 3, 0.75) + sinc_pulse(t, 2 + TE / 2, 3, 1.2)
ax.fill_between(t, offs["RF"], offs["RF"] + rf, color=C["purple"], alpha=0.8, lw=0)
ax.text(2, offs["RF"] + 0.9, "90°", ha="center", fontsize=8.5)
ax.text(2 + TE / 2 + 1.0, offs["RF"] + 0.9, "180°", ha="left", fontsize=8.5)
gs = trap(t, 0.2, 3.6, 0.7) + trap(t, 3.9, 1.6, -0.7) + trap(t, 11.2, 3.6, 0.7)
ax.fill_between(t, offs["슬라이스"], offs["슬라이스"] + gs, color=C["blue"], alpha=0.75, lw=0)
for a in [-0.6, -0.4, -0.2, 0.2, 0.4, 0.6]:
    g = trap(t, 5.8, 2.6, a)
    ax.plot(t, np.where(g != 0, offs["위상"] + g, np.nan), color=C["blue"], lw=0.7)
gr = trap(t, 5.8, 2.6, 0.6) + trap(t, 2 + TE - 3.2, 6.4, 0.6)
ax.fill_between(t, offs["읽기"], offs["읽기"] + gr, color=C["blue"], alpha=0.75, lw=0)
T2s = 4.0
fid = np.where(t > 3.5, np.exp(-(t - 3.5) / T2s) * np.cos(2.6 * (t - 3.5)), 0)
echo_c = 2 + TE
echo = np.exp(-np.abs(t - echo_c) / 1.7) * np.cos(2.6 * (t - echo_c)) * 0.75
ax.plot(t, offs["신호"] + 0.8 * fid + echo, color=C["red"], lw=0.9)
ax.text(5.3, offs["신호"] + 0.6, "FID", fontsize=8, color=C["red"])
ax.text(echo_c, offs["신호"] + 0.95, "스핀 에코", ha="center", fontsize=8, color=C["red"])
# TE 표시
yA = offs["신호"] - 0.75
ax.annotate("", xy=(echo_c, yA), xytext=(2, yA),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
ax.text((2 + echo_c) / 2, yA - 0.1, "TE", ha="center", va="top", fontsize=8.5)
for x in (2, 2 + TE / 2, echo_c):
    ax.plot([x, x], [yA, 1.75], color=C["gray"], lw=0.5, ls=":")
for xa, xb in ((2, 2 + TE / 2), (2 + TE / 2, 2 + TE)):
    ax.annotate("", xy=(xb, 1.75), xytext=(xa, 1.75),
                arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.7))
    ax.text((xa + xb) / 2, 1.8, "TE/2", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
ax.set_title("(가) 스핀 에코", fontsize=10, loc="left", x=0.05)

# ---------- (나) 그래디언트 에코 ----------
ax = axes[1]
TE = 13.0
rf = sinc_pulse(t, 2, 3, 0.5)
ax.fill_between(t, offs["RF"], offs["RF"] + rf, color=C["purple"], alpha=0.8, lw=0)
ax.text(2, offs["RF"] + 0.65, "α (< 90°)", ha="center", fontsize=8.5)
rf2 = sinc_pulse(t, 30, 3, 0.5)
ax.fill_between(t, offs["RF"], offs["RF"] + rf2, color=C["purple"], alpha=0.35, lw=0)
ax.text(30, offs["RF"] + 0.65, "다음 α", ha="center", fontsize=7.5, color=C["gray"])
gs = trap(t, 0.2, 3.6, 0.7) + trap(t, 3.9, 1.6, -0.7)
ax.fill_between(t, offs["슬라이스"], offs["슬라이스"] + gs, color=C["blue"], alpha=0.75, lw=0)
for a in [-0.6, -0.4, -0.2, 0.2, 0.4, 0.6]:
    g = trap(t, 5.8, 2.6, a)
    ax.plot(t, np.where(g != 0, offs["위상"] + g, np.nan), color=C["blue"], lw=0.7)
gr = trap(t, 5.8, 2.6, -0.6) + trap(t, 2 + TE - 3.2, 6.4, 0.6)
ax.fill_between(t, offs["읽기"], offs["읽기"] + gr, color=C["blue"], alpha=0.75, lw=0)
ax.text(8.9, offs["읽기"] - 0.45, "음의 엽", ha="left", fontsize=7.5, color=C["blue"])
echo_c = 2 + TE
echo = np.exp(-np.abs(t - echo_c) / 1.7) * np.cos(2.6 * (t - echo_c)) * 0.7
ax.plot(t, offs["신호"] + echo, color=C["red"], lw=0.9)
ax.text(echo_c + 1.8, offs["신호"] + 0.45, "그래디언트 에코", ha="left", fontsize=8, color=C["red"])
ax.text(26.0, offs["읽기"] + 1.0, "스포일러", ha="center", fontsize=7.5, color=C["gray"])
ax.fill_between(t, offs["읽기"], offs["읽기"] + trap(t, 24.5, 3.0, 0.9), color=C["gray"], alpha=0.5, lw=0)
yA = offs["신호"] - 0.75
ax.annotate("", xy=(echo_c, yA), xytext=(2, yA),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
ax.text((2 + echo_c) / 2, yA - 0.1, "TE", ha="center", va="top", fontsize=8.5)
ax.annotate("", xy=(30, 1.75), xytext=(2, 1.75),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
ax.text(16, 1.8, "TR", ha="center", va="bottom", fontsize=8.5)
for x in (2, echo_c, 30):
    ax.plot([x, x], [yA, 1.75], color=C["gray"], lw=0.5, ls=":")
ax.set_title("(나) 그래디언트 에코", fontsize=10, loc="left", x=0.05)

fig.subplots_adjust(wspace=0.04)
save(fig, __file__)
