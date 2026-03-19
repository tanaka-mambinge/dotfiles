---
name: fastapi-database-seeding
description: Standards for creating database seeders for FastAPI applications using SQLModel. Use when creating seeders to populate initial or test data.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  framework: fastapi
  orm: sqlmodel
---

# FastAPI Database Seeding Standards

Guidelines for creating database seeders in FastAPI applications. Seeders populate the database with initial or test data for development, testing, or production environments.

## File Structure

```
./seeders/
├── base_seeder.py          # Base class (already implemented)
├── run_seeders.py          # Seeder registry and CLI runner
├── user_seeder.py          # Individual seeder files
├── product_seeder.py
└── ...
```

## Base Seeder

The `BaseSeed` class (in `./seeders/base_seeder.py`) provides:

- Database session management via `self.session`
- Transaction handling (auto-commit on success, rollback on error)
- Error management and reporting

**All seeders must inherit from `BaseSeed`.**

## Seeder Implementation Pattern

### Step 1: Create Seeder Class

Create a new file in `./seeders/` directory:

```python
# ./seeders/user_seeder.py
from sqlmodel import select
from models.user import User
from seeders.base_seeder import BaseSeed
from utils.auth import get_password_hash
from datetime import datetime, timezone

class UserSeeder(BaseSeed):
    def seed(self):
        """Seed initial user data"""
        
        # Define seed data
        users_data = [
            {
                "email": "admin@example.com",
                "username": "admin",
                "password": "admin123",
                "is_admin": True,
            },
            {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
                "is_admin": False,
            },
        ]
        
        # Seed each user
        for user_data in users_data:
            # Check if user already exists (idempotent)
            existing_user = self.session.exec(
                select(User).where(User.email == user_data["email"])
            ).first()
            
            if existing_user:
                print(f"  - User '{user_data['email']}' already exists, skipping")
                continue
            
            # Create new user
            new_user = User(
                email=user_data["email"],
                username=user_data["username"],
                password_hash=get_password_hash(user_data["password"]),
                is_admin=user_data.get("is_admin", False),
                verified_at=datetime.now(timezone.utc),
            )
            self.session.add(new_user)
            print(f"  - Created user: {user_data['email']}")
```

### Step 2: Register Seeder

Add the seeder to `./seeders/run_seeders.py`:

```python
# ./seeders/run_seeders.py
from .user_seeder import UserSeeder
from .product_seeder import ProductSeeder
from .category_seeder import CategorySeeder

# Order matters - dependencies should come first
SEEDERS = {
    "users": UserSeeder,
    "categories": CategorySeeder,  # Must run before products
    "products": ProductSeeder,     # Depends on categories
}

# ... rest of run_seeders.py remains the same
```

**CRITICAL**: The order in the `SEEDERS` dictionary determines execution order. Place seeders with dependencies later in the dictionary.

### Step 3: Run Seeder

```bash
# Run specific seeder
python -m seeders.run_seeders users

# Run multiple seeders
python -m seeders.run_seeders users products

# Run all seeders in order
python -m seeders.run_seeders all
```

## Key Principles

### Idempotent Seeders

Always check if data exists before creating to allow re-running seeders:

```python
def seed(self):
    # Check for existing record
    existing = self.session.exec(
        select(Model).where(Model.unique_field == value)
    ).first()
    
    if existing:
        print("  - Record already exists, skipping")
        return
    
    # Create new record
    new_record = Model(...)
    self.session.add(new_record)
    print("  - Created record")
```

### Print Progress Messages

Use `print()` statements to show progress:

```python
def seed(self):
    print("  - Creating admin user...")
    # ...
    print("  - Created 5 products")
    print("  - Skipped 2 existing categories")
```

**Message Guidelines:**

- Start with `"  - "` (two spaces, dash, space) for consistency
- Be specific about what was created or skipped
- Include counts for batch operations

### Database Session

Use `self.session` for all database operations:

```python
def seed(self):
    # Query
    user = self.session.exec(select(User).where(User.id == 1)).first()
    
    # Add single record
    self.session.add(new_record)
    
    # Add multiple records (efficient for bulk)
    self.session.add_all([record1, record2, record3])
    
    # Flush to get IDs (when needed for relationships)
    self.session.flush()
    
    # No need to commit - BaseSeed handles this automatically
```

**Do NOT call `self.session.commit()`** - the base class handles commits and rollbacks.

### Getting IDs for Related Records

Use `session.flush()` when you need IDs immediately for foreign key relationships:

```python
def seed(self):
    # Create parent
    category = Category(name="Electronics")
    self.session.add(category)
    self.session.flush()  # Get category.id
    
    # Use parent ID in child
    product = Product(
        name="Laptop",
        category_id=category.id  # Now available
    )
    self.session.add(product)
    print(f"  - Created product in category {category.id}")
```

## Data Sources

### Hardcoded Data

Best for small, static datasets:

```python
def seed(self):
    roles = ["admin", "editor", "viewer"]
    
    for role_name in roles:
        existing = self.session.exec(
            select(Role).where(Role.name == role_name)
        ).first()
        
        if not existing:
            self.session.add(Role(name=role_name))
            print(f"  - Created role: {role_name}")
```

### Structured Data

For larger datasets, use structured data:

```python
def seed(self):
    products_data = [
        {"name": "Laptop", "price": 999.99, "sku": "LAP001"},
        {"name": "Mouse", "price": 29.99, "sku": "MOU001"},
        {"name": "Keyboard", "price": 79.99, "sku": "KEY001"},
    ]
    
    for product_data in products_data:
        existing = self.session.exec(
            select(Product).where(Product.sku == product_data["sku"])
        ).first()
        
        if not existing:
            self.session.add(Product(**product_data))
            print(f"  - Created product: {product_data['name']}")
```
