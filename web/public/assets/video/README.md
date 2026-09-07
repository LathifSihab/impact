# Hero video

Drop the aftermovie here as:

- `hero.webm` — VP9/AV1, 16:9, muted, 10–20s seamless loop, target < 8 MB
- `hero.mp4`  — H.264 fallback, same cut

The homepage picks them up automatically (see `assets/js/main.js`, "hero video"):
the poster still shows first, the video is only fetched when the file exists and the
visitor has not asked for reduced motion. Same pattern as foodmaker.be.

`ffmpeg -i source.mov -t 18 -an -vf scale=1920:-2 -c:v libvpx-vp9 -crf 34 -b:v 0 hero.webm`
`ffmpeg -i source.mov -t 18 -an -vf scale=1920:-2 -c:v libx264 -crf 24 -movflags +faststart hero.mp4`
