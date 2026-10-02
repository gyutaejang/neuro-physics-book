import io

from PIL import Image
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

from figstyle import plt, np, save, C

# L-DOPA (S)와 그 거울상 D-DOPA (R). L형의 2D 좌표를 좌우로 뒤집어 D형을 만든다.
L = Chem.MolFromSmiles("N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O")
AllChem.Compute2DCoords(L)
Chem.WedgeMolBonds(L, L.GetConformer())
D = Chem.Mol(L)
conf = D.GetConformer()
for i in range(D.GetNumAtoms()):
    p = conf.GetAtomPosition(i)
    conf.SetAtomPosition(i, (-p.x, p.y, 0.0))
Chem.AssignChiralTypesFromBondDirs(D)
Chem.AssignStereochemistry(D, cleanIt=True, force=True)
assert Chem.FindMolChiralCenters(L)[0][1] == "S"
assert Chem.FindMolChiralCenters(D)[0][1] == "R"


def draw(mol):
    d = rdMolDraw2D.MolDraw2DCairo(520, 420)
    o = d.drawOptions()
    o.bondLineWidth = 2
    o.padding = 0.08
    o.prepareMolsBeforeDrawing = False
    m = rdMolDraw2D.PrepareMolForDrawing(mol, kekulize=True, addChiralHs=True, wedgeBonds=False)
    d.DrawMolecule(m, highlightAtoms=[1], highlightAtomColors={1: (1.0, 0.85, 0.7)})
    d.FinishDrawing()
    img = np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert("RGBA"))
    ys, xs = np.where(img[:, :, :3].min(axis=2) < 250)
    pad = 12
    return img[max(ys.min() - pad, 0):ys.max() + pad, max(xs.min() - pad, 0):xs.max() + pad]


fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.2))
a1.imshow(draw(L)); a1.set_title("L-DOPA (레보도파, S형): 약으로 쓴다", fontsize=9.5)
a2.imshow(draw(D)); a2.set_title("D-DOPA (R형): 거울상", fontsize=9.5)
for a in (a1, a2):
    a.axis("off")
fig.subplots_adjust(wspace=0.12)
fig.add_artist(plt.Line2D([0.5, 0.5], [0.1, 0.8], transform=fig.transFigure, color=C["gray"], lw=1, ls="--"))
fig.text(0.5, 0.07, "거울", ha="center", va="top", fontsize=8.5, color=C["gray"])
save(fig, __file__)
