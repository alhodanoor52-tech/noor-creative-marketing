"""Original soft ambient piano + pad bed. usage: python3 music.py out.wav seconds"""
import sys, wave
import numpy as np

SR = 44100
out, dur = sys.argv[1], float(sys.argv[2])
n = int(SR * dur)
t = np.arange(n) / SR
mix = np.zeros(n)

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

# I - vi - IV - V in C major, 4s per chord
chords = [[48, 55, 60, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]]
bar = 4.0

def piano(freq, start, length, amp):
    s0 = int(start * SR)
    if s0 >= n:
        return
    ln = min(int(length * SR), n - s0)
    tt = np.arange(ln) / SR
    env = np.exp(-tt * 1.6) * np.minimum(1, tt / 0.008)
    tone = (np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(4 * np.pi * freq * tt)
            + 0.12 * np.sin(6 * np.pi * freq * tt))
    mix[s0:s0 + ln] += amp * env * tone

# soft pad: slow attack sines per chord
for i in range(int(np.ceil(dur / bar))):
    ch = chords[i % 4]
    s0, s1 = int(i * bar * SR), min(int((i + 1) * bar * SR) + int(0.8 * SR), n)
    tt = np.arange(s1 - s0) / SR
    env = np.minimum(1, tt / 1.2) * np.minimum(1, (len(tt) / SR - tt) / 1.0)
    for m in ch:
        f = hz(m)
        mix[s0:s1] += 0.035 * env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt))
    # gentle arpeggio, 8 notes per bar
    arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12, ch[1] + 24, ch[3] + 12, ch[2] + 12, ch[3] + 12]
    for k, m in enumerate(arp):
        piano(hz(m), i * bar + k * bar / 8, 2.5, 0.09 if k % 4 == 0 else 0.06)
    piano(hz(ch[0]), i * bar, 3.5, 0.10)

# simple reverb-ish echoes
rev = mix.copy()
for d, g in [(0.11, 0.35), (0.23, 0.25), (0.37, 0.18), (0.53, 0.12)]:
    k = int(d * SR)
    rev[k:] += g * mix[:-k]
fade = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 2.5)
rev *= fade
rev /= np.max(np.abs(rev)) + 1e-9
rev *= 0.8
stereo = np.stack([rev, np.roll(rev, int(0.012 * SR))], axis=1)
pcm = (stereo * 32767).astype(np.int16)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', out)
