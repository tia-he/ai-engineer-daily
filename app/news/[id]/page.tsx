import Link from "next/link";
import { notFound } from "next/navigation";
import { news } from "../../../data/news";

type NewsPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function NewsPage({ params }: NewsPageProps) {
  const { id } = await params;

  const article = news.find((item) => item.id === id);

  if (!article) {
    notFound();
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-24 pt-16">
      <article className="mx-auto w-full max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center text-sm font-semibold text-gray-600 transition-colors hover:text-gray-900"
        >
          ← Back to today&apos;s brief
        </Link>

        <header className="mt-12 border-b border-gray-200 pb-10">
          <p className="text-sm font-semibold uppercase tracking-widest text-gray-500">
            AI Engineer Daily
          </p>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            {article.title}
          </h1>

          <p className="mt-6 text-xl leading-8 text-gray-600">
            {article.summary}
          </p>

          <p className="mt-5 text-sm text-gray-500">
            July 21, 2026 · 2 min read
          </p>
        </header>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold tracking-tight text-gray-900">
            Article
          </h2>

          <p className="mt-5 text-lg leading-8 text-gray-700">
            {article.content}
          </p>
        </section>

        <section className="mt-12 rounded-3xl bg-white p-8 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-widest text-gray-500">
            Takeaway
          </p>

          <p className="mt-4 text-xl font-medium leading-8 text-gray-900">
            {article.takeaway}
          </p>
        </section>

        <section className="mt-12 border-t border-gray-200 pt-10">
          <h2 className="text-2xl font-semibold tracking-tight text-gray-900">
            Sources
          </h2>

          <ul className="mt-5 space-y-3">
            {article.sources.map((source) => (
              <li key={source.url}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center font-medium text-gray-700 transition-colors hover:text-gray-900 hover:underline"
                >
                  {source.name}
                  <span className="ml-2">↗</span>
                </a>
              </li>
            ))}
          </ul>
        </section>
      </article>
    </main>
  );
}