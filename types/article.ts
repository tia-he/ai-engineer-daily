export interface Source {
  name: string;
  url: string;
}

export interface RelatedNews {
  id: string;
  title: string;
}

export interface Article {
  id: string;

  title: string;

  summary: string;

  content: string;

  takeaway: string;

  concepts: string[];

  background: string;

  relatedNews: RelatedNews[];

  sources: Source[];

  /** Real publish date from the source feed. `null` when the feed didn't provide one — never fabricated. */
  publishedAt: string | null;

  /** Cover image scraped from the source feed. `null` when the feed didn't provide one — never a placeholder. */
  imageUrl: string | null;
}

export interface SearchResult extends Article {
  matchedIn: string[];
}