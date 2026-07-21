import NewsCard from "../components/NewsCard";
import { news } from "../data/news";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-20 pt-24">
      <div className="mx-auto w-full max-w-3xl">
        {/* Header */}
        <header>
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            AI Engineer Daily
          </h1>

          <p className="mt-4 max-w-2xl text-xl leading-8 text-gray-600">
            Stay ahead in AI and software engineering.
          </p>

          <p className="mt-3 text-sm font-medium text-gray-500">
            Tuesday · July 21, 2026
          </p>
        </header>

        {/* Daily Brief */}
        <section className="mt-16">
          <div className="flex items-end justify-between border-b border-gray-200 pb-5">
            <div>
              <h2 className="text-3xl font-semibold tracking-tight text-gray-900">
                Today&apos;s Brief
              </h2>

              <p className="mt-2 text-gray-600">
                {news.length} stories selected for today
              </p>
            </div>
          </div>

          <div className="mt-6 space-y-5">
            {news.map((item, index) => (
              <NewsCard
                key={item.id}
                id={item.id}
                number={index + 1}
                title={item.title}
                summary={item.summary}
              />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}