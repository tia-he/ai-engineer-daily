import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import NewsCard from "../../components/NewsCard";

describe("NewsCard", () => {
  it("renders the title and summary", () => {
    render(
      <NewsCard
        id="openai-coding-model"
        number={1}
        title="OpenAI Releases New Coding Model"
        summary="A new model optimized for software engineering tasks."
      />,
    );

    expect(
      screen.getByRole("heading", { name: "OpenAI Releases New Coding Model" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("A new model optimized for software engineering tasks."),
    ).toBeInTheDocument();
  });

  it("links to the article's detail page", () => {
    render(
      <NewsCard
        id="openai-coding-model"
        number={1}
        title="Title"
        summary="Summary"
      />,
    );

    expect(screen.getByRole("link")).toHaveAttribute(
      "href",
      "/news/openai-coding-model",
    );
  });

  it("pads single-digit numbers with a leading zero", () => {
    render(<NewsCard id="a" number={3} title="Title" summary="Summary" />);

    expect(screen.getByText("03")).toBeInTheDocument();
  });

  it("does not render match badges when matchedIn is absent", () => {
    render(<NewsCard id="a" number={1} title="Title" summary="Summary" />);

    expect(screen.queryByText(/Matched in/)).not.toBeInTheDocument();
  });

  it("renders a badge per matched field when matchedIn is present", () => {
    render(
      <NewsCard
        id="a"
        number={1}
        title="Title"
        summary="Summary"
        matchedIn={["Title", "Concepts"]}
      />,
    );

    expect(screen.getByText("Matched in Title")).toBeInTheDocument();
    expect(screen.getByText("Matched in Concepts")).toBeInTheDocument();
  });
});
