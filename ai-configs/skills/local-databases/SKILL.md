---
name: local-databases
description: Connect to the local MariaDB and MongoDB services, and use Mailpit for development email.
---

# Local Databases and Email

Use these local services when developing or testing applications:

- **MongoDB:** `127.0.0.1:27017`; connect without authentication.
- **MariaDB:** `127.0.0.1:3306`; username `user`, password `password`.
- **Mailpit:** send test email through SMTP at `127.0.0.1:1025` and view captured messages at `http://127.0.0.1:8025`.

Use the database driver and connection method that fit the project. Keep database and email traffic on these local development services.
