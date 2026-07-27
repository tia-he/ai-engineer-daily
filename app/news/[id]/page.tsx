import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import Badge from "../../../components/Badge";
import Section from "../../../components/Section";
import { readingTime, sourceLabel } from "../../../lib/format";
import { getArticle } from "../../../services/api";

type NewsPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export async function generateMetadata({
  params,
}: NewsPageProps): Promise<Metadata> {
  const { id } = await params;

  try {
    const article = await getArticle(id);

    return { title: article.title, description: article.summary };
  } catch {
    return { title: "Article not found" };
  }
}

export default async function NewsPage({ params }: NewsPageProps) {
  const { id } = await params;

  let article;

  try {
    article = await getArticle(id);
  } catch {
    notFound();
  }

  const source = sourceLabel(article);
  const minutes = readingTime(article.content);

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
          <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
            <p className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
              {source ?? "Unattributed"}
            </p>

            <p className="shrink-0 font-mono text-xs tracking-tight text-ink-faint">
              {minutes} min read
            </p>
          </div>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-ink sm:text-5xl">
            {article.title}
          </h1>

          <p className="mt-6 text-xl leading-8 text-ink-muted">
            {article.summary}
          </p>
        </header>

        {/* The takeaway leads. It's the reason someone opened this page —
            burying it under the full text makes them scroll for the payoff. */}
        <Section title="Takeaway">
          <div className="overflow-hidden rounded-3xl border border-rule bg-card shadow-sm">
            <div className="border-l-2 border-l-ink p-8">
              <p className="text-xl font-medium leading-8 text-ink">
                {article.takeaway}
              </p>
            </div>
          </div>
        </Section>

        <Section title="Article">
          <p className="text-lg leading-8 text-ink-muted">{article.content}</p>
        </Section>

        <Section title="Background">
          <p className="text-lg leading-8 text-ink-muted">
            {article.background}
          </p>
        </Section>

        {article.concepts.length > 0 && (
          <Section title="Concepts" meta={`${article.concepts.length} tagged`}>
            <div className="flex flex-wrap gap-2">
              {article.concepts.map((concept) => (
                <Badge key={concept} text={concept} />
              ))}
            </div>
          </Section>
        )}

        <Section title="Sources">
          <ul className="space-y-3">
            {article.sources.map((source) => (
              <li key={source.url}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-baseline gap-2 font-medium text-ink transition-colors hover:text-ink-muted"
                >
                  <span className="underline underline-offset-4">
                    {source.name}
                  </span>

                  <span
                    aria-hidden="true"
                    className="text-ink-faint transition-transform duration-300 group-hover:-translate-y-0.5"
                  >
                    ↗
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </Section>

        {article.relatedNews.length > 0 && (
          <Section title="Related">
            <div className="space-y-3">
              {article.relatedNews.map((item) => (
                <Link
                  key={item.id}
                  href={`/news/${item.id}`}
                  className="group flex items-baseline justify-between gap-4 rounded-2xl border border-rule bg-card p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
                >
                  <span className="font-medium text-ink transition-colors group-hover:text-ink-muted">
                    {item.title}
                  </span>

                  <span
                    aria-hidden="true"
                    className="shrink-0 text-ink-faint transition-transform duration-300 group-hover:translate-x-1"
                  >
                    →
                  </span>
                </Link>
              ))}
            </div>
          </Section>
        )}
      </article>
    </main>
  );
}
