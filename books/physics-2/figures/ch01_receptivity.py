from figstyle import plt, np, save, C

# 뇌 조직에서 얻는 MR 신호의 상대 크기 = 농도 × 존재비 × 핵 하나의 감도.
# 핵 하나의 감도는 같은 B0에서 |γ|^3 I(I+1)에 비례한다(¹H = 1).
def sens(g, I):
    return abs(g) ** 3 * I * (I + 1) / (42.577 ** 3 * 0.75)

rows = [  # (이름, 핵 농도 mM, 존재비, γ/2π, I)
    ("¹H 물", 89000, 1.0, 42.577, 0.5),
    ("¹H NAA (메틸 3개)", 30, 1.0, 42.577, 0.5),
    ("²³Na 조직 나트륨", 45, 1.0, 11.262, 1.5),
    ("¹⁷O 물 (자연 존재비)", 44500, 0.00038, 5.772, 2.5),
    ("³¹P 크레아틴인산", 4.5, 1.0, 17.235, 0.5),
    ("²H 물 (자연 존재비)", 89000, 0.00016, 6.536, 1.0),
    ("¹³C 글루탐산 C4 (자연 존재비)", 10, 0.0107, 10.708, 0.5),
]
vals = [c * a * sens(g, I) / 89000 for _, c, a, g, I in rows]
cols = [C["blue"], C["blue"], C["green"], C["gray"], C["green"], C["gray"], C["gray"]]
fig, ax = plt.subplots(figsize=(6.8, 3.2))
y = np.arange(len(rows))[::-1]
ax.barh(y, vals, color=cols, height=0.6)
for yi, v in zip(y, vals):
    if v < 1:
        m, ex = f"{v:.0e}".split("e")
        sup = str(int(ex)).replace("-", "⁻").translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        lab = f"{m}×10{sup}"
    else:
        lab = "1"
    ax.text(v * 1.4, yi, lab, va="center", fontsize=8)
ax.set_yticks(y)
ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(1e-8, 10)
ax.set_xticks([1e-8, 1e-6, 1e-4, 1e-2, 1])
ax.set_xticklabels(["10⁻⁸", "10⁻⁶", "10⁻⁴", "10⁻²", "1"])
ax.minorticks_off()
ax.set_xlabel("같은 자기장·같은 부피에서 신호의 상대 크기 (¹H 물 = 1, 로그)")
fig.tight_layout()
save(fig, __file__)
