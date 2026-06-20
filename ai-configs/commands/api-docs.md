---
description: Generate API documentation for endpoints
---

Generate API documentation for the endpoints in the routes file(s) specified.

$ARGUMENTS

The default routes file to document is: routes/company_profile.py

If you want to document different routes, specify them as arguments, e.g.:
"routes/cars.py routes/auth.py"
or "all" to document all endpoints in the routes/ directory

For each endpoint, provide the following in markdown format:

### {HTTP_METHOD} {endpoint_path}

**Description:** Brief description of what the endpoint does

**Headers:** Required headers (e.g., Authorization, Content-Type)

**Payload:** Request body structure (if applicable)

```json
{
  // field: description (type)
}
```

**Response on Success:**

```json
{
  // field: description
}
```

**Response on Errors:**

```json
{
  "detail": "Error message"
}
```

**Notes:** Any additional important information (auth required, file upload notes, etc.)

Group endpoints by route file. Use @ routes/{filename} to read the route file content.
