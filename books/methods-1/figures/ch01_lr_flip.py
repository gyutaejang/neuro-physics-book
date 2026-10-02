from figstyle import plt, np, save, C
from ch01_voxel_array import brain_slice

# 배열의 열 번호 i가 커질수록 환자의 오른쪽(RAS)인 축상면. 위쪽이 앞쪽이다.
n = 96
img = brain_slice(n, seed=1).astype(float)
y, x = np.mgrid[0:n, 0:n]
# 왼쪽 하전두 부근 활성(언어 과제), 오른쪽 머리 바깥의 비타민 E 표지
act = np.exp(-(((x - 27) / 5.5) ** 2 + ((y - 30) / 5.5) ** 2))
marker = (x - 88) ** 2 + (y - 48) ** 2 <= 4
img[marker] = 900


def show(ax, im, a, left, right, title, bad=False):
    ax.imshow(im, cmap="gray", vmin=0, vmax=900)
    ax.imshow(np.ma.masked_less(a, 0.25), cmap="autumn_r", vmin=0.2, vmax=1.0, alpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(C["red"] if bad else C["gray"])
        s.set_linewidth(1.6 if bad else 0.8)
    ax.text(3, 6, left, color="white", fontsize=12, weight="bold", va="top")
    ax.text(n - 4, 6, right, color="white", fontsize=12, weight="bold", va="top", ha="right")
    ax.set_title(title, fontsize=9.5, color=C["red"] if bad else C["ink"])


fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw=dict(wspace=0.08))
show(axs[0], img, act, "L", "R", "(가) 신경과 관례\n환자 왼쪽이 화면 왼쪽")
show(axs[1], img[:, ::-1], act[:, ::-1], "R", "L", "(나) 방사선과 관례\n환자 왼쪽이 화면 오른쪽")
show(axs[2], img[:, ::-1], act[:, ::-1], "L", "R", "(다) 헤더 오류: 배열은 뒤집혔는데\n표시는 (가)처럼", bad=True)
for ax, col in zip(axs, [88, 7, 7]):
    ax.annotate("표지", xy=(col, 48), xytext=(col + (-14 if col > 48 else 14), 74), color="white",
                fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="->", color="white", lw=0.9))
axs[2].set_xlabel("활성이 오른쪽 반구에 보이고,\n오른쪽에 붙인 표지가 왼쪽에 있다", fontsize=8.5, color=C["red"])
axs[0].set_xlabel("왼쪽 하전두 활성", fontsize=8.5)
axs[1].set_xlabel("같은 데이터, 거울상 표시", fontsize=8.5)
save(fig, __file__)
