#!/usr/bin/env python3
"""Prepare the transcribe.cpp runtime in the user's video-production cache."""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import urllib.request


RUNTIME_COMMIT = "0a264781e0ca6fa67a6131371aae4fc3cd19dbe2"


def cache_dir() -> Path:
    override = os.environ.get("VIDEO_PRODUCTION_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    root = Path(os.environ.get("XDG_CACHE_HOME") or "~/.cache").expanduser()
    return root / "video-production"


def runtime_candidates(build_dir: Path) -> list[Path]:
    binary_names = ("transcribe-cli.exe", "transcribe-cli")
    bin_dir = build_dir / "bin"
    return [
        candidate
        for name in binary_names
        for candidate in (bin_dir / name, bin_dir / "Release" / name)
    ]


def download_source_archive(archive_path: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    partial = archive_path.with_suffix(archive_path.suffix + ".part")
    url = f"https://codeload.github.com/handy-computer/transcribe.cpp/tar.gz/{RUNTIME_COMMIT}"
    request = urllib.request.Request(url, headers={"User-Agent": "video-production-skill"})
    try:
        with urllib.request.urlopen(request) as response, partial.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
        if partial.stat().st_size == 0:
            raise RuntimeError("Runtime source download returned an empty file")
        partial.replace(archive_path)
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def extract_source(archive_path: Path, source_dir: Path) -> None:
    staging = source_dir.with_name(source_dir.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    try:
        with tarfile.open(archive_path, "r:gz") as archive:
            members = archive.getmembers()
            roots = {PurePosixPath(member.name).parts[0] for member in members if member.name}
            if len(roots) != 1:
                raise RuntimeError("Runtime source archive has an unexpected directory layout")
            root_name = next(iter(roots))
            selected = []
            for member in members:
                member_path = PurePosixPath(member.name)
                relative = member_path.relative_to(root_name)
                if relative.is_absolute() or ".." in relative.parts:
                    raise RuntimeError(f"Unsafe path in runtime source archive: {member.name}")
                if member.issym() or member.islnk():
                    link_path = PurePosixPath(member.linkname)
                    if link_path.is_absolute() or ".." in link_path.parts:
                        raise RuntimeError(f"Unsafe link in runtime source archive: {member.name}")
                member.name = str(relative)
                selected.append(member)
            archive.extractall(staging, members=selected)
        if source_dir.exists():
            shutil.rmtree(source_dir)
        staging.replace(source_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> int:
    cache = cache_dir()
    runtime_root = cache / "transcribe.cpp"
    source_dir = runtime_root / "source"
    build_dir = runtime_root / "build"
    candidates = runtime_candidates(build_dir)
    for candidate in candidates:
        if candidate.is_file():
            print(f"Transcription runtime is ready: {candidate}")
            return 0

    legacy_cli = (
        Path.home() / "Code" / "videos" / "tools" / "transcribe.cpp" / "build" / "bin"
        / ("transcribe-cli.exe" if os.name == "nt" else "transcribe-cli")
    )
    cache_bin = build_dir / "bin"
    cache_bin.mkdir(parents=True, exist_ok=True)
    if legacy_cli.is_file():
        destination = cache_bin / legacy_cli.name
        shutil.copy2(legacy_cli, destination)
        print(f"Copied the existing transcription runtime to: {destination}")
        return 0

    archive_path = cache / "tmp" / f"transcribe.cpp-{RUNTIME_COMMIT}.tar.gz"
    if not archive_path.is_file() or archive_path.stat().st_size == 0:
        print("Downloading transcribe.cpp source (no model is downloaded by setup).", file=sys.stderr)
        download_source_archive(archive_path)
    if not (source_dir / "CMakeLists.txt").is_file():
        extract_source(archive_path, source_dir)

    cmake = shutil.which("cmake")
    if not cmake:
        raise RuntimeError("CMake is required to build the transcription runtime.")
    subprocess.run([
        cmake, "-S", str(source_dir), "-B", str(build_dir),
        "-DTRANSCRIBE_VULKAN=OFF", "-DCMAKE_BUILD_TYPE=Release",
    ], check=True)
    jobs = os.environ.get("BUILD_JOBS", str(os.cpu_count() or 4))
    subprocess.run([
        cmake, "--build", str(build_dir), "--config", "Release",
        "--target", "transcribe-cli", "--parallel", jobs,
    ], check=True)
    for candidate in runtime_candidates(build_dir):
        if candidate.is_file():
            print(f"Transcription runtime is ready: {candidate}")
            return 0
    raise RuntimeError("Build completed but transcribe-cli was not found in the build output.")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError, tarfile.TarError, RuntimeError) as exc:
        print(f"Transcription runtime setup failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
