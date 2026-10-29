#!/usr/bin/env python3
"""Transcribe one audio file to timestamped JSON."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request


MODEL_NAME = "whisper-large-v3-turbo-Q8_0.gguf"
MODEL_URL = (
    "https://huggingface.co/handy-computer/whisper-large-v3-turbo-gguf/"
    f"resolve/main/{MODEL_NAME}"
)
RUNTIME_COMMIT = "0a264781e0ca6fa67a6131371aae4fc3cd19dbe2"
SUPPORTED = {
    ".aac", ".aif", ".aiff", ".flac", ".m4a", ".mkv", ".mov", ".mp3",
    ".mp4", ".ogg", ".opus", ".wav", ".webm", ".wma",
}
VOWELS = frozenset("aeiou")


def cache_dir() -> Path:
    override = os.environ.get("VIDEO_PRODUCTION_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    root = Path(os.environ.get("XDG_CACHE_HOME") or "~/.cache").expanduser()
    return root / "video-production"


def model_path(cache: Path | None = None) -> Path:
    return (cache or cache_dir()) / "models" / MODEL_NAME


def runtime_path(cache: Path | None = None) -> Path:
    override = os.environ.get("VIDEO_PRODUCTION_TRANSCRIBE_CLI")
    if override:
        return Path(override).expanduser()
    build_bin = (cache or cache_dir()) / "transcribe.cpp" / "build" / "bin"
    for name in ("transcribe-cli", "transcribe-cli.exe"):
        for candidate in (build_bin / name, build_bin / "Release" / name):
            if candidate.is_file():
                return candidate
    installed = shutil.which("transcribe-cli")
    if installed:
        return Path(installed)
    return build_bin / ("transcribe-cli.exe" if os.name == "nt" else "transcribe-cli")


def ensure_model(path: Path) -> Path:
    if path.is_file() and path.stat().st_size > 0:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    print(f"Whisper model is missing; downloading {MODEL_NAME} (about 886 MB).", file=sys.stderr)
    request = urllib.request.Request(MODEL_URL, headers={"User-Agent": "video-production-skill"})
    try:
        with urllib.request.urlopen(request) as response, partial.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
        if partial.stat().st_size == 0:
            raise RuntimeError("Model download returned an empty file")
        partial.replace(path)
    except Exception:
        partial.unlink(missing_ok=True)
        raise
    return path


def _vowel_weight(token: str) -> int:
    normalized = unicodedata.normalize("NFKD", token.casefold())
    count = sum(char in VOWELS for char in normalized if not unicodedata.combining(char))
    return max(count, 1)


def estimate_word_timestamps(text: str, start_ms: int, end_ms: int) -> list[dict[str, object]]:
    """Apportion a Whisper segment across words by vowel count; timings are estimates."""
    tokens = text.split()
    if not tokens:
        return []

    # Keep punctuation attached to its word. If a punctuation-only token appears,
    # fold it into the preceding token (or the next one when it starts the segment).
    words: list[str] = []
    pending_prefix = ""
    for token in tokens:
        if not any(char.isalnum() for char in token):
            if words:
                words[-1] += token
            else:
                pending_prefix += token
            continue
        words.append(pending_prefix + token)
        pending_prefix = ""
    if pending_prefix:
        if words:
            words[-1] += pending_prefix
        else:
            words.append(pending_prefix)
    if not words:
        return []

    weights = [_vowel_weight(word) for word in words]
    total_weight = sum(weights)
    duration_ms = max(end_ms - start_ms, 0)
    result: list[dict[str, object]] = []
    elapsed_weight = 0
    cursor_ms = start_ms
    for index, (word, weight) in enumerate(zip(words, weights)):
        elapsed_weight += weight
        next_ms = end_ms if index == len(words) - 1 else start_ms + round(duration_ms * elapsed_weight / total_weight)
        result.append({
            "text": word,
            "start": round(cursor_ms / 1000, 3),
            "end": round(next_ms / 1000, 3),
            "start_ms": cursor_ms,
            "end_ms": next_ms,
            "estimated": True,
        })
        cursor_ms = next_ms
    return result


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transcribe one audio file and print timestamped JSON to stdout."
    )
    parser.add_argument("audio", type=Path, help="Audio file to transcribe")
    parser.add_argument("-o", "--output", type=Path, help="Save JSON to this path instead of stdout")
    parser.add_argument("--language", help="Language code such as en; omit for automatic detection")
    args = parser.parse_args()

    audio = args.audio.expanduser().resolve()
    if not audio.is_file():
        parser.error(f"Audio file not found: {audio}")
    if audio.suffix.lower() not in SUPPORTED:
        parser.error(f"Unsupported audio format: {audio.suffix or '(no extension)'}")
    cli = runtime_path()
    if not cli.is_file():
        setup = Path(__file__).with_name("setup-transcriber.py")
        parser.error(f"Transcription runtime is missing. Run: {setup}")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        parser.error("ffmpeg is required to convert audio to 16 kHz mono WAV.")

    try:
        model = ensure_model(model_path())
        with tempfile.TemporaryDirectory(prefix="video-transcribe-") as temp_dir:
            temp_path = Path(temp_dir)
            print(f"Preparing {audio.name}…", file=sys.stderr, flush=True)
            wav = temp_path / "audio.wav"
            run([ffmpeg, "-nostdin", "-v", "error", "-y", "-i", str(audio),
                 "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])
            batch = temp_path / "input.list"
            batch.write_text(f"{wav}\n", encoding="utf-8")
            command = [str(cli), "-m", str(model), "--batch", str(batch),
                       "--batch-jsonl", "--timestamps", "segment", "-q"]
            if args.language:
                command.extend(["--language", args.language])
            print("Transcribing…", file=sys.stderr, flush=True)
            result = run(command)
            rows = [
                row for line in result.stdout.splitlines() if line.strip()
                for row in [json.loads(line)] if row.get("type") != "batch_header"
            ]
            if len(rows) != 1:
                raise RuntimeError(f"Runtime returned {len(rows)} results for one input file")

        row = rows[0]
        if row.get("error"):
            raise RuntimeError(f"Failed to transcribe {audio.name}: {row['error']}")
        segments = []
        for segment in row.get("segments", []):
            start_ms = int(segment["t0_ms"])
            end_ms = int(segment["t1_ms"])
            text = segment.get("text", "").strip()
            normalized = {
                "start": round(start_ms / 1000, 3),
                "end": round(end_ms / 1000, 3),
                "start_ms": start_ms,
                "end_ms": end_ms,
                "text": text,
                "words": estimate_word_timestamps(text, start_ms, end_ms),
            }
            if "speaker_id" in segment:
                normalized["speaker_id"] = segment["speaker_id"]
            segments.append(normalized)

        document = {
            "source": str(audio),
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "language": args.language or "auto",
            "model": {
                "name": "Whisper large-v3-turbo",
                "file": model.name,
                "quantization": "Q8_0",
                "runtime": "transcribe.cpp",
                "runtime_commit": RUNTIME_COMMIT,
            },
            "word_timing": {
                "kind": "estimated",
                "method": "vowel-weighted within Whisper segment timestamps",
            },
            "text": row.get("text", "").strip(),
            "segments": segments,
        }
        if row.get("raw_text"):
            document["raw_text"] = row["raw_text"]

        encoded = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            output_path = args.output.expanduser()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(encoded, encoding="utf-8")
            print(f"Saved {output_path}", file=sys.stderr)
        else:
            sys.stdout.write(encoded)
        return 0
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, KeyError, RuntimeError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
        print(f"Transcription failed: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
