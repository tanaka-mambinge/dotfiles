---
name: stock-media
description: Search Pexels for stock photos and videos, download candidate clips, and create or inspect 16-frame visual grids before using a video. Use when an agent needs stock media for ads, explainers, social content, presentations, or any workflow where a video should be visually screened before selection.
---

# Stock Media

Use the Docker development CLI below to discover and fetch Pexels videos. Do not use a host-installed executable or host keyring:

```bash
CLI="docker compose run --rm --service-ports stock-media"
```

Treat the generated 4×4 frame grid as a compact visual storyboard: inspect it with image viewing tools to understand the clip's subject, composition, lighting, camera movement, and temporal changes before committing to the video.

## Workflow

1. Search for candidates.
2. Select a small shortlist based on duration, aspect ratio, resolution, and likely fit.
3. Download candidates at a practical resolution.
4. Generate a 16-frame grid for each candidate.
5. View the grid and assess the sequence, not just one still frame.
6. Return the chosen local video, grid, Pexels source URL, and creator attribution when available.

To install the latest version directly from GitHub, run:

```bash
pip install --upgrade "git+https://github.com/tanaka-mambinge/stock-media-cli.git@main"
```

The CLI stores the Pexels API key in the operating system credential store. The
CLI does not read API keys from environment variables or `.env` files.

If the Pexels key is missing, run the requested `${CLI} search` or
`${CLI} download` command. The CLI starts a temporary loopback setup page,
prints a one-time `http://127.0.0.1:3232/setup?...` link, and waits for the user to submit
the key in their browser. Show that link to the user exactly as printed. Do not
ask the user to send the key in chat or tell them to type it into the terminal.
After the user submits the form, the CLI stores the key in the OS credential
store and retries the original operation. If the provider rejects the key, the
same page reopens so the user can replace it without restarting the workflow.

If the user explicitly asks to revoke credentials, use the Docker CLI:

```bash
${CLI} keys revoke --platform pexels
${CLI} keys revoke --all
```

Never revoke keys without an explicit user request.

## Search

Search output is JSON and should be saved or piped into a parser rather than treated as prose:

```bash
${CLI} search "modern city skyline business" --per-page 10
${CLI} search "abstract technology background" --orientation landscape --size large --per-page 10
${CLI} search "red cars" --media-type image --per-page 10
```

Use `--media-type image` for Pexels photo metadata. Image downloading is not
currently supported; downloads remain video-only.

Useful search terms describe both the subject and intended use. For corporate footage, try `modern city skyline business`, `downtown office buildings`, `business district aerial`, or `technology office exterior`.

Prefer landscape clips for standard ads and presentations. Prefer portrait only when the output is explicitly for short-form vertical video. For an initial shortlist, favor clips around 10–30 seconds, 1920×1080 or larger, and motion that leaves usable negative space for text overlays.

## Download

Download to `./media` by default, or use a directory for generated filenames and a `.mp4` path for an exact filename:

```bash
${CLI} download 6950318 --quality hd --width 1920
${CLI} download 6950318 --quality hd --width 1920 --output ./media/candidates
${CLI} download 6950318 --output ./media/city-skyline.mp4
```

The command returns JSON containing the local path, dimensions, byte count, and Pexels source URL. Use `--width 1920` for a practical preview unless the final production needs 4K.

## Generate and Inspect the Visual Grid

Generate a 4×4 JPEG contact sheet from 16 representative frames:

```bash
${CLI} grid ./media/pexels-6950318.mp4
${CLI} grid ./media/pexels-6950318.mp4 --output ./media/skyline-grid.jpg
```

If no output path is given, the grid is written beside the video as `<video-stem>-grid.jpg`. Use the image viewer on that JPEG. Read it left-to-right, top-to-bottom as a storyboard:

- Check whether the subject stays in frame or is lost during camera movement.
- Check whether the clip has a clean opening and closing frame.
- Look for changes in light, focus, traffic, people, or objects that affect ad suitability.
- Identify negative space for headlines, logos, subtitles, and calls to action.
- Reject clips whose grid reveals distracting cuts, blur, watermarks, shaky motion, or unusable framing.

The grid is a visual preview, not a replacement for full playback. When timing, readable text, lip sync, or a specific transition matters, inspect the actual video as well.

## Reporting the Selection

Return:

- the selected video's absolute local path;
- the grid's absolute local path;
- the Pexels source URL and creator information from the search response when available;
- a short reason covering visual fit, aspect ratio, duration, resolution, motion, and text-overlay suitability.

Do not claim that a grid proves the full video is suitable. Mention any remaining uncertainty that requires playback.
