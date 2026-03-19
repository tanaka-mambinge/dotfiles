---
name: react-data-fetching
description: Patterns for implementing data fetching in React applications (web and mobile) using SWR.
compatibility: opencode
---

# React Data Fetching with SWR

## Architecture Principles

**Component → SWR Hook → Fetcher → API Endpoint → Response**

- **SWR Hooks**: Handle data fetching, caching, and revalidation
- **Fetcher Utility**: Centralized API request handlerv
- **Type Safety**: TypeScript generics for response types
- **State Management**: Loading, error, and data states handled automatically

## Data Flow Pattern

**Component Mount → SWR Request → Fetcher Call → API Response → Component Update**

---

## File Structure

```
lib/
├── fetcher.ts        # SWR fetcher utility
└── api.ts            # API configuration
hooks/
└── useProducts.ts    # Custom SWR hooks
components/
└── ProductList.tsx   # Components using SWR
```

---

## Implementation Steps

### 1. Setup Fetcher Utility

**Location**: `./lib/fetcher.ts`

**Rules**:

- Centralize all API request logic
- Handle authentication headers
- Include error handling
- Export single fetcher function

```typescript
// ./lib/fetcher.ts (Web)
export const fetcher = async (url: string) => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) throw new Error("Failed to fetch data");
  return res.json();
};

// ./lib/fetcher.ts (React Native)
export const fetcher = (url: string) => {
  const accessToken = useAuthStore.getState().accessToken;

  return fetch(`${API_URL}${url}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }).then(res => res.json());
};
```

---

### 2. Use SWR in Components

**Location**: Component files

**Rules**:

- Import fetcher from `@/lib/fetcher`
- Use TypeScript generics for type safety
- Match API endpoint patterns: `/api/v{x}/resource`
- Handle loading and error states
- Use `mutate` for manual revalidation

```typescript
import useSWR from 'swr';
import { fetcher } from '@/lib/fetcher';

// In component
const { data, error, isLoading, mutate } = useSWR<ResponseType>(
  '/api/v1/endpoint',
  fetcher
);
```

---

### 3. Create Custom Hooks (Optional)

**Location**: `./hooks/useProducts.ts`

**Rules**:

- Wrap SWR logic in custom hooks for reusability
- Export typed hook functions
- Keep hooks focused on single data source

```typescript
// ./hooks/useProducts.ts
import useSWR from 'swr';
import { fetcher } from '@/lib/fetcher';

export function useProducts() {
  return useSWR('/api/v1/products', fetcher);
}
```
