import { Article, SearchResult } from "../types/article";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function getNews(): Promise<Article[]> {
  const response = await fetch(`${API_BASE_URL}/news`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch news.");
  }

  return response.json();
}

export async function getArticle(id: string): Promise<Article> {
  const response = await fetch(`${API_BASE_URL}/news/${id}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Article not found.");
  }

  return response.json();
}

export async function searchNews(query: string): Promise<SearchResult[]> {
  // Relative path (proxied by the rewrite in next.config.ts) so this
  // client-side fetch stays same-origin and isn't blocked by CORS.
  const response = await fetch(
    `/api/search?q=${encodeURIComponent(query)}`,
    { cache: "no-store" },
  );

  if (!response.ok) {
    throw new Error("Search failed.");
  }

  return response.json();
}