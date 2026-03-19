---
name: react-form-validation
description: Patterns for implementing form validation in React applications using react-hook-form and Yup.
compatibility: opencode
---

# React Form Validation with react-hook-form and Yup

## Architecture Principles

**Schema Definition → Hook Setup → Uncontrolled Components → Validation → Submission**

- **Yup Schemas**: Define validation rules and error messages
- **react-hook-form**: Handle form state and validation integration
- **Uncontrolled Components**: Use refs instead of controlled state
- **Type Safety**: TypeScript inference from Yup schemas
- **Error Display**: Automatic error message handling

## Data Flow Pattern

**User Input → Field Blur/Submit → Yup Validation → Error Display → Form Submission**

---

## File Structure

```
schemas/
├── auth.schema.ts      # Authentication form schemas
└── product.schema.ts   # Product form schemas
components/
├── TextField.tsx       # Reusable form input component
└── LoginForm.tsx       # Form components
types/
└── forms.ts           # Inferred form types
```

---

## Implementation Steps

### 1. Define Yup Schema

**Location**: `./schemas/{feature}.schema.ts`

**Rules**:

- Group related schemas by feature
- Export schema and inferred type
- Use descriptive error messages
- Include all validation rules

```typescript
// ./schemas/auth.schema.ts
import * as yup from 'yup';

export const loginSchema = yup.object({
  email: yup
    .string()
    .email('Please enter a valid email address')
    .required('Email is required'),
  password: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required'),
});

export type LoginFormData = yup.InferType<typeof loginSchema>;
```

---

### 2. Setup Form with react-hook-form

**Location**: Component files

**Rules**:

- Use `@hookform/resolvers/yup` for schema integration
- Always use **uncontrolled components** (register, not Controller)
- Destructure only needed values from useForm
- Handle submission errors appropriately

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { loginSchema, type LoginFormData } from '@/schemas/auth.schema';

export default function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: yupResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      
      if (!response.ok) throw new Error('Login failed');
      
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

---

### 3. Create Custom Validation Rules

**Rules**:

- Use `.test()` for custom validation rules
- Reference other fields with `this.parent`
- Provide clear error messages

```typescript
// ./schemas/profile.schema.ts
import * as yup from 'yup';

export const changePasswordSchema = yup.object({
  currentPassword: yup.string().required('Current password is required'),
  newPassword: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .required('New password is required'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('newPassword')], 'Passwords must match')
    .required('Please confirm your password'),
});

export type ChangePasswordFormData = yup.InferType<typeof changePasswordSchema>;
```

---

## Common Patterns

### Handle API Validation Errors

```typescript
const onSubmit = async (data: LoginFormData) => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const error = await response.json();
      // Display API error message
      setError('root', { message: error.message });
      return;
    }
    
    // Success handling
  } catch (error) {
    setError('root', { message: 'An unexpected error occurred' });
  }
};
```

### Reset Form After Submission

```typescript
const { reset, handleSubmit } = useForm<FormData>({
  resolver: yupResolver(schema),
});

const onSubmit = async (data: FormData) => {
  // Submit data
  reset(); // Clear form
};
```

### Set Default Values

```typescript
const { register } = useForm<FormData>({
  resolver: yupResolver(schema),
  defaultValues: {
    email: '',
    newsletter: true,
  },
});
```
