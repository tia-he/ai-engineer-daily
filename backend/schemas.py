from pydantic import BaseModel


class Source(BaseModel):
    name: str
    url: str


class Article(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    takeaway: str

    concepts: list[str]

    background: str

    sources: list[Source]

    # Both optional: not every RSS source carries a publish date or a cover
    # image, so a missing one is `None` rather than a fabricated value.
    publishedAt: str | None = None

    imageUrl: str | None = None


class SearchResult(Article):
    matchedIn: list[str]
