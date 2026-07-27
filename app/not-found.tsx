import Link from "next/link";

export default function NotFound() {
  return (
    <main className="px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl">
        <p className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
          404
        </p>

        <h1 className="mt-3 text-5xl font-bold tracking-tight text-ink">
          No such story
        </h1>

        <p className="mt-3 max-w-2xl text-xl leading-8 text-ink-muted">
          That article isn&rsquo;t in the archive. It may have been removed, or
          the link may be wrong.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/"
            className="rounded-full bg-ink px-6 py-3 text-sm font-semibold text-surface transition-opacity hover:opacity-80"
          >
            Read today&rsquo;s brief
          </Link>

          <Link
            href="/search"
            className="rounded-full border border-rule bg-card px-6 py-3 text-sm font-semibold text-ink transition-colors hover:bg-accent-soft"
          >
            Search the archive
          </Link>
        </div>
      </div>
    </main>
  );
}
