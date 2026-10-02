import io

import numpy as np
from PIL import Image
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

from figstyle import plt, save


def molecule_image(smiles, size, highlight=None, min_font=17):
    """figstyle.molecule_image와 같되, 긴 분자에서도 원자 글자가 읽히도록 최소 글자 크기를 준다."""
    mol = Chem.MolFromSmiles(smiles)
    d = rdMolDraw2D.MolDraw2DCairo(*size)
    opts = d.drawOptions()
    opts.bondLineWidth = 2
    opts.padding = 0.06
    opts.minFontSize = min_font
    kw = {}
    if highlight:
        kw = {"highlightAtoms": list(highlight),
              "highlightAtomColors": {i: (1.0, 0.85, 0.7) for i in highlight}}
    d.DrawMolecule(mol, **kw)
    d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert("RGBA"))


PALM = "CCCCCCCCCCCCCCCC(=O)O"                  # 팔미트산 16:0
OLEIC = "CCCCCCCC/C=C\\CCCCCCCC(=O)O"           # 올레산 18:1 시스-9
CHOL = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3"
        "(CC[C@@H](C4)O)C)C")
POPC = ("CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC[N+](C)(C)C)"
        "OC(=O)CCCCCCC/C=C\\CCCCCCCC")

fig = plt.figure(figsize=(7.3, 4.9))
gs = fig.add_gridspec(3, 2, height_ratios=[0.55, 0.55, 1.2], width_ratios=[1.45, 0.75], hspace=0.18, wspace=0.02)
panels = [
    (gs[0, 0], PALM, (760, 170), None, "팔미트산 (포화, 16:0)"),
    (gs[1, 0], OLEIC, (760, 210), [8, 9], "올레산 (시스 이중 결합, 18:1)"),
    (gs[0:2, 1], CHOL, (420, 360), [25], "콜레스테롤"),
    (gs[2, :], POPC, (1000, 400), list(range(21, 32)), "인지질: 포스파티딜콜린 (머리 강조)"),
]
for spec, smi, size, hl, name in panels:
    ax = fig.add_subplot(spec)
    ax.imshow(molecule_image(smi, size, hl))
    ax.set_title(name, fontsize=9.5)
    ax.axis("off")
save(fig, __file__)
