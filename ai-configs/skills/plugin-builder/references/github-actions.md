# GitHub Actions and releases

Use separate workflows for validation and publishing.

## Pull requests and branch pushes

Run on pull requests and the default branch:

- manifest validation;
- Go formatting check;
- `go test ./...`;
- `go vet ./...`;
- cross-platform compilation;
- secret/log redaction checks;
- `git diff --check` where applicable.

## Releases

Run on tags matching `vX.Y.Z`:

1. Check that the tag version matches `.codex-plugin/plugin.json`.
2. Run the complete test suite.
3. Build all supported binaries.
4. Generate checksums.
5. Publish a GitHub Release with the binaries and checksums.

Use `GITHUB_TOKEN` or repository Actions secrets only inside the workflow. Do not assume that a local commit triggers Actions: the commit must reach GitHub, and a release workflow requires the matching tag event.

After publishing, verify the actual remote repository and release assets. A successful local build is not proof that the marketplace can install the plugin.

