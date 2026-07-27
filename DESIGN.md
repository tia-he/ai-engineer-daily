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

Used for secondary information (e.g. reading time).

Example:
1 min read

Tailwind:

```tsx
text-sm text-gray-500
```

Never display fabricated metadata (e.g. a made-up publication date).
If the underlying data doesn't exist yet, omit the line rather than
show something misleading — reading time is fine because it's
computed for real from the article's content length.

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

# Navigation

A single sticky NavBar (`components/NavBar.tsx`) appears on every
page: a wordmark on the left, Home/Search links on the right. The
active route is bold with a small underline.

Tailwind:

```tsx
sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-md
```

Because the nav is sticky, page `<main>` elements use a smaller
`pt-*` than they would otherwise (`pt-16` for Home/Search, `pt-10`
for the article page) so content doesn't sit doubly offset.

---

# Badges

Used for concept tags and "Matched in X" search indicators.

Tailwind:

```tsx
rounded-full border border-gray-200 bg-gray-100 px-3.5 py-1.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-200
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

# Loading States

Route-level data fetches (Home, Article) use Next.js's `loading.tsx`
convention; the search page's client-side fetch shows the same
skeleton inline while `isLoading` is true. Both reuse a single
`components/NewsCardSkeleton.tsx` so the loading shape always
matches the loaded shape.

Tailwind:

```tsx
animate-pulse rounded-3xl border border-gray-200 bg-white p-7
```

Apply `animate-pulse` to the card's outer wrapper, not to each
placeholder bar individually — the whole card should pulse together.

---

# Empty & Error States

Use `components/EmptyState.tsx` (icon + heading + subtext) instead
of a plain sentence whenever a list can legitimately be empty (zero
search results, zero articles). Icons are small inline stroke SVGs
in `text-gray-400`, not an icon library dependency.

A failed request (e.g. search) is shown as a bordered callout with a
Retry action, not unstyled red text:

```tsx
rounded-2xl border border-red-200 bg-red-50 px-6 py-4
```

An invalid route (e.g. an unknown article id) renders
`app/not-found.tsx`, styled to match the rest of the product instead
of Next's default 404 page.

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
