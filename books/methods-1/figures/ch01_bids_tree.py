from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch

# BIDS 폴더 구조(왼쪽)와 BOLD 영상 옆에 붙는 JSON 사이드카(오른쪽).
MONO = "DejaVu Sans Mono"
tree = [
    (0, "my_study/", None),
    (1, "dataset_description.json", "데이터셋 이름, BIDS 버전"),
    (1, "participants.tsv", "참가자별 나이, 성별, 집단"),
    (1, "sub-01/", None),
    (2, "anat/", None),
    (3, "sub-01_T1w.nii.gz", "구조 영상"),
    (3, "sub-01_T1w.json", None),
    (2, "func/", None),
    (3, "sub-01_task-stroop_bold.nii.gz", "4차원 BOLD"),
    (3, "sub-01_task-stroop_bold.json", "획득 변수(오른쪽)"),
    (3, "sub-01_task-stroop_events.tsv", "자극 시각과 조건"),
    (2, "fmap/", None),
    (3, "sub-01_dir-AP_epi.nii.gz", "역위상 부호화 쌍"),
    (2, "eeg/", None),
    (3, "sub-01_task-oddball_eeg.vhdr", "BrainVision 원자료"),
    (1, "sub-02/ …", None),
    (1, "derivatives/", "전처리 결과는 따로"),
]

fig = plt.figure(figsize=(7.4, 3.9))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

y0, dy = 95, 5.4
for k, (lev, name, note) in enumerate(tree):
    y = y0 - k * dy
    x = 1.5 + lev * 3.2
    if lev > 0:
        ax.plot([x - 2.2, x - 0.6], [y, y], color=C["gray"], lw=0.7)
    folder = name.endswith("/") or name.endswith("…")
    ax.text(x, y, name, family=MONO, fontsize=7.4, va="center",
            color=C["blue"] if folder else C["ink"], weight="bold" if folder else "normal")
    if note:
        ax.text(41.5, y, note, fontsize=7.4, va="center", color=C["green"])
# 세로 가지
for lev in (1, 2, 3):
    idx = [k for k, t in enumerate(tree) if t[0] == lev]
for k, (lev, _, _) in enumerate(tree):
    if lev == 0:
        continue
    # 부모를 찾아 세로선
    p = max(j for j in range(k) if tree[j][0] == lev - 1)
    x = 1.5 + lev * 3.2 - 2.2
    ax.plot([x, x], [y0 - p * dy - 2.0, y0 - k * dy], color=C["gray"], lw=0.7)

# JSON 사이드카
bx, by, bw, bh = 62.5, 22, 36.5, 70
ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.4,rounding_size=1.5",
                            fc=C["light"], ec=C["blue"], lw=1))
ax.text(bx + 1.2, by + bh - 3.5, "sub-01_task-stroop_bold.json", family=MONO,
        fontsize=7.2, weight="bold", color=C["blue"])
lines = ['{', '  "RepetitionTime": 2.0,', '  "EchoTime": 0.03,',
         '  "FlipAngle": 77,', '  "SliceTiming": [0.0, 1.0,',
         '                  0.0556, …],', '  "PhaseEncodingDirection": "j-",',
         '  "TotalReadoutTime": 0.0315,', '  "MultibandAccelerationFactor": 1,',
         '  "TaskName": "stroop"', '}']
for k, s in enumerate(lines):
    ax.text(bx + 1.2, by + bh - 10 - k * 5.1, s, family=MONO, fontsize=7.0, color=C["ink"])
ax.text(bx + bw / 2, by - 5, "단위는 초(s). 전처리 도구가 이 값을 읽는다.",
        ha="center", fontsize=7.6, color=C["red"])
ax.annotate("", xy=(bx - 0.6, y0 - 9 * dy), xytext=(56, y0 - 9 * dy),
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.9))
save(fig, __file__)
