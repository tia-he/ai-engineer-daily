"use client";

import { FormEvent, useState } from "react";

import NewsCard from "../../components/NewsCard";
import { searchNews } from "../../services/api";
import { SearchResult } from "../../types/article";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch(event: FormEvent) {
    event.preventDefault();

    const trimmed = query.trim();

    if (!trimmed) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await searchNews(trimmed);

      setResults(data);
      setHasSearched(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-20 pt-24">
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
            className="shrink-0 rounded-full bg-gray-900 px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-gray-700"
          >
            Search
          </button>
        </form>

        <section className="mt-16">
          {isLoading && (
            <p className="text-gray-600">Searching...</p>
          )}

          {error && (
            <p className="text-red-600">{error}</p>
          )}

          {!isLoading && !error && hasSearched && (
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
          )}
        </section>
      </div>
    </main>
  );
}
