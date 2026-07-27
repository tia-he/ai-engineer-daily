"use client";

import { FormEvent, useState } from "react";

import EmptyState from "../../components/EmptyState";
import NewsCard from "../../components/NewsCard";
import NewsCardSkeleton from "../../components/NewsCardSkeleton";
import { searchNews } from "../../services/api";
import { SearchResult } from "../../types/article";

function SearchIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-5 w-5"
    >
      <circle cx="11" cy="11" r="7" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runSearch(searchQuery: string) {
    setIsLoading(true);
    setError(null);

    try {
      const data = await searchNews(searchQuery);

      setResults(data);
      setHasSearched(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSearch(event: FormEvent) {
    event.preventDefault();

    const trimmed = query.trim();

    if (!trimmed) {
      return;
    }

    await runSearch(trimmed);
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl">
        <header>
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Search
          </h1>

          <p className="mt-4 max-w-2xl text-xl leading-8 text-gray-600">
            Find AI news by title, summary, takeaway, or concept.
          </p>
        </header>

        <form onSubmit={handleSearch} className="mt-12 flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search articles..."
            className="w-full rounded-full border border-gray-200 bg-white px-6 py-4 text-base text-gray-900 shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
          />

          <button
            type="submit"
            className="shrink-0 rounded-full bg-gray-900 px-8 py-4 text-sm font-semibold text-white transition-all duration-300 hover:bg-gray-700 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2"
          >
            Search
          </button>
        </form>

        <section className="mt-16">
          {isLoading && (
            <div className="space-y-5">
              <NewsCardSkeleton />
              <NewsCardSkeleton />
              <NewsCardSkeleton />
            </div>
          )}

          {error && (
            <div className="flex items-center justify-between gap-4 rounded-2xl border border-red-200 bg-red-50 px-6 py-4">
              <p className="text-sm font-medium text-red-700">{error}</p>

              <button
                type="button"
                onClick={() => runSearch(query.trim())}
                className="shrink-0 rounded-full border border-red-200 bg-white px-4 py-2 text-sm font-semibold text-red-700 transition-colors duration-300 hover:bg-red-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-700 focus-visible:ring-offset-2"
              >
                Retry
              </button>
            </div>
          )}

          {!isLoading && !error && hasSearched && (
            <>
              {results.length > 0 ? (
                <>
                  <div className="flex items-end justify-between border-b border-gray-200 pb-5">
                    <div>
                      <h2 className="text-3xl font-semibold tracking-tight text-gray-900">
                        Results
                      </h2>

                      <p className="mt-2 text-gray-600">
                        {results.length}{" "}
                        {results.length === 1 ? "story" : "stories"} found
                      </p>
                    </div>
                  </div>

                  <div className="mt-6 space-y-5">
                    {results.map((item, index) => (
                      <NewsCard
                        key={item.id}
                        id={item.id}
                        number={index + 1}
                        title={item.title}
                        summary={item.summary}
                        matchedIn={item.matchedIn}
                      />
                    ))}
                  </div>
                </>
              ) : (
                <EmptyState
                  icon={<SearchIcon />}
                  title="No matching stories"
                  description={`We couldn't find anything for "${query}". Try a different keyword or concept.`}
                />
              )}
            </>
          )}
        </section>
      </div>
    </main>
  );
}
