# AI Engineer Daily Design System

This document defines the design principles and UI standards for AI Engineer Daily.
The goal is to keep the product clean, consistent, and easy to extend.

---

# Design Principles

1. Clarity over decoration.
2. Readability comes before aesthetics.
3. Consistency is more important than creativity.
4. Every page should feel lightweight and focused.
5. Use whitespace intentionally.

---

# Typography

## Page Title (H1)

Used for page titles.

Example:
AI Engineer Daily

Tailwind:

```tsx
text-5xl font-bold tracking-tight text-gray-900
```

---

## Subtitle

Used below page titles.

Example:
Stay ahead in AI and software engineering.

Tailwind:

```tsx
text-xl text-gray-600
```

---

## Meta

Used for dates and secondary information.

Example:
Tuesday · July 21, 2026

Tailwind:

```tsx
text-sm text-gray-500
```

---

## Section Title

Used for page sections.

Examples:

- Today's Brief
- Concepts
- Sources
- Related News

Tailwind:

```tsx
text-2xl font-semibold text-gray-900
```

---

# Color Palette

## Background

```tsx
bg-gray-50
```

## Card

```tsx
bg-white
```

## Primary Text

```tsx
text-gray-900
```

## Secondary Text

```tsx
text-gray-600
```

## Meta Text

```tsx
text-gray-500
```

---

# Cards

All cards should share the same visual style.

Tailwind:

```tsx
rounded-3xl
border
border-gray-200
bg-white
shadow-sm
transition-all
duration-300
hover:-translate-y-1
hover:shadow-lg
```



---

# Spacing

Use consistent spacing throughout the project.

| Element | Tailwind |
|----------|----------|
| Header → Subtitle | mt-3 |
| Subtitle → Meta | mt-2 |
| Header → Content | mt-12 |
| Card → Card | mt-5 |
| Section → Section | mt-12 |

---

# Motion

Animations should be subtle.

Use:

- transition-all
- duration-300
- hover:-translate-y-1
- hover:shadow-lg

Avoid flashy animations.

---

# Inspiration

The visual language is inspired by:

- Apple
- OpenAI
- Notion
- Linear

The goal is **not** to copy their interfaces, but to learn from their typography, spacing, simplicity, and information hierarchy.
