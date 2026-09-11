# Binary-first distribution

Use Go for the companion CLI so normal users receive one executable rather than installing npm, PyPI, Go, Python, or system packages.

Build with `CGO_ENABLED=0`, `-trimpath`, and release metadata embedded through linker flags. Publish these targets unless the product has a documented exception:

```text
linux_amd64
linux_arm64
darwin_amd64
darwin_arm64
windows_amd64.exe
windows_arm64.exe
```

Each release must contain matching SHA-256 checksums. The plugin skill should:

1. Detect `GOOS` and `GOARCH` without asking the user to choose.
2. Resolve a pinned plugin version or release, not an arbitrary untrusted URL.
3. Download the matching asset and checksum file.
4. Verify the checksum before execution.
5. Store the executable in a plugin-specific cache directory.
6. Reuse the verified cached binary for the rest of the task.

The CLI should provide:

- `version` for diagnostics;
- human-readable output by default;
- stable normalized JSON with `--json`;
- non-zero exit codes for authentication, validation, network, rate-limit, and server failures;
- redacted errors that never include credentials or authorization headers.

