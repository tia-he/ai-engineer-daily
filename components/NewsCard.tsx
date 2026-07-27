import Link from "next/link";

import Badge from "./Badge";

type NewsCardProps = {
  id: string;
  title: string;
  summary: string;
  /** Publisher of record. Replaces an ordinal — the feed isn't ranked. */
  source?: string | null;
  readMinutes?: number;
  concepts?: string[];
  matchedIn?: string[];
};

export default function NewsCard({
  id,
  title,
  summary,
  source,
  readMinutes,
  concepts,
  matchedIn,
}: NewsCardProps) {
  const shownConcepts = concepts?.slice(0, 3) ?? [];

  return (
    <Link
      href={`/news/${id}`}
      className="group block rounded-3xl border border-rule bg-card p-7 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
    >
      <article>
        <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-rule pb-4">
          <span className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
            {source ?? "Unattributed"}
          </span>

          {readMinutes ? (
            <span className="shrink-0 font-mono text-xs tracking-tight text-ink-faint">
              {readMinutes} min
            </span>
          ) : null}
        </div>

        <h3 className="mt-4 text-2xl font-semibold tracking-tight text-ink transition-colors group-hover:text-ink-muted">
          {title}

          <span className="ml-2 inline-block text-ink-faint transition-transform duration-300 group-hover:translate-x-1">
            →
          </span>
        </h3>

        <p className="mt-3 text-base leading-7 text-ink-muted">{summary}</p>

        {(shownConcepts.length > 0 || (matchedIn && matchedIn.length > 0)) && (
          <div className="mt-5 flex flex-wrap gap-2">
            {shownConcepts.map((concept) => (
              <Badge key={concept} text={concept} />
            ))}

            {matchedIn?.map((field) => (
              <Badge key={`matched-${field}`} text={`matched in ${field}`} />
            ))}
          </div>
        )}
      </article>
    </Link>
  );
}
