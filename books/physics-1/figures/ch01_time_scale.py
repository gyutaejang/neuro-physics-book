from figstyle import log_scale_map, save, C

items = [
    (1e-5, "이온 통로\n열림 ~10 μs"),
    (1e-3, "활동전위\n~1 ms"),
    (2e-2, "시냅스 후 전위\n~10–20 ms"),
    (1e-1, "알파파 한 주기\n~100 ms"),
    (2, "fMRI TR\n~1–2 s"),
    (6, "BOLD 반응 정점\n~5–6 s"),
    (3.6e3, "스캔 한 회기\n~1 h"),
    (8.64e4 * 7, "기억 공고화\n수일~수주"),
]
ticks = [(1e-6, "1 μs"), (1e-3, "1 ms"), (1, "1 s"), (60, "1분"), (3600, "1시간"), (86400, "1일"),
         (86400 * 30, "1달")]
fig, ax = log_scale_map(items, "시간 (로그 눈금)", (3e-7, 1e7), figsize=(7.5, 3.4), color=C["red"], ticks=ticks)
ax.axvspan(1, 6, ymin=0.47, ymax=0.53, color=C["red"], alpha=0.12)
save(fig, __file__)
