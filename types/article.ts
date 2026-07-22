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
}