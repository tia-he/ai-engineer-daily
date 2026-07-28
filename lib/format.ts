import { Article } from "../types/article";

/**
 * These helpers only derive things the data actually supports: where a
 * story came from, how long it is, and — when the source feed provided
 * one — when it was published. A missing `publishedAt` renders as no date
 * at all, never a fabricated or "today" placeholder.
 */

/** Publisher of record for a story — the label the brief scans on. */
export function sourceLabel(article: Pick<Article, "sources">): string | null {
  return article.sources?.[0]?.name ?? null;
}

/** Compact "JUL 27" label from the real publish date. `null` when the source feed didn't provide one. */
export function publishedLabel(
  article: Pick<Article, "publishedAt">,
): string | null {
  if (!article.publishedAt) {
    return null;
  }

  const date = new Date(article.publishedAt);

  if (Number.isNaN(date.getTime())) {
    return null;
  }

  return date
    .toLocaleDateString("en-US", { month: "short", day: "numeric" })
    .toUpperCase();
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
