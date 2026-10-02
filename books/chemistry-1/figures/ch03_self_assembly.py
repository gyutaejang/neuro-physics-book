from figstyle import plt, np, save, C


def molecule_image(smiles, size, highlight, min_font=26):
    """figstyle.molecule_image와 같지만, 사슬이 긴 분자에서도 원자 기호가 읽히도록 최소 글자 크기를 둔다."""
    import io
    from PIL import Image
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    mol = Chem.MolFromSmiles(smiles)
    d = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = d.drawOptions()
    opts.bondLineWidth = 2
    opts.padding = 0.06
    opts.minFontSize = min_font
    d.DrawMolecule(mol, highlightAtoms=highlight,
                   highlightAtomColors={i: (1.0, 0.85, 0.7) for i in highlight})
    d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert("RGBA"))


SDS = "CCCCCCCCCCCCOS(=O)(=O)[O-].[Na+]"
DPPC = "CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCCC"
sds_head = list(range(12, 18))
dppc_head = list(range(21, 32))  # 인산-콜린 머리

fig = plt.figure(figsize=(7.4, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1], width_ratios=[0.9, 1.35], hspace=0.08, wspace=0.02)
a1 = fig.add_subplot(gs[0, 0])
a2 = fig.add_subplot(gs[0, 1])
a1.imshow(molecule_image(SDS, (520, 200), sds_head))
a2.imshow(molecule_image(DPPC, (600, 420), dppc_head, min_font=19))
a1.set_title("도데실 황산 나트륨 (SDS): 꼬리 1개", fontsize=9.5)
a2.set_title("다이팔미토일 포스파티딜콜린 (DPPC): 꼬리 2개", fontsize=9.5)
for a in (a1, a2):
    a.axis("off")

# 아래: 미셀과 이중층 도식
def lipid(ax, x, y, ang, n_tails, col_head, length=0.9):
    dx, dy = np.cos(ang), np.sin(ang)
    px, py = -dy, dx
    offs = [0] if n_tails == 1 else [-0.07, 0.07]
    for o in offs:
        xs = x + dx * np.linspace(0.12, length, 12) + px * o
        ys = y + dy * np.linspace(0.12, length, 12) + py * o
        wig = 0.025 * np.sin(np.linspace(0, 6 * np.pi, 12))
        ax.plot(xs + px * wig, ys + py * wig, color=C["gray"], lw=1.1, zorder=2)
    ax.add_patch(plt.Circle((x, y), 0.13, facecolor=col_head, edgecolor=C["ink"], lw=0.6, zorder=3))

b1 = fig.add_subplot(gs[1, 0])
n = 16
for k in range(n):
    t = 2 * np.pi * k / n
    lipid(b1, 1.15 * np.cos(t), 1.15 * np.sin(t), t + np.pi, 1, C["blue"], length=1.0)
b1.text(0, -1.85, "미셀: 꼬리는 안, 머리는 물 쪽", ha="center", fontsize=9)
b1.set_xlim(-1.9, 1.9)
b1.set_ylim(-2.2, 1.5)
b1.set_aspect("equal")
b1.axis("off")

b2 = fig.add_subplot(gs[1, 1])
for x in np.arange(-2.2, 2.3, 0.33):
    lipid(b2, x, 1.0, -np.pi / 2, 2, C["blue"], length=0.92)
    lipid(b2, x, -1.0, np.pi / 2, 2, C["blue"], length=0.92)
b2.text(2.65, 0, "기름층\n(εᵣ ≈ 2)", fontsize=8.5, va="center", color=C["gray"])
b2.text(0, 1.45, "물", fontsize=9, ha="center", color=C["blue"])
b2.text(0, -1.42, "물", fontsize=9, ha="center", va="top", color=C["blue"])
b2.text(0.4, -2.15, "이중층: 꼬리 두 개짜리 지질은 판을 이룬다 (약 5 nm)", ha="center", fontsize=9)
b2.set_xlim(-2.6, 3.5)
b2.set_ylim(-2.4, 1.7)
b2.set_aspect("equal")
b2.axis("off")
save(fig, __file__)
