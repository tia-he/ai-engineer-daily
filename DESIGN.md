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

Two faces, two jobs. **Geist Sans** carries everything a reader reads.
**Geist Mono** carries everything a machine produced: source names, counts,
timings, labels. Both are already loaded in `app/layout.tsx` — never introduce
a third family, and never set `font-family` on `body` (doing so overrides the
loaded fonts, which is how this project spent its first release rendering in
Arial).

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
Monday, July 27, 2026

Tailwind:

```tsx
text-sm text-ink-faint
```

---

## Machine Label

Used for provenance, counts, timings, and eyebrows — anything derived rather
than written. Mono, uppercase, letterspaced. This is the one typographic move
that gives the product its character, so it stays consistent everywhere.

Examples:

- OPENAI
- 3 STORIES · 3 SOURCES
- MONDAY, JULY 27, 2026

Tailwind:

```tsx
font-mono text-xs uppercase tracking-[0.16em] text-ink-faint
```

Durations keep their natural case (`1 min`, `4 min read`) and drop the
uppercase/tracking, since a unit isn't a label.

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

Colors are referenced through semantic tokens, never as raw `gray-*` utilities.
The light values are exactly the grays this system started with; the tokens exist
so the dark scheme in `app/globals.css` can flip them in one place. Hardcoding
`text-gray-900` strands text on the wrong background at night.

| Token | Utility | Light | Dark | Use |
|---|---|---|---|---|
| `--surface` | `bg-surface` | `#f9fafb` (gray-50) | `#0a0a0a` | Page canvas |
| `--card` | `bg-card` | `#ffffff` | `#141414` | Card fill |
| `--ink` | `text-ink` | `#111827` (gray-900) | `#ededed` | Primary text |
| `--ink-muted` | `text-ink-muted` | `#4b5563` (gray-600) | `#a1a1aa` | Body, secondary |
| `--ink-faint` | `text-ink-faint` | `#6b7280` (gray-500) | `#8b8b93` | Meta, eyebrows |
| `--rule` | `border-rule` | `#e5e7eb` (gray-200) | `#262626` | Borders, dividers |
| `--accent-soft` | `bg-accent-soft` | `#f3f4f6` (gray-100) | `#1c1c1c` | Badges, skeletons |

Inverted controls (primary buttons) use `bg-ink text-surface`, which stays correct
in both schemes without a second rule.

## Chrome

| Token | Utility | Value | Use |
|---|---|---|---|
| `--chrome` | `bg-chrome` | `#111827` (fixed) | Masthead, the brief's hero, the article dateline bar |
| `--chrome-ink` | `text-chrome-ink` | `#f9fafb` (fixed) | Text/icons on chrome |

Unlike every other token, `chrome` does **not** flip with `prefers-color-scheme` —
it's the site's constant dark instrument bar, not body content. Using the
inverting `bg-ink`/`text-surface` pair for a structural band (rather than a
small control) makes it flip to a *light* plank floating on a dark page in
dark mode, which is the bug this token exists to avoid. Borders/hairlines
inside chrome use `border-white/10` rather than `border-rule`, since `--rule`
also flips and would go invisible against a background that no longer does.

Every chrome surface also carries the `.chrome-grid` class (`globals.css`) —
a faint dot-lattice `background-image`, not a photo. It's the one place this
product spends a decorative flourish, so it's applied identically everywhere
chrome appears (masthead, hero, dateline bar, and their loading skeletons)
rather than varied per page. A literal photo was considered and rejected:
there's no single image that represents "AI engineering" without becoming a
stock-photo cliché, and a generated texture keeps the brand consistent
without a licensing/sourcing question per page.

---

# Cards

All cards should share the same visual style.

Tailwind:

```tsx
rounded-3xl
border
border-rule
bg-card
shadow-sm
transition-all
duration-300
hover:-translate-y-1
hover:shadow-lg
```

## Story card anatomy

A story card leads with a machine-label row — source on the left, reading time
on the right — separated from the title by a hairline rule. The whole card is
the link, so it carries no separate "Read article" control; the affordance is
the title's hover colour and the trailing arrow.

```text
┌──────────────────────────────────┐
│ ┌────────┐ OPENAI · JUL 27 3 min │  ← machine label, hairline under
│ │ image  │ Headline of the story │     →
│ │(if any)│ One-sentence summary. │
│ └────────┘ [concept] [concept]   │  ← at most 3
└──────────────────────────────────┘
```

The thumbnail and the `· JUL 27` date are both conditional on the record
actually having them (`imageUrl`, `publishedAt`) — a card with neither just
falls back to the text-only layout above. Never a placeholder image, never a
fabricated date.

---

# Provenance, not invented chronology

`published_at`/`image_url` are nullable columns fed by best-effort RSS
parsing (`backend/ingest_rss.py`): not every source provides a publish date
or a cover image, so a missing one is `null`, never a fabricated stand-in
like "July 21, 2026" or a stock photo. Show what the record actually
supports:

- **Source name** (`sources[0].name`) as the card and article eyebrow.
- **Reading time** derived from the real body copy at 220 wpm.
- **Published date** (`lib/format.ts#publishedLabel`) next to the source,
  only when the feed provided one.
- **Cover image** (`imageUrl`) as the card thumbnail / article lead image,
  only when the feed provided one.
- **Today's date** on the brief header itself, computed at request time —
  the brief is genuinely a daily surface, so "today" is true regardless of
  any one article's `publishedAt`.

For the same reason, story cards carry no `01 / 02 / 03` ordinals: the feed is
returned in insertion order and is not ranked, so a number would imply an
editorial judgement the data doesn't contain.

---

# States

Every fetching surface needs all four. Each one names what happened and offers
the next move; none of them apologise or go vague.

| State | Rule |
|---|---|
| Loading | Skeleton in `bg-accent-soft` matching the real layout's shape. Scope `loading.tsx` to the route it fits — a boundary above a route that calls `notFound()` streams the response and downgrades its 404 to a 200. |
| Empty | Say what was looked for and give a way forward (`Nothing matched "…"`, plus suggested topics). |
| Error | Name the failure and the fix (`The search service didn't respond. Check that the backend is running`). Never a bare "Something went wrong". |
| Not found | `app/not-found.tsx`, with routes back to the brief and to search. |

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

`globals.css` reduces all transitions to near-zero under
`prefers-reduced-motion: reduce`, so nothing above needs its own guard.

---

# Accessibility floor

Non-negotiable, and cheap to keep:

- Keyboard focus is visible everywhere — `globals.css` sets a `:focus-visible`
  outline in `--ink`, legible on both schemes. Don't remove it with
  `focus:outline-none` unless you replace it in the same rule.
- Decorative glyphs (`→`, `↗`, `←`) carry `aria-hidden="true"`.
- Badges are non-interactive and carry no hover state, so nothing reads as a
  button that isn't one.
- Async regions announce with `aria-live="polite"`.
- Layouts hold to 320px without horizontal scroll. Label/value rows use
  `flex-wrap` with `gap-x`/`gap-y` rather than a fixed `gap`.

---

# Inspiration

The visual language is inspired by:

- Apple
- OpenAI
- Notion
- Linear

The goal is **not** to copy their interfaces, but to learn from their typography, spacing, simplicity, and information hierarchy.
