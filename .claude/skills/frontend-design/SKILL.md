---
name: frontend-design
description: Guidance for distinctive, intentional visual design when building or reshaping UI in AI Engineer Daily. Covers aesthetic direction, typography, and how the project's DESIGN.md system constrains where boldness is allowed.
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Frontend Design

> Adapted from the `frontend-design` skill in Anthropic's official plugin marketplace
> (Apache-2.0, see LICENSE.txt). Modified for AI Engineer Daily: the "This project"
> section below is new, and the process section is scoped to an existing design system
> rather than a greenfield brief.

Approach this as the design lead at a small studio known for giving every client a visual identity that could not be mistaken for anyone else's. This client has already rejected proposals that felt templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take one real aesthetic risk you can justify.

## This project

AI Engineer Daily is a Next.js 16 / React 19 / Tailwind v4 reading surface: a daily brief, article pages, and search. The reader is an engineer skimming on the way to something else, so legibility and scan speed outrank expression.

**`DESIGN.md` at the repo root is authoritative and wins over anything below.** It fixes the type scale, the gray-based palette, card treatment, the spacing ladder, and the motion vocabulary. Read it before you write UI. If a design idea requires breaking it, that's a proposal to the human and an edit to `DESIGN.md` — not a one-off deviation in a component.

That flips the usual mandate here. The generic version of this skill tells you to take an aesthetic risk on every page; this product's stated principle is "consistency is more important than creativity." Both survive if you scope them:

- **Systemic axes are closed.** Palette, type scale, card shell, spacing steps, hover motion — match `DESIGN.md` exactly and reuse `components/` (`NewsCard`, `Section`, `Badge`) rather than restyling in place. New UI that looks like an existing pattern must *be* that pattern.
- **Editorial axes are open.** Hierarchy within a page, what the hero actually leads with, how a brief is sequenced, what a badge encodes, empty and error states, density and rhythm. This is where the work gets a point of view, and where "one memorable thing" belongs.
- **Before adding a token, check `app/globals.css`.** It defines `--background` / `--foreground` with a `prefers-color-scheme` dark block, so anything hardcoded to `text-gray-900` needs a dark-mode answer or it breaks at night. Prefer the theme variables when a value should follow the scheme.
- **Stack notes:** Tailwind v4 (CSS-first `@theme`, no `tailwind.config.js`). Per `AGENTS.md`, read the relevant guide in `node_modules/next/dist/docs/` before writing Next.js code — this version diverges from what you remember.

Also: the DESIGN.md inspiration list (Apple, OpenAI, Notion, Linear) is a shared reference, which means it is also the most-imitated look in this category. Treat "clean sans, gray-50 canvas, white rounded card, subtle lift on hover" as the floor you inherit, not the idea you contribute.

## Ground it in the subject

If the brief does not pin down what the product or subject is, pin it yourself before designing: name one concrete subject, its audience, and the page's single job, and state your choice. If there's any information in your memory about the human's preferences, context about what they're building, or designs you've made before – use that as a hint. The subject's own world, its materials, instruments, artifacts, and vernacular, is where distinctive choices come from. Build with the brief's real content and subject matter throughout.

Here the subject's world is AI/ML engineering: papers, releases, benchmarks, model cards, changelogs, sources with dates and provenance. Real headlines and real timestamps beat lorem ipsum every time — a layout tuned on fake content usually breaks on the real thing.

## Design principles

For web designs, the hero is a thesis. Open with the most characteristic thing in the subject's world, in whatever form makes sense for it: a headline, an image, an animation, a live demo, an interactive moment. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the template answer, only use if that's truly the best option.

Typography carries the personality of the page. Pair the display and body faces deliberately, not the same families you would reach for on any other project, and set a clear type scale with intentional weights, widths, and spacing. Make the type treatment itself a memorable part of the design, not a neutral delivery vehicle for the content. *In this repo, the scale is already set in `DESIGN.md` — personality comes from how you apply it (measure, rhythm, where weight lands), not from introducing new sizes.*

Structure is information. Structural devices, numbering, eyebrows, dividers, labels, should encode something true about the content, not decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence - like a real process or a typed timeline where order carries information the reader needs. Question if choices like numbered markers actually make sense before incorporating them. *A daily brief genuinely is chronological — dates and ordering carry real information here, so lean on them where they're true and drop them where they aren't.*

Leverage motion deliberately. Think about where and if animation can serve the subject: a page-load sequence, a scroll-triggered reveal, hover micro-interactions, ambient atmosphere. An orchestrated moment usually lands harder than scattered effects; choose what the direction calls for. However, sometimes less is more, and extra animation contributes to the feeling that the design is AI-generated. *`DESIGN.md` caps this at `transition-all duration-300`, `hover:-translate-y-1`, `hover:shadow-lg`. Don't exceed it without asking.*

Match complexity to the vision. Maximalist directions need elaborate execution; minimal directions need precision in spacing, type, and detail. Elegance is executing the chosen vision well. This project is firmly the minimal case, so the quality bar is precision: consistent optical spacing, correct measure, no orphaned labels, alignment that holds at every breakpoint.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Process: brainstorm, explore, plan, critique, build, critique again

For calibration: AI-generated design right now clusters around three looks: (1) a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta accent; (2) a near-black background with a single bright acid-green or vermilion accent; (3) a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns. All three are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly — the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. Just like a human designer who's hired, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.

Add a fourth default to that list for this project, because a news reader invites it: the "AI newsletter" look — gradient-on-white hero, pill-shaped category chips in six unrelated hues, a 3-up card grid with icon circles, and stat tiles nobody asked for. `DESIGN.md` already rules out most of it; notice when you're drifting there anyway.

Work in two passes. First, brainstorm a short design plan. On a greenfield surface that means a compact token system — color as 4–6 named hex values, typefaces for 2+ roles, a layout concept with ASCII wireframes, and a signature element. **In this repo the token system already exists**, so the plan is shorter and different: name the existing tokens and components you'll reuse, name the one editorial decision that makes this screen specific, and sketch the layout in ASCII to compare against alternatives before committing.

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief — revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan exactly and deriving every color and type decision from it.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and a element-based selector like .cta). This can happen often with paddings/margins between sections. With Tailwind this shows up instead as competing utilities on one element and as spacing applied from both sides of a gap — pick one owner for the space between two things (the container's `gap` or the child's margin, not both).

Try to do a lot of this planning and iteration in your thinking, and only show ideas to the user when you have higher confidence it'll delight them.

## Restraint and self-critique

Spend your boldness in one place. Let the signature element be the one memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Not taking a risk can be a risk itself! Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected. Critique your own work as you build, taking screenshots if your environment supports it – a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creators have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

Run `npm run dev` and look at the result before calling a change done; the `/run` skill can drive it. Check the dark scheme too — `globals.css` has a `prefers-color-scheme: dark` block, and gray-fixed text is the usual thing that breaks there. When a screen settles into a pattern worth repeating, add it to `DESIGN.md` so the next pass inherits it.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand, and therefore easier to use. They are design material, not decoration. Bring the same intentionality to copy that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's side of the screen. Name things by what people control and recognize, never by how the system is built. A person manages notifications, not webhook config. Describe what something does in plain terms rather than selling it. Being specific is always better than being clever.

Use active voice as default. A control should say exactly what happens when it's used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act. For this product that means: a search with no results says what was searched and offers a next move; a day with no brief yet says when the next one lands.

Keep the register conversational and tuned: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each element do exactly one job. A label labels, an example demonstrates, and nothing quietly does double duty. The audience is working engineers — don't explain what an LLM is, and don't hype a release the source didn't hype.
