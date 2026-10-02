from figstyle import log_scale_map, save

items = [
    (1e-10, "이온 지름\n~0.1 nm"),
    (5e-9, "세포막 두께\n~5 nm"),
    (2e-8, "시냅스 틈\n~20 nm"),
    (4e-8, "시냅스 소포\n~40 nm"),
    (1e-6, "축삭 지름\n~1 μm"),
    (2e-5, "세포체\n~20 μm"),
    (5e-4, "피질 기둥\n~0.5 mm"),
    (2.5e-3, "fMRI 복셀\n~2–3 mm"),
    (3e-2, "해마 길이\n~4 cm"),
    (1.7e-1, "뇌 앞뒤 길이\n~17 cm"),
]
ticks = [(1e-10, "0.1 nm"), (1e-9, "1 nm"), (1e-8, "10 nm"), (1e-7, "100 nm"), (1e-6, "1 μm"),
         (1e-5, "10 μm"), (1e-4, "100 μm"), (1e-3, "1 mm"), (1e-2, "1 cm"), (1e-1, "10 cm"), (1, "1 m")]
fig, ax = log_scale_map(items, "길이 (로그 눈금: 한 칸이 10배)", (5e-11, 2), figsize=(7.5, 3.4), ticks=ticks)
ax.tick_params(axis="x", labelsize=7.5)
save(fig, __file__)
