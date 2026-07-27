import EmptyState from "../components/EmptyState";
import NewsCard from "../components/NewsCard";
import { getNews } from "../services/api";

function InboxIcon() {
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
      <path d="M22 12h-6l-2 3h-4l-2-3H2" />
      <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11Z" />
    </svg>
  );
}

export default async function Home() {
  const news = await getNews();

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

              <p className="mt-2 text-gray-600">
                {news.length} stories selected for today
              </p>
            </div>
          </div>

          {news.length > 0 ? (
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
          ) : (
            <div className="mt-6">
              <EmptyState
                icon={<InboxIcon />}
                title="No stories yet"
                description="Check back soon — new AI engineering stories are added regularly."
              />
            </div>
          )}
        </section>
      </div>
    </main>
  );
}