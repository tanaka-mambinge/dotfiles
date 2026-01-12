---
name: react-design-implementation
description: Guidelines for implementing React components and pages from design images and descriptions.
compatibility: opencode
---

# React Design Implementation

## Overview

Create React components that match provided designs while maintaining consistency with existing codebase patterns.

## Technology Stack

### React Web Apps

- **Styling**: Tailwind CSS utility classes
- **Components**: Functional components with hooks
- **State**: useState, useContext, or state management library
- **Data Fetching**: SWR with fetcher utility

### React Native Apps

- **Styling**: NativeWind (Tailwind for React Native)
- **Components**: Functional components with hooks
- **Navigation**: React Navigation
- **Data Fetching**: SWR with fetcher utility

---

## Implementation Approach

### Step 1: Analyze Existing Components

Examine similar existing components to understand:

- **File structure** - Where components are located
- **Naming conventions** - How components are named
- **Styling patterns** - Common Tailwind/NativeWind classes used
- **Component composition** - How components are broken down
- **State management** - How data flows through the app
- **Data fetching patterns** - How SWR is used for API calls

### Step 2: Match the Design Reference

Study the provided design and identify:

- **Layout structure** - Grid, flexbox, positioning
- **Visual hierarchy** - Spacing, sizing, typography
- **Interactive elements** - Buttons, inputs, links, cards

### Step 3: Determine File Location

Follow the project's directory structure conventions:

**Common React Web Structure:**

```

app/
  (public)/
    page.tsx
    layout.tsx
  (admin)/
    admin/
      page.tsx
      layout.tsx
  globals.css
  layout.tsx
components/
  Button.tsx
  Card.tsx
  Input.tsx
hooks/
  usePagination.ts
lib/
  fetcher.ts
  api.ts
  cn.ts
stores/
  authStore.ts

```

**Common React Native Structure:**

```

./src/
  components/
    Button.jsx
    Card.jsx
  screens/
    ProductsScreen.jsx
    HomeScreen.jsx
  hooks/
    useProducts.js
  lib/
    fetcher.ts
    api.ts
  stores/

```
