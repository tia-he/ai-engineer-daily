import Link from "next/link";

import Section from "../../../components/Section";

const SECTION_TITLES = [
  "Article",
  "Takeaway",
  "Concepts",
  "Background",
  "Related News",
  "Sources",
];

export default function Loading() {
  return (
    <main className="px-6 pb-24 pt-12">
      <article className="mx-auto w-full max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-[0.14em] text-ink-faint transition-colors hover:text-ink"
        >
          <span aria-hidden="true">←</span>
          Back to the brief
        </Link>

        <header className="mt-10 border-b border-rule pb-10">
          <div className="h-3 w-24 animate-pulse rounded-full bg-accent-soft" />

          <div className="mt-4 space-y-3">
            <div className="h-10 w-full animate-pulse rounded-full bg-accent-soft sm:h-12" />
            <div className="h-10 w-2/3 animate-pulse rounded-full bg-accent-soft sm:h-12" />
          </div>

          <div className="mt-6 h-6 w-full animate-pulse rounded-full bg-accent-soft" />
        </header>

        {SECTION_TITLES.map((title) => (
          <Section key={title} title={title}>
            <div className="space-y-3">
              <div className="h-4 w-full animate-pulse rounded-full bg-accent-soft" />
              <div className="h-4 w-5/6 animate-pulse rounded-full bg-accent-soft" />
            </div>
          </Section>
        ))}
      </article>
    </main>
  );
}
