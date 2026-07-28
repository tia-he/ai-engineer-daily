"use client";

import { FormEvent, useState } from "react";

import NewsCard from "../../components/NewsCard";
import { publishedLabel, readingTime, sourceLabel } from "../../lib/format";
import { searchNews } from "../../services/api";
import { SearchResult } from "../../types/article";

const SUGGESTIONS = ["agents", "MCP", "code generation", "fine-tuning"];

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [submitted, setSubmitted] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runSearch(raw: string) {
    const trimmed = raw.trim();

    if (!trimmed) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await searchNews(trimmed);

      setResults(data);
      setSubmitted(trimmed);
      setHasSearched(true);
    } catch {
      setError(
        "The search service didn't respond. Check that the backend is running, then try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    runSearch(query);
  }

  function handleSuggestion(term: string) {
    setQuery(term);
    runSearch(term);
  }

  return (
    <main className="px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl">
        <header>
          <p className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
            Archive
          </p>

          <h1 className="mt-3 text-5xl font-bold tracking-tight text-ink">
            Search
          </h1>

          <p className="mt-3 max-w-2xl text-xl leading-8 text-ink-muted">
            Find AI news by title, summary, takeaway, or concept.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="mt-12">
          <label htmlFor="search-query" className="sr-only">
            Search articles
          </label>

          <div className="flex flex-col gap-3 sm:flex-row">
            <input
              id="search-query"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search articles"
              className="w-full rounded-full border border-rule bg-card px-6 py-4 text-base text-ink shadow-sm placeholder:text-ink-faint focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink"
            />

            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="shrink-0 rounded-full bg-ink px-8 py-4 text-sm font-semibold text-surface transition-opacity hover:opacity-80 disabled:opacity-40"
            >
              {isLoading ? "Searching" : "Search"}
            </button>
          </div>
        </form>

        <section className="mt-12" aria-live="polite">
          {!hasSearched && !isLoading && !error && (
            <div className="rounded-3xl border border-rule bg-card p-7 shadow-sm">
              <p className="text-base leading-7 text-ink">
                Search every brief published so far.
              </p>

              <p className="mt-2 text-base leading-7 text-ink-muted">
                Start with a topic:
              </p>

              <div className="mt-4 flex flex-wrap gap-2">
                {SUGGESTIONS.map((term) => (
                  <button
                    key={term}
                    type="button"
                    onClick={() => handleSuggestion(term)}
                    className="rounded-full border border-rule bg-accent-soft px-3 py-1 font-mono text-xs tracking-tight text-ink-muted transition-colors hover:text-ink"
                  >
                    {term}
                  </button>
                ))}
              </div>
            </div>
          )}

          {isLoading && (
            <div className="space-y-5">
              {[0, 1, 2].map((row) => (
                <div
                  key={row}
                  className="animate-pulse rounded-3xl border border-rule bg-card p-7 shadow-sm"
                >
                  <div className="h-3 w-24 rounded-full bg-accent-soft" />
                  <div className="mt-5 h-6 w-3/4 rounded-full bg-accent-soft" />
                  <div className="mt-4 h-4 w-full rounded-full bg-accent-soft" />
                  <div className="mt-2 h-4 w-2/3 rounded-full bg-accent-soft" />
                </div>
              ))}
            </div>
          )}

          {error && !isLoading && (
            <div className="rounded-3xl border border-rule bg-card p-7 shadow-sm">
              <p className="text-base leading-7 text-ink">Search failed</p>

              <p className="mt-2 text-base leading-7 text-ink-muted">{error}</p>
            </div>
          )}

          {!isLoading && !error && hasSearched && (
            <>
              <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-rule pb-4">
                <h2 className="text-2xl font-semibold tracking-tight text-ink">
                  Results
                </h2>

                <span className="shrink-0 font-mono text-xs uppercase tracking-[0.14em] text-ink-faint">
                  {results.length}{" "}
                  {results.length === 1 ? "story" : "stories"}
                </span>
              </div>

              {results.length === 0 ? (
                <div className="mt-6 rounded-3xl border border-rule bg-card p-7 shadow-sm">
                  <p className="text-base leading-7 text-ink">
                    Nothing matched &ldquo;{submitted}&rdquo;.
                  </p>

                  <p className="mt-2 text-base leading-7 text-ink-muted">
                    Search covers titles, summaries, takeaways, and concepts.
                    Try a broader term:
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    {SUGGESTIONS.map((term) => (
                      <button
                        key={term}
                        type="button"
                        onClick={() => handleSuggestion(term)}
                        className="rounded-full border border-rule bg-accent-soft px-3 py-1 font-mono text-xs tracking-tight text-ink-muted transition-colors hover:text-ink"
                      >
                        {term}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="mt-6 space-y-5">
                  {results.map((item) => (
                    <NewsCard
                      key={item.id}
                      id={item.id}
                      title={item.title}
                      summary={item.summary}
                      source={sourceLabel(item)}
                      date={publishedLabel(item)}
                      imageUrl={item.imageUrl}
                      readMinutes={readingTime(item.content)}
                      matchedIn={item.matchedIn}
                    />
                  ))}
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </main>
  );
}
