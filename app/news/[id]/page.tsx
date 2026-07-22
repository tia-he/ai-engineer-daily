import Link from "next/link";
import { notFound } from "next/navigation";

import Badge from "../../../components/Badge";
import Section from "../../../components/Section";
import { getArticle } from "../../../services/api";

type NewsPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function NewsPage({ params }: NewsPageProps) {
  const { id } = await params;

  let article;

  try {
    article = await getArticle(id);
  } catch {
    notFound();
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-24 pt-16">
      <article className="mx-auto w-full max-w-3xl">
        {/* Back Button */}
        <Link
          href="/"
          className="inline-flex items-center text-sm font-semibold text-gray-600 transition-colors hover:text-gray-900"
        >
          ← Back to Today's Brief
        </Link>

        {/* Header */}
        <header className="mt-12 border-b border-gray-200 pb-10">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
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

        {/* Article */}
        <Section title="Article">
          <p className="text-lg leading-8 text-gray-700">
            {article.content}
          </p>
        </Section>

        {/* Takeaway */}
        <Section title="Takeaway">
          <div className="rounded-3xl bg-white p-8 shadow-sm">
            <p className="text-xl font-medium leading-8 text-gray-900">
              {article.takeaway}
            </p>
          </div>
        </Section>

        {/* Concepts */}
        <Section title="Concepts">
          <div className="flex flex-wrap gap-3">
            {article.concepts.map((concept) => (
              <Badge key={concept} text={concept} />
            ))}
          </div>
        </Section>

        {/* Background */}
        <Section title="Background">
          <p className="text-lg leading-8 text-gray-700">
            {article.background}
          </p>
        </Section>

        {/* Related News */}
        <Section title="Related News">
          <div className="space-y-4">
            {article.relatedNews.map((item) => (
              <div
                key={item.id}
                className="rounded-2xl border border-gray-200 bg-white p-5 transition-all duration-300 hover:shadow-md"
              >
                <p className="font-semibold text-gray-900">
                  {item.title}
                </p>

                <p className="mt-2 text-sm text-gray-500">
                  Coming soon
                </p>
              </div>
            ))}
          </div>
        </Section>

        {/* Sources */}
        <Section title="Sources">
          <ul className="space-y-3">
            {article.sources.map((source) => (
              <li key={source.url}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center font-medium text-gray-700 transition-colors hover:text-gray-900 hover:underline"
                >
                  {source.name}

                  <span className="ml-2">
                    ↗
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </Section>
      </article>
    </main>
  );
}