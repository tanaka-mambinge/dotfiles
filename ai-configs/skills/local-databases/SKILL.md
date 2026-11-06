---
name: local-databases
description: Connect to local MariaDB, MongoDB, Typesense, and Mailpit development services.
---

# Local Databases and Email

Use these local services when developing or testing applications:

- **MongoDB:** `127.0.0.1:27017`; connect without authentication.
- **MariaDB:** `127.0.0.1:3306`; username `user`, password `password`.
- **Typesense:** `127.0.0.1:8108`; check readiness at `http://127.0.0.1:8108/health`. Search credentials belong in the server's secret configuration, never in client code or logs.
- **Mailpit:** send test email through SMTP at `127.0.0.1:1025` and view captured messages at `http://127.0.0.1:8025`.

Use the database driver and connection method that fit the project. Keep database and email traffic on these local development services.

## Typesense service

Check whether the packaged service is running with `systemctl is-active typesense-server.service`; start it with `sudo systemctl start typesense-server.service` when needed. For Debian and Ubuntu installs, the service configuration and generated admin key are in `/etc/typesense/typesense-server.ini`. Do not print the key or copy it into source files.

If the Linux binary is missing, use the official [Typesense downloads page](https://typesense.org/downloads/) to select the current x64 or ARM64 archive. For example, the x64 archive can be downloaded and extracted with:

```sh
mkdir -p ./tmp/typesense
cd ./tmp/typesense
wget https://dl.typesense.org/releases/30.2/typesense-server-30.2-linux-amd64.tar.gz
tar -xzf typesense-server-30.2-linux-amd64.tar.gz
```

Follow the official [Linux installation guide](https://typesense.org/docs/guide/install-typesense.html) to set a persistent data directory, API key, and port, then start the binary. Use port `8108` for Yonda development.

## Yonda development

From the repository root, start the API and web frontend together with `npm run dev`. Do not launch either service separately.
