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
    <main className="min-h-screen bg-gray-50 px-6 pb-24 pt-10">
      <article className="mx-auto w-full max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center rounded-sm text-sm font-semibold text-gray-600 transition-colors duration-300 hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2"
        >
          ← Back to Today&apos;s Brief
        </Link>

        <header className="mt-12 border-b border-gray-200 pb-10">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
            AI Engineer Daily
          </p>

          <div className="mt-4 space-y-3">
            <div className="h-10 w-full animate-pulse rounded bg-gray-200 sm:h-12" />
            <div className="h-10 w-2/3 animate-pulse rounded bg-gray-200 sm:h-12" />
          </div>

          <div className="mt-6 h-6 w-full animate-pulse rounded bg-gray-100" />

          <div className="mt-5 h-4 w-20 animate-pulse rounded bg-gray-100" />
        </header>

        {SECTION_TITLES.map((title) => (
          <Section key={title} title={title}>
            <div className="space-y-3">
              <div className="h-4 w-full animate-pulse rounded bg-gray-100" />
              <div className="h-4 w-5/6 animate-pulse rounded bg-gray-100" />
            </div>
          </Section>
        ))}
      </article>
    </main>
  );
}
