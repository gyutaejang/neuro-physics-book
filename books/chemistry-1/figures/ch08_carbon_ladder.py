import io

from PIL import Image
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

from figstyle import plt, np, save, C


def mol_with_h(smiles, size=(300, 260)):
    # 작은 분자는 수소를 모두 그려야 산화수를 셀 수 있다.
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    d = rdMolDraw2D.MolDraw2DCairo(*size)
    o = d.drawOptions()
    o.bondLineWidth = 2
    o.padding = 0.15
    o.fixedBondLength = 55
    o.minFontSize = 18
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert("RGBA"))


# 탄소 하나짜리 분자의 산화수 사다리. 오른쪽으로 갈수록 탄소가 전자를 잃는다(산화).
items = [
    ("C", "메테인", r"CH$_4$", "−4"),
    ("CO", "메탄올", r"CH$_3$OH", "−2"),
    ("C=O", "폼알데하이드", "HCHO", "0"),
    ("OC=O", "폼산", "HCOOH", "+2"),
    ("O=C=O", "이산화탄소", r"CO$_2$", "+4"),
]
fig = plt.figure(figsize=(7.2, 3.2))
w = 0.18
for i, (smi, name, formula, ox) in enumerate(items):
    x0 = 0.02 + i * 0.195
    ax = fig.add_axes([x0, 0.36, w, 0.46])
    ax.imshow(mol_with_h(smi))
    ax.axis("off")
    fig.text(x0 + w / 2, 0.93, name, ha="center", va="center", fontsize=9.5)
    fig.text(x0 + w / 2, 0.85, formula, ha="center", va="center", fontsize=9.5)
    fig.text(x0 + w / 2, 0.31, f"C의 산화수 {ox}", ha="center", va="center", fontsize=9.5,
             color=C["blue"], weight="bold")

ax = fig.add_axes([0.02, 0.0, 0.96, 0.24])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.annotate("", xy=(0.99, 0.72), xytext=(0.01, 0.72),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.8, mutation_scale=14))
ax.text(0.5, 0.86, "산화: 한 칸마다 전자 2개를 잃는다 (H를 잃거나 O를 얻는다)",
        ha="center", va="bottom", fontsize=9, color=C["red"])
ax.annotate("", xy=(0.01, 0.3), xytext=(0.99, 0.3),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.8, mutation_scale=14))
ax.text(0.5, 0.12, "환원: 전자를 얻는다. 왼쪽일수록 산소로 태울 때 내놓는 에너지가 크다",
        ha="center", va="top", fontsize=9, color=C["green"])
save(fig, __file__)
