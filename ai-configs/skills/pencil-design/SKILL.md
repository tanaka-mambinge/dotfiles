---
name: pencil-design
description: Use this skill alongside the 'frontend-design' skill when designing in Pencil.dev. This skill provides technical constraints and best practices to prevent layout failures.
category: design
---

# Pencil.dev Design Guidelines

**CRITICAL**: Always use this skill **together with the `frontend-design` skill**. The frontend-design skill provides the design thinking, aesthetic direction, and real-world principles. This skill provides the technical constraints specific to the Pencil.dev layout engine. Both are required for successful design work.

This skill guides proper layout construction in Pencil.dev to prevent common technical failures.

## Design Philosophy

Pencil.dev uses a flexbox-based layout engine with specific constraints. Understanding these constraints allows you to build freely within them. The tool provides visual editing capabilities, but the underlying .pen format follows rigid rules that must be respected.

Technical constraints are not creative limitations. They are the boundaries within which exceptional design happens. Work with the flexbox system rather than against it.

## Critical Constraints

### Frame Height Behavior

The layout engine does not automatically expand parent frames to fit children. Fixed heights truncate content when content exceeds the declared dimension. Use dynamic height values that allow frames to grow with their content. Reserve fixed heights only for elements that must maintain exact dimensions.

### Padding Requirements

All screens need breathing room between content and boundaries. Insufficient padding causes elements to touch edges. Generous padding creates visual hierarchy and professional appearance. Text blocks benefit from maximum width constraints for readability.

### Text Expansion

Text elements grow beyond their declared dimensions. Long strings break layouts. Plan for maximum text length plus adequate buffer space. Container frames should use dynamic width when holding text. Never constrain text with fixed widths.

### Layout Engine Behavior

Absolute positioning is ignored on flexbox children. Coordinate properties have no effect inside frames with layout properties. Spacing is controlled entirely by parent gap and padding values. Work with this system, not against it.

### Screenshot Verification

The system cannot handle multiple concurrent screenshot requests. Take one screenshot per screen. Analyze results. Fix issues. Then proceed. Batching screenshots causes failures and requires restarting the entire design process.

## Anti-Patterns

Fixed height on content containers results in clipped elements and hidden content.

Fixed width on text elements causes truncation and unreadable copy.

Absolute positioning on flexbox children is silently ignored, breaking intended layouts.

Insufficient padding on screen edges pushes content to boundaries, appearing broken.

Child elements wider than their parent overflow boundaries.

Multiple simultaneous screenshot calls crash the verification system.

## Workflow

1. **Start with frontend-design skill**: Establish the design direction, aesthetics, and real-world constraints
2. **Apply pencil-design constraints**: Implement within Pencil.dev's technical limitations
3. **Build one screen at a time**: Define the structure with proper constraints
4. **Take one screenshot to verify**: Analyze for clipping, overflow, or misalignment
5. **Fix any issues**: Then proceed to the next screen

This methodical approach prevents cascading errors and ensures each screen functions correctly before adding complexity.

## Technical Flexibility

Within these constraints, all creative decisions remain open as defined by the frontend-design skill. Typography, color, spacing, composition, and visual style are flexible within realistic, production-ready boundaries. The constraints ensure your creative work displays correctly—they do not dictate what that work should be.

Choose appropriate directions for the context. Experiment within reason. Create distinctive visual languages that solve real problems. Just ensure the technical foundation supports your vision by respecting the flexbox behavior and dimension rules.
