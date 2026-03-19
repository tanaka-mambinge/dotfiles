---
name: react-component-creation
description: Standards for creating custom reusable React components with TypeScript, Tailwind CSS, and Radix Primitives. Use when building new UI components for web applications.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  framework: react
---

# React Component Creation Standards

Guidelines for creating custom reusable React components following consistent patterns and best practices.

## File Organization

- **Location**: `components/ui/`
- **Naming**: PascalCase with `.tsx` extension (e.g., `Button.tsx`, `TextField.tsx`)
- **Structure**: Single file containing component, types, and styles

## Component Pattern

Use default export with function declaration:

```tsx
export default function ComponentName(props: ComponentNameProps) {
  // Component implementation
}
```

## Props Definition

Define props using interface extending React.ComponentProps:

```tsx
interface ButtonProps extends React.ComponentProps<'button'> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  // Additional custom props
}
```

**Key points:**

- Use `interface` keyword
- Extend `React.ComponentProps<'element'>` for HTML elements
- Extend base Radix component props when using Radix primitives
- Define custom props after the extends clause

## Variant Management

Use string literal types for variants:

```tsx
interface ComponentProps extends React.ComponentProps<'element'> {
  variant?: 'primary' | 'secondary' | 'outline';
}

export default function Component({ variant = 'primary', ...props }: ComponentProps) {
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
  };
  
  return <element className={cn(variantStyles[variant], props.className)} {...props} />;
}
```

## Styling Approach

Always use the `cn()` utility from `@/lib/cn.ts` to merge Tailwind classes:

```tsx
import { cn } from '@/lib/cn';

export default function Component({ className, ...props }: ComponentProps) {
  return (
    <element 
      className={cn(
        'base-classes',
        'hover:state-classes',
        className
      )} 
      {...props} 
    />
  );
}
```

**Key points:**

- Import `cn` from `@/lib/cn.ts`
- Apply base classes first
- Apply state/variant classes conditionally
- Always include `className` prop for composability
- Place user's `className` last to allow overrides

## Radix Primitives Integration

Use Radix Primitives as the base for components when available:

```tsx
import * as Slider from '@radix-ui/react-slider';
import { cn } from '@/lib/cn';

interface PriceSliderProps extends React.ComponentProps<typeof Slider.Root> {
  // Custom props
}

export default function PriceSlider({ className, ...props }: PriceSliderProps) {
  return (
    <Slider.Root 
      className={cn(
        'relative flex h-5 w-[200px] touch-none select-none items-center',
        className
      )}
      {...props}
    >
      <Slider.Track className="relative h-[3px] grow rounded-full bg-gray-300">
        <Slider.Range className="absolute h-full rounded-full bg-blue-600" />
      </Slider.Track>
      <Slider.Thumb 
        className="block size-5 rounded-full bg-white shadow-md hover:bg-gray-50"
        aria-label="Price range"
      />
    </Slider.Root>
  );
}
```

**Key points:**

- Import pattern: `import * as ComponentName from '@radix-ui/react-component-name'`
- Extend Radix component props: `React.ComponentProps<typeof Radix.Root>`
- Style each Radix part with Tailwind classes
- Use Radix for: Dialogs, Dropdowns, Sliders, Tooltips, Accordions, etc.
- Fall back to native HTML elements when Radix doesn't provide the component

## Ref Forwarding

Forward refs only when needed (interactive elements, forms, animations):

```tsx
import { forwardRef } from 'react';

interface InputProps extends React.ComponentProps<'input'> {
  label?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, ...props }, ref) => {
    return (
      <div>
        {label && <label className="text-sm font-medium">{label}</label>}
        <input
          ref={ref}
          className={cn('border rounded px-3 py-2', className)}
          {...props}
        />
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
```

**When to forward refs:**

- Form inputs (text, textarea, select)
- Elements that need focus management
- Components used with animation libraries
- When parent needs direct DOM access

**When NOT to forward refs:**

- Static display components
- Layout wrappers
- Simple styled containers
