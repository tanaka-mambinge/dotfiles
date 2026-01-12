---
name: fastapi-route
description: Coding standards and best practices for building FastAPI routes.
compatibility: opencode
---

# FastAPI Route Organization & Coding Practices

## Architecture Principles

**Request Flow: HTTP → Route Handler → Service Layer → Database → Response**

- **Route Handlers**: Handle HTTP concerns only (request parsing, status codes, error formatting)
- **Service Classes**: Contain business logic and database operations (static methods with full type hints)
- **Pydantic Models**: Request/response structure and basic validation
- **Marshmallow Schemas**: Complex validation logic and business rule validation

## Data Flow Pattern

**Incoming Request → Pydantic DTO → Marshmallow Schema Validation → Service Method → Untyped Response**

---

## File Structure

```
project/
├── routes/
│   ├── __init__.py
│   ├── users.py
│   └── products.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── product_service.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
└── main.py
```

---

## Implementation Steps

### 1. Service Layer (Business Logic)

**Location**: `./services/{domain}_service.py`

**Rules**:

- Use static methods exclusively
- Always include complete type hints
- Handle all database operations
- Return typed objects (`Model`, `Model | None`, `list[Model]`)

```python
# ./services/user_service.py
from sqlmodel import select, Session
from models.user import User
from utils.db import get_session

class UserService:    
    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        """Retrieve user by ID or None if not found."""
        with get_session() as session:
            statement = select(User).where(User.id == user_id)
            return session.exec(statement).first()
```

---

### 2. Validation Schemas (Business Rules)

**Location**: `./schemas/{domain}.py`

**Rules**:

- Use Marshmallow for ALL validation
- Include custom validators for business rules
- Reference service layer for existence checks

```python
# ./schemas/user.py
from marshmallow import Schema, fields, validates, ValidationError
from services.user_service import UserService

class CreateUserRequestSchema(Schema):
    """Validation schema for user registration."""
    
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format."
        }
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required."}
    )
    
    @validates("email")
    def validate_unique_email(self, value: str) -> None:
        """Ensure email is not already registered."""
        if UserService.check_email_exists(value):
            raise ValidationError("This email is already registered.")
```

---

### 3. Route Handlers (HTTP Layer)

**Location**: `./routes/{domain}.py`

**Rules**:

- Keep handlers thin (delegation only)
- Use Pydantic models for request structure
- Call Marshmallow schemas for validation
- Delegate all logic to services
- Return untyped responses (dicts or ORM objects)
- Always use `/api/v{version}` prefix

```python
# ./routes/users.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from marshmallow import ValidationError
from schemas.user import CreateUserRequestSchema
from services.user_service import UserService

router = APIRouter(prefix="/api/v1", tags=["users"])

# Pydantic DTOs for request structure
class CreateUserRequestDto(BaseModel):
    """Request model for user registration."""
    email: str
    password: str

# Route handlers
@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_req: CreateUserRequestDto):
    """
    Register a new user account.
    """
    schema = CreateUserRequestSchema()
    
    # Validate with Marshmallow
    try:
        schema.load(user_req.model_dump())
    except ValidationError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.messages
        )
    
    # Delegate to service
    new_user = UserService.create_user(
        email=user_req.email,
        password=user_req.password
    )
    
    return new_user
```

---

### 4. Application Registration

**Location**: `./main.py`

```python
# ./main.py
from fastapi import FastAPI
from routes import users, products

app = FastAPI(
    title="My API",
    description="API with clean architecture",
    version="1.0.0"
)

# Register routers
app.include_router(users.router)
app.include_router(products.router)
```
