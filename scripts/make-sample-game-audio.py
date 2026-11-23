#!/usr/bin/env python3
"""雛形のリズムゲーム用仮音源を作る（テンプレート専用）。

CD 側の仮音源（10秒）は滑らかな音で打音が無く、譜面生成（打音の解析）が
検証できない。そのためゲーム側の仮音源だけは、キック・スネア・ハット・
ベース・メロディーを持つ単純な合成曲（24秒）をここで作る。メロディーは
音高が偏ると譜面のレーン分布が偏って生成器の検証に落ちるため、音階全体を
均等に回す。新作では使わない（実在の曲の MP3 を src/game/assets/ に置く。
手順は docs/PRODUCTION.md）。

使い方: python3 scripts/make-sample-game-audio.py
出力: src/game/assets/track01.mp3 / track02.mp3（MP3 192kbps、ffmpeg が必要）
"""
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent


def midi(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def add_tone(buf: np.ndarray, t0: float, freq: float, dur: float, gain: float, decay: float = 6.0) -> None:
    i0 = int(t0 * SR)
    n = int(dur * SR)
    if i0 >= len(buf):
        return
    n = min(n, len(buf) - i0)
    t = np.arange(n) / SR
    env = np.exp(-decay * t)
    tone = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
    buf[i0:i0 + n] += gain * env * tone


def add_kick(buf: np.ndarray, t0: float, gain: float = 0.9) -> None:
    i0 = int(t0 * SR)
    n = int(0.14 * SR)
    if i0 >= len(buf):
        return
    n = min(n, len(buf) - i0)
    t = np.arange(n) / SR
    freq = 45 + 75 * np.exp(-28 * t)
    phase = np.cumsum(2 * np.pi * freq / SR)
    buf[i0:i0 + n] += gain * np.exp(-16 * t) * np.sin(phase)


def add_noise(buf: np.ndarray, t0: float, rng: np.random.Generator, dur: float, gain: float, decay: float, diff: bool) -> None:
    i0 = int(t0 * SR)
    n = int(dur * SR)
    if i0 >= len(buf):
        return
    n = min(n, len(buf) - i0)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    if diff:
        noise = np.diff(np.concatenate([[0.0], noise]))  # ハット用に高域寄り
    buf[i0:i0 + n] += gain * np.exp(-decay * t) * noise


# バーごとに変えるキックの位置（拍単位）
KICK_PATTERNS = [
    [0.0, 1.0, 2.0, 3.0],
    [0.0, 1.5, 2.0, 3.0],
    [0.0, 2.0, 3.0, 3.5],
    [0.0, 1.0, 2.0, 2.5, 3.0],
]


def render(bpm: float, base: int, scale: list[int], roots: list[int], bars: int,
           chorus: set[int], seed: int, step: int = 3) -> np.ndarray:
    """base: メロディーの基準 MIDI。scale: 音階（半音オフセット）。
    roots: バーごとのベース音（MIDI）。メロディーは音階を巡回して均等に使う。"""
    rng = np.random.default_rng(seed)
    beat = 60.0 / bpm
    total = bars * 4 * beat + 0.3
    buf = np.zeros(int(total * SR))
    pool = [base + s for s in scale]
    cursor = 0
    for bar_i in range(bars):
        bar_t = bar_i * 4 * beat
        for k in KICK_PATTERNS[bar_i % len(KICK_PATTERNS)]:
            add_kick(buf, bar_t + k * beat)
        for b in (1, 3):  # スネアは 2・4 拍目（バーによってゴーストや位置の揺れを足す）
            add_noise(buf, bar_t + b * beat, rng, 0.09, 0.5, 26, diff=False)
        if bar_i % 2 == 1:
            add_noise(buf, bar_t + 3.5 * beat, rng, 0.07, 0.28, 26, diff=False)
        if bar_i % 4 == 3:
            add_noise(buf, bar_t + 0.75 * beat, rng, 0.07, 0.3, 26, diff=False)
        for e in range(8):  # ハットは 8 分音符
            add_noise(buf, bar_t + e * beat / 2, rng, 0.035, 0.16 if e % 2 else 0.24, 70, diff=True)
        root = roots[bar_i % len(roots)]
        add_tone(buf, bar_t, midi(root), beat * 0.9, 0.5, decay=3.0)
        add_tone(buf, bar_t + 2 * beat, midi(root + 7), beat * 0.9, 0.4, decay=3.0)
        in_chorus = bar_i in chorus
        for e in range(8):
            if not in_chorus and e == 7 and bar_i % 2 == 1:
                continue  # バースは末尾に抜けを作る
            note = pool[cursor % len(pool)] + (12 if in_chorus else 0)
            cursor += step  # 巡回の歩幅（音階の長さと互いに素にして全音を回す）
            add_tone(buf, bar_t + e * beat / 2, midi(note), beat / 2 * 0.95, 0.5, decay=7.0)
    peak = np.max(np.abs(buf))
    return (buf / peak * 0.89).astype(np.float32)


def to_mp3(samples: np.ndarray, out: Path) -> None:
    wav_path = out.with_suffix('.wav')
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(str(wav_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(
        ['ffmpeg', '-y', '-v', 'error', '-i', str(wav_path), '-codec:a', 'libmp3lame', '-b:a', '192k', str(out)],
        check=True,
    )
    wav_path.unlink()


def main() -> None:
    major = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    minor = [-5, -3, 0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27]
    # track-a: BPM 120・C メジャー、12 バー（24秒）。サビは 7–10 バー目（12–20秒）
    to_mp3(
        render(120, 60, major, [36, 43, 41, 38], 12, {6, 7, 8, 9}, seed=1, step=4),
        ROOT / 'src/game/assets/track01.mp3',
    )
    # track-b: BPM 132・A マイナー、13 バー（約23.6秒）。サビは 6–9 バー目（約10.9–18.2秒）
    to_mp3(
        render(132, 57, minor, [33, 41, 36, 43], 13, {6, 7, 8, 9}, seed=2, step=11),
        ROOT / 'src/game/assets/track02.mp3',
    )
    print('src/game/assets/track01.mp3 / track02.mp3 を作った')


if __name__ == '__main__':
    main()
