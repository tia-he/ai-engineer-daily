import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import NewsCard from "../../components/NewsCard";

describe("NewsCard", () => {
  it("renders the title and summary", () => {
    render(
      <NewsCard
        id="openai-coding-model"
        title="OpenAI Releases New Coding Model"
        summary="A new model optimized for software engineering tasks."
      />,
    );

    expect(
      screen.getByRole("heading", { name: /OpenAI Releases New Coding Model/ }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("A new model optimized for software engineering tasks."),
    ).toBeInTheDocument();
  });

  it("links to the article's detail page", () => {
    render(<NewsCard id="openai-coding-model" title="Title" summary="Summary" />);

    expect(screen.getByRole("link")).toHaveAttribute(
      "href",
      "/news/openai-coding-model",
    );
  });

  it("falls back to 'Unattributed' when no source is given", () => {
    render(<NewsCard id="a" title="Title" summary="Summary" />);

    expect(screen.getByText("Unattributed")).toBeInTheDocument();
  });

  it("renders the source and read time when given", () => {
    render(
      <NewsCard
        id="a"
        title="Title"
        summary="Summary"
        source="OpenAI"
        readMinutes={4}
      />,
    );

    expect(screen.getByText("OpenAI")).toBeInTheDocument();
    expect(screen.getByText("4 min")).toBeInTheDocument();
  });

  it("does not render badges when concepts and matchedIn are absent", () => {
    render(<NewsCard id="a" title="Title" summary="Summary" />);

    expect(screen.queryByText(/matched in/)).not.toBeInTheDocument();
  });

  it("renders up to 3 concept badges", () => {
    render(
      <NewsCard
        id="a"
        title="Title"
        summary="Summary"
        concepts={["LLM", "Code Generation", "Repository", "Extra"]}
      />,
    );

    expect(screen.getByText("LLM")).toBeInTheDocument();
    expect(screen.getByText("Code Generation")).toBeInTheDocument();
    expect(screen.getByText("Repository")).toBeInTheDocument();
    expect(screen.queryByText("Extra")).not.toBeInTheDocument();
  });

  it("renders a badge per matched field when matchedIn is present", () => {
    render(
      <NewsCard
        id="a"
        title="Title"
        summary="Summary"
        matchedIn={["Title", "Concepts"]}
      />,
    );

    expect(screen.getByText("matched in Title")).toBeInTheDocument();
    expect(screen.getByText("matched in Concepts")).toBeInTheDocument();
  });
});
