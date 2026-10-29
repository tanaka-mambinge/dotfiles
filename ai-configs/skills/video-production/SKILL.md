---
name: video-production
description: Personal visual storytelling and motion preferences for creating or editing videos. Use alongside the relevant production workflow to make voice-led videos with deliberate pacing, sparse on-screen text, progressive visual reveals, and expressive motion.
---

# Video production craft

Use this skill as a personal craft layer alongside the workflow that builds the video. Before creating a video or updating an existing one, read all of the craft references below to understand what to preserve, improve, or create. Also inspect the brief, current video and available visual references. Revisit a topic guide while working when its decisions come up:

- [Visual storytelling](references/visual-storytelling.md) for reference use, information density, scene reveals, and text legibility.
- [Motion](references/motion.md) for GSAP easing and reveal pacing.
- [Assets](references/assets.md) for icons, logos, and custom vector artwork.
- [Effects](references/effects.md) for gradients, glow, and shader inspiration.
- [Typography](references/typography.md) for font choices and typographic roles.

When narration or spoken audio drives the edit, use `scripts/transcribe.py <audio-path>` to create a timestamped transcript. It prints JSON to the terminal by default; pass `--output <path>` to save it as a file. The JSON includes vowel-weighted estimated word timings inside each segment. Treat those timings as pacing cues, not measured alignment. The model is downloaded only when this script runs and the cached model is missing. If the transcription runtime is unavailable, run `python scripts/setup-transcriber.py`.

To reduce background noise in a recording, run `python scripts/denoise.py <audio-path>`. It saves `<filename>_denoised.wav` beside the source; pass `--output <path.wav>` to choose another location. It accepts mono or stereo WAV, FLAC, OGG, MP3, and AIFF audio, and keeps the source sample rate and channel count. It uses the MossFormer2_SE_48K speech-enhancement model; `--strength 0..1` blends in the original audio for a gentler effect. On first use per computer, it downloads the model and the required audio runtime into the video-production cache. Set `VIDEO_PRODUCTION_CACHE_DIR` to reuse a different cache location. Video files are not accepted.
