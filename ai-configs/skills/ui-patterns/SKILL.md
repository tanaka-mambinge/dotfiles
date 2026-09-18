---
name: ui-patterns
description: >-
  Create or review clear, distinctive, good-looking web and app interfaces for
  everyday users. Use when choosing layout, hierarchy, typography, copy,
  information density, visual direction, interaction patterns, motion, or
  micro-interactions, and when checking a UI for common visual and usability
  anti-patterns. Complements ui-design with a focused clarity, composition,
  variety, and interaction lens.
---

# UI Patterns

Use this skill when the work changes how an interface looks, reads, feels, or
is organized. The goal is a UI that is obvious to a normal person, visually
intentional, and responsive to what they do. A first pass is not finished
until it has gone through the mandatory enhancement pass below.

This skill is a focused companion to `ui-design`, not a replacement for a
full accessibility or implementation audit. Preserve existing project
conventions during refinement when they serve the user; improve them when
they create the problems below.

## Non-negotiable quality floor

These rules apply on every task and cannot be diluted by optional references:

- Establish the page's one primary purpose, audience, most important action,
  and clear reading order before styling.
- Make hierarchy deliberate. Important content and actions must be easy to
  find; supporting detail should recede or use progressive disclosure.
- Keep one clear narrative spine. Choose an F-shaped path for content-led
  pages or a Z-shaped path for short landing pages when the content supports
  it. Establish a left-side anchor for F layouts and let related information
  branch from it. Do not alternate the dominant content from side to side or
  create a zig-zag reading path merely for visual variety.
- Use numbers only when they genuinely number an ordered list or are essential
  product data. Never add decorative numbers to headings, labels, cards,
  sections, or metadata. Never use `/` in rendered user-facing copy,
  headings, labels, navigation, metadata, or decorative notation.
- Give every section one unique job. Remove repeated claims, filler content,
  decorative labels, unnecessary metadata, and extra calls to action. Do not
  turn every group of ideas into a card grid or four-column band.
- Keep descriptions, helper text, metadata, and actions subordinate to their
  heading. Do not give supporting copy the same visual weight or level as the
  primary heading.
- Choose a coherent visual direction rather than assembling generic components.
  Deliberately choose a shape language, surface or material language, control
  language, composition language, and interaction language. Use layout, copy,
  type, spacing, surfaces, controls, and effects as one connected system.
- Do not let rectangular cards, rectangular buttons, flat surfaces, or
  color-only hover states become the automatic answer. They are valid choices
  when intentional, but an interface made entirely from those defaults must
  be reconsidered or justified internally before delivery.
- Pages and interactions must not feel inert, static, or flat. Include
  purposeful motion and micro-interactions that clarify cause and effect,
  continuity, state, or fitting delight. A color or opacity change alone is
  not enough when a richer response would improve the experience.
- When variations are requested, make genuinely different design directions.
  Change the composition, layout, hierarchy, wording, copy tone, typography,
  component relationships, spacing, surfaces, and motion language—not just
  the palette or decoration. Never duplicate the first direction and reskin
  it. Preserve the underlying goal and functionality unless behavioral
  alternatives are requested.
- Keep controls familiar and copy plain. Keep secondary and destructive
  actions contextual instead of making every action equally prominent.
- Verify real rendered behavior at wide and narrow sizes, including contrast,
  overflow, focus, hover, pressed, loading, empty, success, and error states
  where applicable. Respect reduced-motion preferences.

## Mandatory workflow

Use the agent's internal todo, step list, or equivalent progress tracker. Do
not create a tracking document in the project. Track these items explicitly
and mark them done only after they have been implemented or inspected:

- Intent and audience
- Visual direction
- Layout and hierarchy
- Copy and typography
- Surfaces and visual treatment
- Interaction states
- Motion and micro-interactions
- Responsive and accessibility checks
- Variation requirements, when applicable
- Final rendered review

Complete the workflow in this order:

1. Classify the request as refinement, redesign, review, or variations. For
   refinement, treat the current interface as the visual baseline. For
   redesign, a new visual system is encouraged. For explicit variations,
   each direction may establish its own coherent palette and system.
2. Inspect the request, existing UI, project conventions, available assets,
   and target viewport. Define the purpose, audience, primary action, and
   what can wait behind progressive disclosure.
3. Resolve visual direction before committing to generic styling. If the
   brief leaves it materially open, brainstorm a few coherent directions or
   ask focused questions. Keep this contextual and open-ended; do not use a
   fixed catalogue of style labels.
   For variations, read
   [references/variation-workflow.md](references/variation-workflow.md) now,
   create a separate structural brief for every direction in the internal
   tracker, and do this before implementing any direction.
4. Create the initial design or review pass.
5. Read [references/enhancement-pass.md](references/enhancement-pass.md) and
   [references/creative-direction.md](references/creative-direction.md) and
   [references/content-and-layout.md](references/content-and-layout.md).
   Inspect the actual result against every section and use the references to
   challenge generic geometry, surfaces, controls, content density, and
   interaction patterns.
   Reading the references is not completion; apply the improvements they
   reveal. If a section does not apply, record why in the internal tracker.
6. For variation requests, compare every rendered direction structurally and
   visually before presenting them. If any pair converges, revise it; do not
   present the set yet.
7. Re-render after the enhancement pass. Fix missed hierarchy, copy, visual
   quality, state, responsive, and interaction issues before delivery.
8. Complete the final rendered review and only then hand off the result. For
   variations, all directions must pass the comparison gates in the reference.

## Direction and composition

- Prefer a clear path through the task over a wall of widgets, card piles,
  unrelated metrics, or control-panel chrome. Use the fewest sections needed
  to make the product understandable and persuasive.
- Use vertical composition and natural scrolling. Stack content and controls
  on narrow screens rather than forcing ordinary reading or forms to scroll
  horizontally.
- Give each region a job. Align related content, separate unrelated content
  with space, and use detail views, drawers, sections, and menus for deeper
  information or rarely used actions.
- Use multi-column layouts only when the items are genuinely comparable,
  equally important, concise, and improved by being seen together. A group of
  four items is not a reason to create four columns.
- Keep descriptions, metadata, and helper text visually subordinate to their
  heading through scale, weight, spacing, placement, and contrast.
- Preserve the existing palette and semantic roles during refinement unless a
  new palette is requested. Distinct requested variations may use different
  palettes when each remains coherent and usable.

## Motion and interaction character

- Choose motion based on the component, trigger, spatial relationship, and
  chosen visual direction. Vary origins, trajectories, pacing, staging, and
  transition mechanisms so every interface does not use one canned recipe.
- Use spatial or dimensional responses where they improve feedback: elements
  may emerge from a meaningful origin, track an action, reshape around new
  content, reveal or mask information, or hand attention to a related element.
- Animate paired states consistently. Do not polish only hover while ignoring
  focus or pressed feedback, or animate opening without considering closing.
- Keep frequent interactions quick and unobtrusive. Do not delay input,
  obscure content, create noise, or use motion instead of clear state design.
- For detailed timing, easing, springs, gestures, performance debugging, or
  reverse-engineering motion, use `ui-animation`.

## Final handoff

Before delivery, confirm the internal tracker is complete, the rendered result
has passed the enhancement reference, and any intentional exceptions are
understood. Briefly summarize the visual direction, meaningful interaction or
motion work, and deliberate exceptions without exposing unnecessary internal
process detail.
