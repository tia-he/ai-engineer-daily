from pydantic import BaseModel


class Source(BaseModel):
    name: str
    url: str


class RelatedNews(BaseModel):
    id: str
    title: str


class Article(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    takeaway: str

    concepts: list[str]

    background: str

    relatedNews: list[RelatedNews]

    sources: list[Source]