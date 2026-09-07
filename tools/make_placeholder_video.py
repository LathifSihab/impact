"""Build the placeholder hero loop until IMPACT supplies the aftermovie master.

Three of their own stills with a slow push-in and cross-fades, ending where it
starts so the loop is seamless. Encoded muted, 1280x720, VP9 (webm) + H.264 (mp4)
to match the <source> order in main.js. Replace both files with the real cut and
nothing else changes.
"""
import pathlib
import numpy as np
from PIL import Image
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "site/assets/img"
OUT = ROOT / "site/assets/video"
OUT.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 25
SHOTS = ["court-169.jpg", "field-169.jpg", "hands-169.jpg"]
HOLD, FADE = 3.4, 0.9           # seconds per shot, cross-fade length
ZOOM = 0.08                     # push-in over the shot


def frame(im, t):
    """t in 0..1 across the shot; returns a WxH RGB array with a slow push-in."""
    z = 1 + ZOOM * t
    cw, ch = int(im.width / z), int(im.height / z)
    x, y = (im.width - cw) // 2, int((im.height - ch) * 0.45)
    return np.asarray(im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS))


def main():
    shots = []
    for name in SHOTS:
        im = Image.open(IMG / name).convert("RGB")
        s = min(im.width / W, im.height / H)
        im = im.resize((int(im.width / s * 1.12), int(im.height / s * 1.12)), Image.LANCZOS)
        shots.append(im)

    hold_n, fade_n = int(HOLD * FPS), int(FADE * FPS)
    frames = []
    for i, im in enumerate(shots):
        nxt = shots[(i + 1) % len(shots)]
        for k in range(hold_n):
            frames.append(frame(im, k / (hold_n + fade_n)))
        for k in range(fade_n):
            a = frame(im, (hold_n + k) / (hold_n + fade_n))
            b = frame(nxt, k / (hold_n + fade_n) * 0.15)
            w = k / fade_n
            frames.append((a * (1 - w) + b * w).astype(np.uint8))

    print("frames:", len(frames), "= %.1fs" % (len(frames) / FPS))
    for ext, codec, args in (
        ("webm", "libvpx-vp9", ["-b:v", "0", "-crf", "40", "-row-mt", "1", "-an"]),
        ("mp4", "libx264", ["-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]),
    ):
        path = OUT / ("hero." + ext)
        w = imageio_ffmpeg.write_frames(str(path), (W, H), fps=FPS, codec=codec,
                                        quality=None, output_params=args, macro_block_size=1)
        w.send(None)
        for f in frames:
            w.send(f)
        w.close()
        print("  %s: %.1f MB" % (path.name, path.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
