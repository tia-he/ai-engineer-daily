import Link from "next/link";

import Section from "../../../components/Section";

const MAIN_SECTION_TITLES = ["Takeaway", "Article", "Background"];
const RAIL_SECTION_TITLES = ["Concepts", "Sources"];

export default function Loading() {
  return (
    <main className="pb-24">
      <div className="chrome-grid border-b border-white/10 bg-chrome">
        <div className="mx-auto flex w-full max-w-5xl items-baseline justify-between px-6 py-3">
          <Link
            href="/"
            className="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-[0.14em] text-chrome-ink/60 transition-colors hover:text-chrome-ink"
          >
            <span aria-hidden="true">←</span>
            Back to the brief
          </Link>

          <div className="h-3 w-16 animate-pulse rounded-full bg-white/10" />
        </div>
      </div>

      <article className="mx-auto w-full max-w-5xl px-6 pt-12">
        <header className="max-w-3xl border-b border-rule pb-10">
          <div className="h-3 w-24 animate-pulse rounded-full bg-accent-soft" />

          <div className="mt-4 space-y-3">
            <div className="h-10 w-full animate-pulse rounded-full bg-accent-soft sm:h-12" />
            <div className="h-10 w-2/3 animate-pulse rounded-full bg-accent-soft sm:h-12" />
          </div>

          <div className="mt-6 h-6 w-full animate-pulse rounded-full bg-accent-soft" />
        </header>

        <div className="mt-10 h-64 w-full max-w-3xl animate-pulse rounded-3xl bg-accent-soft sm:h-80" />

        <div className="lg:grid lg:grid-cols-[1fr_320px] lg:items-start lg:gap-12">
          <div className="min-w-0">
            {MAIN_SECTION_TITLES.map((title) => (
              <Section key={title} title={title}>
                <div className="space-y-3">
                  <div className="h-4 w-full animate-pulse rounded-full bg-accent-soft" />
                  <div className="h-4 w-5/6 animate-pulse rounded-full bg-accent-soft" />
                </div>
              </Section>
            ))}
          </div>

          <aside className="mt-12 lg:mt-0">
            {RAIL_SECTION_TITLES.map((title) => (
              <Section key={title} title={title}>
                <div className="space-y-3">
                  <div className="h-4 w-full animate-pulse rounded-full bg-accent-soft" />
                  <div className="h-4 w-2/3 animate-pulse rounded-full bg-accent-soft" />
                </div>
              </Section>
            ))}
          </aside>
        </div>
      </article>
    </main>
  );
}
