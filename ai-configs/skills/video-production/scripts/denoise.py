#!/usr/bin/env python3
"""Reduce background noise with MossFormer2_SE_48K and save a WAV."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request


MODEL_NAME = "MossFormer2_SE_48K"
MODEL_FILENAME = "last_best_checkpoint.pt"
MODEL_REVISION = "eff8c97925c8bec812af707814b3e5d777fd4503"
MODEL_URL = (
    "https://huggingface.co/alibabasglab/MossFormer2_SE_48K/resolve/"
    f"{MODEL_REVISION}/{MODEL_FILENAME}"
)
MODEL_SIZE = 221_552_019
MODEL_SHA256 = "03692b9f773bbd6bb43b9c5a41f96b1e28affd66e13796b7bec66ad3d8b227c6"
MODEL_SAMPLE_RATE = 48_000
MODEL_DIRECTORY = "mossformer2-clearvoice"
RUNTIME_DIRECTORY = "mossformer-runtime"
TORCH_VERSION = "2.11.0"
TORCHVISION_VERSION = "0.26.0"
SOUNDFILE_VERSION = "0.12.1"
SOXR_VERSION = "1.1.0"
NUMPY_VERSION = "1.26.4"
SUPPORTED_EXTENSIONS = {".aif", ".aiff", ".flac", ".mp3", ".oga", ".ogg", ".wav"}
BLOCK_SIZE = 1024 * 1024


def cache_dir() -> Path:
    override = os.environ.get("VIDEO_PRODUCTION_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    root = Path(os.environ.get("XDG_CACHE_HOME") or "~/.cache").expanduser()
    return root / "video-production"


def runtime_dir() -> Path:
    return cache_dir() / RUNTIME_DIRECTORY


def runtime_python(path: Path) -> Path:
    if os.name == "nt":
        return path / "Scripts" / "python.exe"
    return path / "bin" / "python"


RUNTIME_PROBE = r"""
import numpy
import torch
import torchaudio
import soundfile
import soxr
import clearvoice

if int(numpy.__version__.split('.')[0]) >= 2:
    raise SystemExit('ClearVoice needs NumPy 1.x')
if torch.__version__.split('+')[0] != '2.11.0':
    raise SystemExit('Unexpected PyTorch runtime version')
if torchaudio.__version__.split('+')[0] != '2.11.0':
    raise SystemExit('Unexpected TorchAudio runtime version')
"""


def _probe_runtime(python: Path) -> bool:
    if not python.is_file():
        return False
    try:
        result = subprocess.run(
            [str(python), "-c", RUNTIME_PROBE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except OSError:
        return False


def _is_python_312(python: Path) -> bool:
    try:
        result = subprocess.run(
            [
                str(python), "-c",
                "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0 and result.stdout.strip() == "3.12"
    except OSError:
        return False


def _find_python_312() -> Path:
    candidates: list[Path] = [Path(sys.executable)]
    for name in ("python3.12", "python312", "python"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))

    for candidate in candidates:
        if _is_python_312(candidate):
            return candidate

    if os.name == "nt":
        launcher = shutil.which("py")
        if launcher:
            try:
                result = subprocess.run(
                    [launcher, "-3.12", "-c", "import sys; print(sys.executable)"],
                    capture_output=True,
                    check=False,
                    text=True,
                )
                candidate = Path(result.stdout.strip()) if result.returncode == 0 else None
                if candidate and _is_python_312(candidate):
                    return candidate
            except OSError:
                pass

    uv = shutil.which("uv")
    if uv:
        result = subprocess.run(
            [uv, "python", "find", "3.12"], capture_output=True, check=False, text=True
        )
        if result.returncode == 0:
            candidate = Path(result.stdout.strip())
            if _is_python_312(candidate):
                return candidate

        print(
            "Python 3.12 is missing; preparing it for the denoiser…",
            file=sys.stderr,
            flush=True,
        )
        subprocess.run([uv, "python", "install", "3.12"], check=True)
        result = subprocess.run(
            [uv, "python", "find", "3.12"], capture_output=True, check=True, text=True
        )
        candidate = Path(result.stdout.strip())
        if _is_python_312(candidate):
            return candidate

    raise RuntimeError(
        "The MossFormer denoiser needs Python 3.12. Install Python 3.12 or the uv "
        "Python manager, then run this command again."
    )


def _run_setup(command: list[str], label: str) -> None:
    print(label, file=sys.stderr, flush=True)
    subprocess.run(command, check=True)


def ensure_runtime() -> tuple[Path, bool]:
    """Return the cached Python and whether it is the current interpreter."""
    root = cache_dir()
    environment = runtime_dir()
    python = runtime_python(environment)
    is_current_runtime = Path(sys.prefix).resolve() == environment.resolve()
    if _probe_runtime(python):
        return python, is_current_runtime

    # Rebuild from the base interpreter if the current cached runtime is damaged.
    if is_current_runtime:
        base_python = Path(getattr(sys, "_base_executable", None) or sys.executable)
        return base_python, False

    root.mkdir(parents=True, exist_ok=True)
    if environment.exists():
        shutil.rmtree(environment)
    base_python = _find_python_312()
    print(
        "MossFormer audio tools are missing; preparing them in the video-production cache.",
        file=sys.stderr,
        flush=True,
    )
    try:
        subprocess.run(
            [str(base_python), "-m", "venv", "--clear", str(environment)], check=True
        )
        python = runtime_python(environment)

        pytorch = [
            f"torch=={TORCH_VERSION}",
            f"torchaudio=={TORCH_VERSION}",
            f"torchvision=={TORCHVISION_VERSION}",
        ]
        indexes = ["--index-url", "https://pypi.org/simple"]
        if (
            platform.machine().lower() in {"amd64", "x86_64"}
            and (sys.platform.startswith("linux") or os.name == "nt")
        ):
            pytorch = [
                f"torch=={TORCH_VERSION}+cpu",
                f"torchaudio=={TORCH_VERSION}+cpu",
                f"torchvision=={TORCHVISION_VERSION}+cpu",
            ]
            indexes.extend(["--extra-index-url", "https://download.pytorch.org/whl/cpu"])

        common_pip = [
            str(python), "-m", "pip", "install", "--disable-pip-version-check",
            "--no-input", "--no-cache-dir", *indexes,
        ]
        _run_setup(
            [*common_pip, *pytorch],
            "Downloading the audio model runtime…",
        )
        _run_setup(
            [
                *common_pip,
                f"numpy=={NUMPY_VERSION}",
                f"soundfile=={SOUNDFILE_VERSION}",
                f"soxr=={SOXR_VERSION}",
                "clearvoice==0.1.2",
            ],
            "Downloading MossFormer audio tools…",
        )
        if not _probe_runtime(python):
            raise RuntimeError("The downloaded MossFormer audio runtime failed its startup check.")
    except Exception:
        shutil.rmtree(environment, ignore_errors=True)
        raise
    return python, Path(sys.prefix).resolve() == environment.resolve()


def model_workdir() -> Path:
    return cache_dir() / "models" / MODEL_DIRECTORY


def checkpoint_path() -> Path:
    return model_workdir() / "checkpoints" / MODEL_NAME / MODEL_FILENAME


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(BLOCK_SIZE):
            digest.update(block)
    return digest.hexdigest()


def _model_is_ready(checkpoint: Path) -> bool:
    marker = checkpoint.parent / "last_best_checkpoint"
    if not checkpoint.is_file() or checkpoint.stat().st_size != MODEL_SIZE:
        return False
    if not marker.is_file() or marker.read_text(encoding="utf-8").strip() != MODEL_FILENAME:
        return False
    return _sha256(checkpoint) == MODEL_SHA256


def ensure_model() -> Path:
    """Download and verify the pinned MossFormer2 weights when they are missing."""
    checkpoint = checkpoint_path()
    if _model_is_ready(checkpoint):
        return checkpoint

    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    partial = checkpoint.with_suffix(checkpoint.suffix + ".part")
    offset = partial.stat().st_size if partial.is_file() else 0
    if offset >= MODEL_SIZE:
        partial.unlink(missing_ok=True)
        offset = 0

    request = urllib.request.Request(
        MODEL_URL,
        headers={"User-Agent": "video-production-skill/1.0"},
    )
    if offset:
        request.add_header("Range", f"bytes={offset}-")
    print(
        "MossFormer2 model is missing; downloading its 222 MB weights…",
        file=sys.stderr,
        flush=True,
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            append = offset > 0 and getattr(response, "status", response.getcode()) == 206
            if not append:
                offset = 0
            mode = "ab" if append else "wb"
            downloaded = offset
            next_report = downloaded + 20 * 1024 * 1024
            with partial.open(mode) as output:
                while block := response.read(BLOCK_SIZE):
                    output.write(block)
                    downloaded += len(block)
                    if downloaded >= next_report:
                        print(
                            f"Downloaded {downloaded / (1024 * 1024):.0f} MB of 222 MB…",
                            file=sys.stderr,
                            flush=True,
                        )
                        next_report = downloaded + 20 * 1024 * 1024

        if partial.stat().st_size != MODEL_SIZE:
            raise RuntimeError(
                f"MossFormer2 download is incomplete ({partial.stat().st_size} of {MODEL_SIZE} bytes)."
            )
        if _sha256(partial) != MODEL_SHA256:
            raise RuntimeError("MossFormer2 download failed its integrity check.")
        partial.replace(checkpoint)
        (checkpoint.parent / "last_best_checkpoint").write_text(
            f"{MODEL_FILENAME}\n", encoding="utf-8"
        )
    except Exception:
        # Keep a valid partial download so a later run can resume it.
        raise
    return checkpoint


def _as_frames_channels(audio, channels: int):
    import numpy as np

    result = np.asarray(audio, dtype=np.float32)
    if result.ndim == 3 and result.shape[0] == 1:
        result = result[0]
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2:
        raise RuntimeError(f"MossFormer returned an unexpected audio shape: {result.shape}")
    if result.shape[1] == channels:
        return result
    if result.shape[0] == channels:
        return result.T
    raise RuntimeError(
        f"MossFormer returned {result.shape[0]} by {result.shape[1]} samples; expected {channels} channel(s)."
    )


def denoise_audio(audio_path: Path, output_path: Path, strength: float) -> None:
    import numpy as np
    import soundfile as sf
    import soxr
    from clearvoice import ClearVoice

    audio, sample_rate = sf.read(str(audio_path), dtype="float32", always_2d=True)
    channels = audio.shape[1]
    if channels not in (1, 2):
        raise ValueError(f"MossFormer supports mono or stereo audio; this file has {channels} channels.")
    if sample_rate <= 0 or len(audio) == 0:
        raise ValueError("The audio file has no readable samples.")
    if not np.isfinite(audio).all():
        raise ValueError("The audio contains invalid sample values.")

    original_frames = len(audio)
    if sample_rate != MODEL_SAMPLE_RATE:
        audio_48k = soxr.resample(audio, sample_rate, MODEL_SAMPLE_RATE, quality="HQ")
    else:
        audio_48k = audio

    workdir = model_workdir()
    workdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="video-denoise-") as temp_dir:
        model_input = Path(temp_dir) / "audio_48k.wav"
        sf.write(model_input, audio_48k, MODEL_SAMPLE_RATE, subtype="PCM_16")

        previous_directory = Path.cwd()
        try:
            # ClearVoice reads its checkpoint path from its bundled config as a
            # relative path, so run it from the dedicated cache directory.
            os.chdir(workdir)
            clearvoice = ClearVoice(
                task="speech_enhancement", model_names=[MODEL_NAME]
            )
            result = clearvoice(input_path=str(model_input))
        finally:
            os.chdir(previous_directory)

    if isinstance(result, dict):
        if MODEL_NAME in result:
            result = result[MODEL_NAME]
        if isinstance(result, dict):
            if not result:
                raise RuntimeError("MossFormer did not return any audio.")
            result = next(iter(result.values()))
    cleaned_48k = _as_frames_channels(result, channels)
    if len(cleaned_48k) > len(audio_48k):
        cleaned_48k = cleaned_48k[:len(audio_48k)]
    elif len(cleaned_48k) < len(audio_48k):
        cleaned_48k = np.pad(cleaned_48k, ((0, len(audio_48k) - len(cleaned_48k)), (0, 0)))

    if strength < 1.0:
        cleaned_48k = audio_48k * (1.0 - strength) + cleaned_48k * strength

    if sample_rate != MODEL_SAMPLE_RATE:
        cleaned = soxr.resample(cleaned_48k, MODEL_SAMPLE_RATE, sample_rate, quality="HQ")
    else:
        cleaned = cleaned_48k
    if len(cleaned) > original_frames:
        cleaned = cleaned[:original_frames]
    elif len(cleaned) < original_frames:
        cleaned = np.pad(cleaned, ((0, original_frames - len(cleaned)), (0, 0)))
    if not np.isfinite(cleaned).all():
        raise RuntimeError("MossFormer returned invalid sample values.")

    sf.write(str(output_path), cleaned, sample_rate, format="WAV", subtype="PCM_16")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reduce background noise in one audio file and save a cleaned WAV."
    )
    parser.add_argument("audio", type=Path, help="Audio file to clean")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Output WAV path (default: <name>_denoised.wav)",
    )
    parser.add_argument(
        "--strength", type=float, default=1.0, metavar="0..1",
        help="Denoising amount: 0 keeps the original, 1 uses full MossFormer (default: 1)",
    )
    args = parser.parse_args()
    if not 0.0 <= args.strength <= 1.0:
        parser.error("--strength must be between 0 and 1")
    return args


def main() -> int:
    args = parse_args()
    audio_path = args.audio.expanduser().resolve()
    if not audio_path.is_file():
        print(f"Denoising failed: audio file not found: {audio_path}", file=sys.stderr)
        return 2
    if audio_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        formats = ", ".join(ext.lstrip(".") for ext in sorted(SUPPORTED_EXTENSIONS))
        print(
            "Denoising failed: unsupported audio format "
            f"{audio_path.suffix or '(no extension)'}. Supported formats: {formats}.",
            file=sys.stderr,
        )
        return 2

    output_path = args.output.expanduser() if args.output else audio_path.with_name(
        f"{audio_path.stem}_denoised.wav"
    )
    output_path = output_path.resolve()
    if output_path.suffix.lower() != ".wav":
        print("Denoising failed: output path must end in .wav.", file=sys.stderr)
        return 2
    if output_path == audio_path:
        print("Denoising failed: output path must be different from the input file.", file=sys.stderr)
        return 2

    try:
        python, is_current_runtime = ensure_runtime()
        if not is_current_runtime:
            command = [str(python), str(Path(__file__).resolve()), *sys.argv[1:]]
            return subprocess.run(command).returncode

        ensure_model()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            prefix=f".{output_path.stem}.", suffix=".tmp.wav", dir=output_path.parent, delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
        try:
            denoise_audio(audio_path, temporary_path, args.strength)
            temporary_path.replace(output_path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
        print(f"Saved denoised audio: {output_path}", file=sys.stderr)
        return 0
    except subprocess.CalledProcessError as exc:
        print(
            f"Denoising setup failed: command exited with status {exc.returncode}.",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        print(f"Denoising failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
