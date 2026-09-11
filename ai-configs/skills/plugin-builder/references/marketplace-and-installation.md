# Marketplace and installation

Keep the plugin repository and marketplace repository conceptually separate.

## Standalone plugin

The plugin repository itself contains `.codex-plugin/plugin.json` at its root and can be installed directly from GitHub. Do not require a parent repository or a nested source path.

## Marketplace collection

A marketplace collection may contain a root marketplace manifest that lists independent plugin repositories. Each entry must use the marketplace's supported direct-repository source form. Do not use `git-subdir` for a plugin that has its own repository.

## Verification checklist

Before saying installation works:

1. Confirm the manifest exists in the remote branch, not only locally.
2. Confirm the marketplace entry name exactly matches the plugin manifest name and install command.
3. Confirm the referenced branch and repository are public or authenticated as intended.
4. Refresh or re-add the marketplace after changing its manifest.
5. Test installation from the remote source, not only from a local checkout.
6. Check that the release assets match the current plugin version.

If installation fails, report the exact layer that failed: marketplace discovery, manifest parsing, source checkout, binary download, authentication, or runtime API access.

