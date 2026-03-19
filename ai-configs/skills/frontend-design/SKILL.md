---
name: frontend-design
description: Use this when creating production-grade frontend interfaces that are realistic, usable, and context-appropriate. Use this skill when the user asks to build web components, pages, or applications. Generates polished, practical code that solves real problems without unnecessary complexity.
license: Complete terms in LICENSE.txt
---

This skill guides creation of **production-ready, realistic frontend interfaces** that users would actually deploy. Focus on solving real problems with clean, maintainable code that balances aesthetics with practicality.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and choose an **appropriate** aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it daily?
- **Context**: What industry? What's the user's mental model? A fintech dashboard has different needs than a creative portfolio.
- **Constraints**:
  - Performance budgets and load times
  - Accessibility requirements (WCAG compliance)
  - Team maintainability (will other developers need to work on this?)
  - Browser/device support needs
- **Appropriate Distinctiveness**: Design should be memorable **within reason** for its context. A B2B SaaS tool needs professional polish, not "wow factor." A marketing site can be more expressive.

**CRITICAL**: Match design complexity to the actual use case. Over-designing wastes time and creates maintenance burden. Under-designing looks unprofessional. Find the sweet spot.

## Real-World Design Principles

### Typography

- **Body text**: Use highly readable fonts appropriate for the content length. System fonts (system-ui, -apple-system) are perfectly fine for UI text.
- **Headings**: Can be more distinctive, but prioritize legibility over novelty.
- **Font loading**: Consider performance. Use font-display: swap. Don't load 5+ web fonts for a simple page.
- **Sizing**: Establish a clear type scale (1.25x or 1.5x ratio). Don't use 12 different font sizes.

### Color & Theme

- **Start with a purpose**: What emotion or function should the color serve?
- **Accessibility first**: Ensure 4.5:1 contrast ratios for text. Test with color blindness simulators.
- **Limit the palette**: 1-2 primary colors, 1-2 neutrals, 1 accent. More colors = more confusion.
- **Avoid**: Neon-on-neon, ultra-low contrast "elegant" gray-on-white, 47 gradient stops.

### Layout & Composition

- **Follow conventions**: Users have expectations. Navigation at top, CTAs visible, forms with labels.
- **Grid systems**: Use consistent spacing (4px, 8px, or 16px base units). Don't eyeball it.
- **Whitespace**: Generous but purposeful. Not everything needs to "pop."
- **Responsive by default**: Design mobile-first. Test breakpoints at 320px, 768px, 1024px, 1440px.
- **Avoid**: Diagonal text for no reason, overlapping elements that hurt readability, "breaking the grid" just to be different.

### Motion & Animation

- **Purposeful motion**: Use animation to guide attention, show state changes, or provide feedback.
- **Performance**: Prefer transform and opacity animations. Avoid animating layout properties.
- **Timing**: 200-400ms for micro-interactions. Respect prefers-reduced-motion.
- **Avoid**: Loading animations that take 3 seconds, bouncing elements, parallax that causes motion sickness, animations on every single element.

### Components & Patterns

- **Use established patterns**: Users know how modals, dropdowns, and tabs work. Don't reinvent for novelty.
- **Consistency**: Buttons should look like buttons across the entire app. Forms should behave predictably.
- **State visibility**: Show loading, error, empty, and success states. Don't just design the happy path.
- **Avoid**: Custom scrollbars that break usability, mystery meat navigation, form inputs without labels.

## Anti-Patterns to Avoid

**NEVER do these "fancy" things that hurt usability:**

- Text that requires horizontal scrolling to read
- Auto-playing videos or music
- Hidden navigation (hamburger menus on desktop without reason)
- Scroll hijacking that breaks native scrolling behavior
- Modals that can't be closed with Escape key or outside click
- Forms that validate only on submit
- Images without alt text or proper aspect ratios
- Custom cursors that make clicking harder
- "Stunning" effects that tank performance on mid-tier devices

**Remember**: The best design is invisible. Users should focus on their task, not your design. Create interfaces that are reliable, fast, and pleasant to use—not interfaces that win design awards but frustrate users.
