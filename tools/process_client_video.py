"""Turn the client's phone clips into web assets.

What arrived: four WhatsApp-recompressed clips, 480x848 portrait, 25fps, with
audio — participants of Basketball Edition 2026 talking to camera, plus some
activity B-roll. Roughly 24 MB in total.

What that means:
  * They are **not** the landscape banner video the brief asks for. Cropping
    9:16 into a full-bleed 16:9 hero would keep about a quarter of the frame and
    upscale a 480px source across 1440px — visibly soft. That item stays open.
  * They are exactly what the removed testimonial section needed, and what the
    "video volgt" slots on the media page were waiting for.

So: keep the native portrait ratio, keep the audio (the speech is the content),
re-encode to sane sizes, and pull a poster frame so nothing downloads until a
visitor presses play. Masters move out of the publish directory.
"""
import pathlib
import shutil
import subprocess
import sys

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
VIDEO = ROOT / "site/assets/video"
OUT = VIDEO / "testimonials"
MASTERS = ROOT / "brief/video-masters"
FF = imageio_ffmpeg.get_ffmpeg_exe()

# source -> (slug, poster timestamp in seconds)
#
# The poster is picked by hand from a frame sweep, not taken from an arbitrary
# offset: the first pass landed mid-sentence on three of the four, so the child
# was caught with an open mouth and half-closed eyes. These four are the frames
# where the participant is looking at the camera with a settled expression.
CLIPS = [
    ("WhatsApp Video 2026-08-31 at 15.44.41 2.mp4", "deelnemer-01", 14),
    ("WhatsApp Video 2026-08-31 at 15.44.43 2.mp4", "deelnemer-02", 38),
    ("WhatsApp Video 2026-08-31 at 15.44.46 2.mp4", "deelnemer-03", 5),
    ("WhatsApp Video 2026-08-31 at 15.44.47 2.mp4", "deelnemer-04", 8),
]

POSTERS_ONLY = "--posters" in sys.argv   # re-pick a still without re-encoding


def run(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    MASTERS.mkdir(parents=True, exist_ok=True)

    total_in = total_out = 0
    for source, slug, poster_at in CLIPS:
        src = VIDEO / source
        if not src.exists():
            src = MASTERS / source
        if not src.exists():
            print("  missing:", source)
            continue
        total_in += src.stat().st_size

        mp4 = OUT / f"{slug}.mp4"
        webm = OUT / f"{slug}.webm"
        jpg = OUT / f"{slug}.jpg"

        # H.264 for reach, VP9 for weight; mono audio at speech bitrate
        if not POSTERS_ONLY:
            run(["-i", str(src), "-c:v", "libx264", "-crf", "28", "-preset", "slow",
             "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "aac", "-b:a", "64k", "-ac", "1", str(mp4)])
        if not POSTERS_ONLY:
            run(["-i", str(src), "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
                 "-row-mt", "1", "-c:a", "libopus", "-b:a", "48k", "-ac", "1", str(webm)])
        run(["-ss", str(poster_at), "-i", str(src), "-frames:v", "1", "-q:v", "3", str(jpg)])

        if POSTERS_ONLY:
            print(f"  {slug}: poster re-picked at {poster_at}s")
            continue
        out_bytes = mp4.stat().st_size + webm.stat().st_size + jpg.stat().st_size
        total_out += out_bytes
        print(f"  {slug}: {src.stat().st_size/1e6:.1f} MB -> "
              f"mp4 {mp4.stat().st_size/1e6:.1f} + webm {webm.stat().st_size/1e6:.1f} MB")

        # the master leaves the publish directory so it is never deployed
        if src.parent == VIDEO:
            shutil.move(str(src), MASTERS / source)

    print(f"  masters moved to brief/video-masters ({total_in/1e6:.1f} MB, not deployed)")
    print(f"  web assets: {total_out/1e6:.1f} MB")


if __name__ == "__main__":
    main()
