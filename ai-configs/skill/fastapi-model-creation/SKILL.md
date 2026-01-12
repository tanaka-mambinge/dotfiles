---
name: fastapi-model-creation
description: Standards for creating SQLModel database models for FastAPI applications. Use when creating or modifying database models, tables, or ORM entities.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  framework: fastapi
  orm: sqlmodel
---

# FastAPI Database Model Creation Standards

Guidelines for creating database models in FastAPI applications using SQLModel. All models follow consistent patterns for maintainability and type safety.

## File Structure

- **Location**: `./models/` directory at project root
- **Naming**: Snake case `.py` files matching the model name (e.g., `user.py`, `blog_post.py`)
- **Registration**: Always export new models in `./models/__init__.py`

## Base Model Features

All models must inherit from `BaseModelMixin`, which automatically provides:

- `id`: Primary key (auto-incrementing integer)
- `created_at`: Timestamp of record creation
- `updated_at`: Timestamp of last update

**Never redefine these fields in your models.**

## Basic Model Pattern

```python
# ./models/user.py
from sqlmodel import Field, Relationship
from models.mixins import BaseModelMixin

# Prevent circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.post import Post

class User(BaseModelMixin, table=True):
    __tablename__ = "users"
    
    # Fields
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(nullable=False)
    disabled: bool = Field(default=False)
    
    # Relationships
    posts: list["Post"] = Relationship(back_populates="author")
```

## Key Conventions

### Table Names

- Always specify `__tablename__` explicitly
- Use snake_case, plural form (e.g., `"users"`, `"blog_posts"`, `"order_items"`)

### Inheritance

```python
class ModelName(BaseModelMixin, table=True):
    # Always inherit from BaseModelMixin first
    # Always specify table=True for database-mapped models
```

**Field Guidelines:**

- Always explicitly set `nullable=False` for required fields
- Add `index=True` for frequently queried fields (foreign keys, lookup fields)
- Use `unique=True` in Field definition for unique constraints
- Set `default=` or `default_factory=` for fields with default values
- Specify `max_length` for string fields where appropriate

### Foreign Keys

```python
# Foreign key definition
author_id: int = Field(foreign_key="users.id", nullable=False)

# Optional foreign key
reviewer_id: int | None = Field(foreign_key="users.id", nullable=True, default=None)
```

**Foreign Key Guidelines:**

- Reference the table name and column: `foreign_key="table_name.id"`
- Add `index=True` for foreign keys (good practice for joins)
- Set `nullable=False` for required relationships

### Circular Import Prevention

Always use this pattern for related models:

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.post import Post
    from models.comment import Comment
```

This allows type checking without runtime circular imports.

## Enum Fields

Define enums as classes inheriting from `str` and `Enum`:

```python
from enum import Enum
from sqlmodel import Field
from models.mixins import BaseModelMixin

class UserType(str, Enum):
    NORMAL = "normal"
    ADMIN = "admin"

class User(BaseModelMixin, table=True):
    __tablename__ = "users"
    
    username: str = Field(nullable=False)
    user_type: UserType = Field(default=UserType.NORMAL, nullable=False)
```

**Enum Guidelines:**

- Always inherit from both `str` and `Enum`
- Use UPPERCASE for enum member names
- Use lowercase strings for values
- Define enums in the same file as the model or in a shared `enums.py`

## Soft Deletes

Add soft delete fields on a per-model basis when needed:

```python
from datetime import datetime

class User(BaseModelMixin, table=True):
    __tablename__ = "users"
    
    username: str = Field(nullable=False)
    
    # Soft delete field
    deleted_at: datetime | None = Field(default=None, nullable=True)
```

**Soft Delete Guidelines:**

- Use `deleted_at: datetime | None` field
- Set `default=None, nullable=True`
- Only add to models that require soft deletes (not all models need this)
- Filter queries to exclude deleted records: `WHERE deleted_at IS NULL`
