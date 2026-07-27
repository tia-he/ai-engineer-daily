import NewsCardSkeleton from "../components/NewsCardSkeleton";

export default function Loading() {
  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl">
        <header>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
            Daily Briefing
          </p>

          <h1 className="mt-4 text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            AI Engineer Daily
          </h1>

          <p className="mt-4 max-w-2xl text-xl leading-8 text-gray-600">
            Stay ahead in AI and software engineering.
          </p>
        </header>

        <section className="mt-16">
          <div className="flex items-end justify-between border-b border-gray-200 pb-5">
            <div>
              <h2 className="text-3xl font-semibold tracking-tight text-gray-900">
                Today&apos;s Brief
              </h2>

              <div className="mt-2 h-5 w-40 animate-pulse rounded bg-gray-200" />
            </div>
          </div>

          <div className="mt-6 space-y-5">
            {Array.from({ length: 4 }).map((_, index) => (
              <NewsCardSkeleton key={index} />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
