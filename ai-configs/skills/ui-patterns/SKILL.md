---
name: ui-patterns
description: >-
  Create or review clear, good-looking web and app interfaces for everyday users.
  Use when choosing layout, hierarchy, typography, information density, or
  interaction patterns, and when checking a UI for common visual and usability
  anti-patterns. Complements ui-design by providing a focused clarity and
  composition lens.
---

# UI Patterns

Use this skill when the work changes how an interface looks, reads, or is
organized. The goal is a UI that feels obvious to a normal person: important
things are easy to find, the page has room to breathe without feeling empty,
and deeper detail is available without putting everything in front of the user
at once.

This is a focused companion to `ui-design`, not a replacement for a full
accessibility or implementation audit. Preserve existing project conventions
when they serve the user; improve them when they create the problems below.

## Choose the right degree of change

Match the design process to the user's request:

- **Redesign, reimagine, or start over:** be willing to create a genuinely new
  visual direction, layout, hierarchy, component treatment, and type system.
  Do not keep an old interface's appearance or structure just because it is
  familiar. Carry forward the product's useful content and behavior unless
  the user asks to change those too.
- **Improve, refine, polish, or clean up:** treat the current interface as the
  visual baseline. Make targeted changes that solve the stated problems and
  retain recognizable structure and conventions where they already work.

In both cases, keep the existing color palette by default. Preserve its
semantic roles and recognizable character while adjusting contrast or shades
when needed. Change the palette only when the user explicitly requests a new
one.

## Start with the user's view

Before choosing components or styling, identify:

- the page or screen's one primary purpose;
- the user's most important action or decision;
- what must be visible immediately and what belongs behind a detail view,
  drawer, section, menu, or secondary page;
- the audience, especially whether the product is for everyday users or
  developers.

Make the first view answer “What is this?” and “What can I do here?” without
making the user hunt through decorative UI or dense controls.

## Create a clear visual hierarchy

Treat attention as a limited resource. Every screen should have a deliberate
order of importance:

1. **Primary focus:** the page purpose and the one action or decision that
   matters most right now.
2. **Secondary focus:** the information or controls needed to support that
   action.
3. **Supporting detail:** context, history, settings, edge cases, and rarely
   used actions that can be quieter or revealed later.

Guide the eye through this order with placement, scale, spacing, grouping,
weight, and restrained color. Do not give every element the same contrast,
size, border, shadow, saturation, or button treatment. If everything is loud,
nothing is important.

Use one clear starting point, meaningful whitespace between groups, and an
obvious next step. Let secondary content recede without making it invisible.
Avoid layouts where headings, cards, badges, icons, metrics, and actions all
compete for attention and the screen becomes a blob of equally weighted
things. When a screen cannot be scanned in a sensible order, reduce, group, or
move content before adding more styling.

## Layout and information architecture

- Prefer pages, sections, and focused detail views over putting a complete
  create form, list, detail view, and every action on one screen.
- Use progressive disclosure. Show the necessary summary first, then let the
  user drill down for history, configuration, explanations, or edge cases.
- Favor an F-shaped reading flow: establish a strong left-aligned column and
  let related content branch naturally to the right. Use the right side for
  supporting context, status, or secondary actions rather than making every
  element compete equally.
- Prefer vertical composition and natural scrolling. On narrow screens,
  stack content and controls rather than squeezing them into wide rows.
- Use consistent alignment, spacing, and grouping to communicate relationships;
  do not depend on borders and cards for every piece of structure.
- Give each region a job and a clear relationship to the region before it.
  Align related content, separate unrelated content with space, and avoid
  isolated elements that float without context.
- Treat horizontal scrolling as an exception. It is appropriate for content
  that is intrinsically wide, such as a data table or timeline, or when the
  user explicitly requests it. Do not make ordinary reading, navigation, or
  forms horizontally scrollable.

Avoid launch-control and control-panel aesthetics by default: no wall of
widgets, excessive chrome, tile grids, card piles, or unrelated metrics shown
only because there is room for them. Avoid box-heavy layouts that resemble a
Windows 8 menu. The composition should feel like a clear path through a task,
not a collection of panels.

## Typography and hierarchy

- Use at least two intentional, distinct font families when the product and
  performance budget allow it: normally a highly readable sans-serif for UI
  text plus a contrasting companion family for headings or emphasis. The
  companion may be a serif or a second sans-serif when that better fits the
  product. Do not add a second font merely for decoration.
- Reserve code fonts for developer-facing products or content that is actually
  code. Do not use monospace as a fashionable default for a consumer UI.
- Use comfortable, readable letter spacing. Never create a sparse, stretched,
  luxury-label look by applying wide tracking to ordinary headings or body
  copy.
- Establish a small, coherent type scale with clear differences between page
  titles, section headings, labels, body copy, metadata, and helper text.
- Make hierarchy visible through size, weight, spacing, and placement before
  relying on color or decoration.
- Check the rendered result at its real size. Text that technically exists but
  is faint, tiny, cramped, or low-contrast is not usable.

## Copy and controls for normal users

- Use familiar, plain-language labels and explain unfamiliar concepts at the
  point of need.
- Avoid technical jargon in user-facing copy. Terms such as CLI, terminal,
  repository, deployment, or API belong in developer tools or documentation,
  not in a normal person's settings or onboarding flow unless the audience
  genuinely needs them.
- Number items sparingly. Do not number every card, section, feature, or step
  as decoration.
- Do not use “eyebrow text,” “section kicker,” “editorial index label,” or
  similar design-language labels in the interface. Avoid decorative
  slash-separated index notation such as “01 / Title” unless the product's
  content or brand genuinely requires it.
- Keep primary actions obvious and secondary actions quiet or contextual.
  Hide destructive and rarely used actions behind an appropriate menu, detail
  view, or confirmation step.
- Use familiar controls and preserve their expected behavior. A button should
  look actionable, a link should navigate, and a field should have a visible
  label.

## Contrast, responsive behavior, and states

Visually inspect the interface rather than assuming the color tokens are safe.
Confirm that:

- body text, headings, labels, placeholder text, icons, borders, and disabled
  states remain distinguishable from their backgrounds;
- focus, hover, pressed, loading, empty, success, and error states are visible
  where applicable;
- important actions remain obvious in both light and dark themes when both are
  supported;
- content does not disappear under sticky headers, footers, or action bars;
- text, buttons, cards, sidebars, and compact panels do not overflow or
  overlap at narrow widths;
- the layout still has a clear reading order when columns stack.

Do not solve contrast problems by making every surface darker, brighter, or
more saturated. Adjust the hierarchy and semantic color roles so emphasis is
intentional.

## Working checklist

For a new or revised UI:

1. Classify the request as a new design, redesign, or improvement so the
   amount of visual change is intentional.
2. Define the primary purpose, audience, primary action, and information that
   can wait.
3. Sketch the page hierarchy with a left-aligned F-shaped reading path and
   explicit drill-down points.
4. Choose typography, spacing, surfaces, and controls as one coherent system,
   preserving the existing palette unless a new one was requested.
5. Remove decorative furniture, redundant panels, unnecessary numbers, and
   actions that do not help the user's task.
6. Render at a wide and narrow viewport and inspect the actual visual result.
7. Check contrast, reading order, overflow, interaction states, and whether a
   normal user can find the next useful action immediately.

When reviewing an existing UI, report concrete problems with the affected
screen or component and explain the user consequence. Do not redesign a
working pattern merely to make it more novel during an improvement pass. When
the user explicitly requests a redesign, a fresh visual system is encouraged;
the existing palette remains the default constraint.
