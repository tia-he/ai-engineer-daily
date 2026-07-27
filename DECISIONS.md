# Product Decisions

## 2026-07-21

### Homepage

Decision:
Do not highlight a separate "Top Story".

Reason:
The product is designed for users to read all 3–5 daily stories. Showing one story as significantly more important may discourage users from reading the others.

---

### Design Style

Decision:
Adopt an Apple-inspired visual language.

Reason:
Focus on typography, spacing, simplicity, and information hierarchy instead of mimicking Apple's layouts.

---

## 2026-07-27

### Fabricated Metadata

Decision:
Never display fabricated metadata. The homepage and article page's
hardcoded publication date were removed rather than replaced with
the client's current date. Reading time was kept, since it's
computed for real from the article's content length.

Reason:
A hardcoded or fake-computed date is misleading data, not a design
detail. If a field's real value doesn't exist yet (no `published_at`
column on `Article` yet), it's better to omit it than show something
false. A real publication date will be added in a future backend
migration sprint.
