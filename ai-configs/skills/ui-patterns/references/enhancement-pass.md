# UI Enhancement Pass

Read this reference after the initial design or review pass for every new or
revised site and separately for every requested variation. Use the agent's
internal progress tracker to inspect each section in order. The purpose is to
improve the actual rendered result, not to produce a written checklist without
changing anything.

For every section: inspect the result, make the highest-value improvements,
then verify the result again. Mark the section complete only after that loop.
If a section genuinely does not apply, record the reason internally.

## 1. Purpose and hierarchy

- Can a new user tell what the page is and what to do next immediately?
- Is there one clear primary focus and action?
- Do placement, scale, spacing, grouping, weight, and color guide attention
  in a sensible order?
- Are secondary details quieter or progressively disclosed?
- Remove competing panels, redundant content, decorative numbers, and actions
  that do not help the task.

## 2. Content and reading path

- Can a new user understand the page by following one clear F-shaped or
  Z-shaped reading path?
- Is there a stable left-side anchor for an F layout, with supporting content
  branching from it?
- Does the page avoid alternating its dominant content from side to side or
  creating a zig-zag scan?
- Does every section have one unique job and add a new idea?
- Remove repeated claims, filler content, decorative labels, unnecessary
  metadata, and extra calls to action.
- Is every multi-column group genuinely comparable and improved by being shown
  together? Do not use four columns merely because there are four items.

## 3. Composition and visual direction

- Does the layout have a clear organizing idea instead of generic assembled
  components?
- Does every region have a purpose and relationship to nearby content?
- Are alignment, whitespace, density, surfaces, borders, shadows, and effects
  working as one system?
- Are effects restrained and supporting hierarchy rather than making every
  surface demand attention?
- For refinement, has the existing visual identity been respected unless a
  new direction was explicitly requested?

## 4. Creative breadth and specificity

- Is the shape language intentional, or did every major surface become a
  default rectangle with the same corner treatment?
- Are controls and buttons designed as part of the product's character rather
  than all using the same standard filled treatment?
- Do surfaces have a coherent character beyond flat background colors? Consider
  depth, transparency, texture, layering, framing, and material cues when they
  fit the product.
- Does the layout use a deliberate composition language rather than the same
  hero-plus-grid arrangement seen in generic site builds?
- Do interactions include spatial, dimensional, revealing, responsive, or
  continuity-preserving behavior where a flat state change would feel weak?
- Does the page feel specific to its product and direction rather than
  assembled from defaults?
- If multiple variants exist, can they be distinguished without comparing
  colors?

## 5. Copy and typography

- Are labels, headings, helper text, and actions plain and familiar for the
  intended audience?
- Are decorative numbers absent unless they are numbering a real list or are
  essential product data?
- Is `/` absent from rendered user-facing copy, headings, labels, navigation,
  metadata, and decorative notation?
- Is the wording concise and appropriate to the chosen direction?
- Are descriptions, metadata, helper text, and actions clearly subordinate to
  their headings rather than competing at the same visual level?
- Are decorative preheadings and design-language labels absent unless they
  convey necessary context?
- Does type hierarchy work through size, weight, spacing, and placement before
  relying on decoration?
- Are line length, line-height, tracking, and heading wraps comfortable at
  actual wide and narrow sizes?
- Are fonts intentional and coherent rather than decorative defaults?

## 6. Interaction states and motion

- Does the interface respond clearly to hover, focus, pressed, loading,
  success, error, reveal, and transition states that exist?
- Do interactions feel active and connected to the user's action rather than
  merely changing a color?
- Is there at least one appropriate spatial, dimensional, staged, or
  continuity-preserving response where the experience would otherwise feel
  static?
- Does motion have a reason, fit the visual direction, and vary where repeated
  patterns would feel mechanical?
- Are paired states treated consistently, input kept immediate, and reduced
  motion respected?

For detailed motion decisions, load `ui-animation` and follow its relevant
references. Do not let that handoff remove motion review from this pass.

## 7. Responsive behavior and accessibility

- Render and inspect the page at a wide and narrow viewport.
- Confirm content stacks in a useful reading order and no text, control,
  sidebar, card, or action bar overflows or overlaps.
- Check contrast for body text, labels, placeholders, icons, borders, disabled
  states, and text over imagery or gradients.
- Confirm focus visibility, keyboard access, touch targets, and state changes.
- Ensure sticky elements do not hide content or important actions.

## 8. Final polish

- Remove visual furniture that does not improve understanding or use.
- Remove any remaining decorative numbering, slash-separated notation, filler
  sections, repeated copy, unjustified grids, or competing text levels.
- Check that the primary action remains obvious and secondary actions stay
  appropriately quiet.
- Look for repeated component treatment, spacing, effects, or animation that
  makes the page feel generated or monotonous.
- Fix the most visible remaining quality issue before adding another effect.
- Re-render after fixes and verify that the result still feels coherent,
  usable, and intentional.
