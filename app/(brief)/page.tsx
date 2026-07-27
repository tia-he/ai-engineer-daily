import Link from "next/link";

import NewsCard from "../../components/NewsCard";
import { distinctSources, readingTime, sourceLabel, todayLabel } from "../../lib/format";
import { getNews } from "../../services/api";

export default async function Home() {
  let news;

  try {
    news = await getNews();
  } catch {
    news = null;
  }

  const sources = news ? distinctSources(news) : [];

  return (
    <main className="px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl">
        <header>
          <p className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
            {todayLabel()}
          </p>

          <h1 className="mt-3 text-5xl font-bold tracking-tight text-ink">
            AI Engineer Daily
          </h1>

          <p className="mt-3 max-w-2xl text-xl leading-8 text-ink-muted">
            Stay ahead in AI and software engineering.
          </p>
        </header>

        <section className="mt-12">
          <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-rule pb-4">
            <h2 className="text-2xl font-semibold tracking-tight text-ink">
              Today&rsquo;s Brief
            </h2>

            {news && news.length > 0 ? (
              <span className="shrink-0 font-mono text-xs uppercase tracking-[0.14em] text-ink-faint">
                {news.length} {news.length === 1 ? "story" : "stories"} ·{" "}
                {sources.length}{" "}
                {sources.length === 1 ? "source" : "sources"}
              </span>
            ) : null}
          </div>

          {news === null ? (
            <div className="mt-6 rounded-3xl border border-rule bg-card p-7 shadow-sm">
              <p className="text-base leading-7 text-ink">
                The brief couldn&rsquo;t be loaded.
              </p>

              <p className="mt-2 text-base leading-7 text-ink-muted">
                The API isn&rsquo;t responding. Start the backend with{" "}
                <code className="font-mono text-sm text-ink">
                  uvicorn main:app --reload
                </code>{" "}
                and reload this page.
              </p>
            </div>
          ) : news.length === 0 ? (
            <div className="mt-6 rounded-3xl border border-rule bg-card p-7 shadow-sm">
              <p className="text-base leading-7 text-ink">
                No stories yet today.
              </p>

              <p className="mt-2 text-base leading-7 text-ink-muted">
                Ingestion runs on a schedule. In the meantime you can{" "}
                <Link
                  href="/search"
                  className="font-medium text-ink underline underline-offset-4"
                >
                  search the archive
                </Link>
                .
              </p>
            </div>
          ) : (
            <div className="mt-6 space-y-5">
              {news.map((item) => (
                <NewsCard
                  key={item.id}
                  id={item.id}
                  title={item.title}
                  summary={item.summary}
                  source={sourceLabel(item)}
                  readMinutes={readingTime(item.content)}
                  concepts={item.concepts}
                />
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
