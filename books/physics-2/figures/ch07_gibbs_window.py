from figstyle import plt, np, save, C

# (가) 깁스 링잉: 날카로운 경계(뇌척수액–조직)를 유한한 주파수만으로 다시 만들면 경계 옆에 물결이 생긴다.
# (나) 스펙트럼 누출: 1 s 구간에 정수배가 아닌 10.25 Hz 사인파를 넣으면 이웃 주파수로 번진다.
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"wspace": 0.3})

N = 1024
x = (np.arange(N) - N // 2) * 0.125          # 0.125 mm 격자, 128 mm
prof = np.where(np.abs(x) < 20, 1.0, 0.3)    # 가운데 밝은 뇌척수액 띠(폭 40 mm), 바깥 조직
k = np.fft.fftfreq(N, 0.125)
P = np.fft.fft(prof)
kmax = 1 / (2 * 220 / 64)
cut = np.abs(k) <= kmax
rect = np.real(np.fft.ifft(P * cut))
hann = np.real(np.fft.ifft(P * cut * 0.5 * (1 + np.cos(np.pi * k / kmax))))
a1.plot(x, prof, color=C["gray"], lw=1, ls=":", label="실제 경계")
a1.plot(x, rect, color=C["red"], lw=1.4, label="자른 그대로")
a1.plot(x, hann, color=C["blue"], lw=1.4, label="한 창을 씌움")
a1.set_xlim(5, 50)
a1.set_ylim(0.1, 1.25)
a1.set_xlabel("위치 (mm)")
a1.set_ylabel("신호 세기")
a1.legend(fontsize=7.5, loc="upper right")
over = (rect.max() - 1) / 0.7
a1.annotate(f"넘침 약 {over * 100:.0f}%", xy=(x[np.argmax(rect * (x > 0))], rect.max()),
            xytext=(6, 1.17), fontsize=8, color=C["red"],
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
a1.set_title("(가) 깁스 링잉 (복셀 약 3.4 mm)", fontsize=9.5)

fs, T = 1000, 1.0
t = np.arange(0, T, 1 / fs)
s = np.sin(2 * np.pi * 10.25 * t)
fr = np.fft.rfftfreq(len(t), 1 / fs)
for w, col, lab in ((np.ones_like(t), C["red"], "사각 창(그냥 자름)"),
                    (np.hanning(len(t)), C["blue"], "한 창")):
    S = np.abs(np.fft.rfft(s * w))
    S = S / S.max()
    a2.plot(fr, 20 * np.log10(S + 1e-9), color=col, marker="o", ms=2.5, lw=1, label=lab)
a2.set_xlim(0, 30)
a2.set_ylim(-70, 5)
a2.axvline(10.25, color=C["gray"], lw=0.6, ls=":")
a2.text(10.6, -66, "실제 10.25 Hz", fontsize=7.5, color=C["gray"])
a2.set_xlabel("주파수 (Hz)")
a2.set_ylabel("상대 파워 (dB)")
a2.legend(fontsize=7.5, loc="upper right")
a2.set_title("(나) 스펙트럼 누출 (1 s 구간)", fontsize=9.5)
save(fig, __file__)
