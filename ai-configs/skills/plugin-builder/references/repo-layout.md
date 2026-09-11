# Standalone repository layout

Every generated plugin is an independent repository. The plugin manifest must be at the repository root so direct repository installation does not depend on a parent monorepo.

```text
plugin-repo/
├── .codex-plugin/plugin.json
├── skills/<plugin-name>/SKILL.md
├── cmd/<binary-name>/main.go
├── internal/
│   ├── auth/
│   ├── client/
│   ├── config/
│   └── models/
├── assets/
├── .github/workflows/
│   ├── ci.yml
│   └── release.yml
├── README.md
├── LICENSE
└── go.mod
```

Do not generate this shape:

```text
parent-repository/
└── plugins/plugin-name/
```

That was the source of the Redan marketplace problem: the local checkout contained the plugin, but the remote `main` branch and marketplace source did not agree about the plugin path. A separate marketplace repository may list multiple standalone plugin repositories, but it should not be required to install one plugin.

Keep generated binaries and temporary screenshots out of Git. Use a cache directory under the user's home directory at runtime and `tmp/` only for local validation artifacts.

