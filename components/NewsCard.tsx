import Link from "next/link";

import Badge from "./Badge";

type NewsCardProps = {
  id: string;
  number: number;
  title: string;
  summary: string;
  matchedIn?: string[];
};

export default function NewsCard({
  id,
  number,
  title,
  summary,
  matchedIn,
}: NewsCardProps) {
  return (
    <Link
      href={`/news/${id}`}
      className="group block rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
    >
      <article className="flex gap-5">
        <span className="pt-1 text-sm font-semibold text-gray-400">
          {String(number).padStart(2, "0")}
        </span>

        <div className="min-w-0 flex-1">
          <h3 className="text-2xl font-semibold tracking-tight text-gray-900 transition-colors group-hover:text-gray-600">
            {title}
          </h3>

          <p className="mt-3 text-base leading-7 text-gray-600">
            {summary}
          </p>

          {matchedIn && matchedIn.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {matchedIn.map((field) => (
                <Badge key={field} text={`Matched in ${field}`} />
              ))}
            </div>
          )}

          <p className="mt-5 text-sm font-semibold text-gray-900">
            Read article
            <span className="ml-2 inline-block transition-transform duration-300 group-hover:translate-x-1">
              →
            </span>
          </p>
        </div>
      </article>
    </Link>
  );
}