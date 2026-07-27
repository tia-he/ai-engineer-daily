import { Article } from "../types/article";

/**
 * The article schema has no `published_at` column, so a per-article date
 * would have to be invented. These helpers only derive things the data
 * actually supports: where a story came from, and how long it is.
 */

/** Publisher of record for a story — the label the brief scans on. */
export function sourceLabel(article: Pick<Article, "sources">): string | null {
  return article.sources?.[0]?.name ?? null;
}

/** Reading time from the real body copy, at a 220 wpm skim. */
export function readingTime(content: string): number {
  const words = content.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 220));
}

/** Today, spelled out. The brief is a daily surface, so "today" is honest. */
export function todayLabel(date = new Date()): string {
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

/** Distinct publishers in a set of stories, in first-seen order. */
export function distinctSources(articles: Pick<Article, "sources">[]): string[] {
  const seen = new Set<string>();

  for (const article of articles) {
    const name = sourceLabel(article);

    if (name) {
      seen.add(name);
    }
  }

  return [...seen];
}
