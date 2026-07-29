import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const { searchNews } = vi.hoisted(() => ({ searchNews: vi.fn() }));

vi.mock("../../services/api", () => ({ searchNews }));

import SearchPage from "../../app/search/page";

function typeQuery(value: string) {
  fireEvent.change(screen.getByPlaceholderText("Search articles"), {
    target: { value },
  });
}

function submit() {
  fireEvent.click(screen.getByRole("button", { name: "Search" }));
}

beforeEach(() => {
  searchNews.mockReset();
});

describe("SearchPage", () => {
  it("shows loading skeletons while the search is in flight", async () => {
    let resolveSearch: (value: unknown) => void = () => {};
    searchNews.mockReturnValue(
      new Promise((resolve) => {
        resolveSearch = resolve;
      }),
    );

    render(<SearchPage />);
    typeQuery("MCP");
    submit();

    expect(document.querySelectorAll(".animate-pulse")).toHaveLength(3);

    resolveSearch([]);
    await waitFor(() =>
      expect(document.querySelectorAll(".animate-pulse")).toHaveLength(0),
    );
  });

  it("renders results when the search succeeds", async () => {
    searchNews.mockResolvedValue([
      {
        id: "openai-coding-model",
        title: "OpenAI Releases New Coding Model",
        summary: "A new model optimized for software engineering tasks.",
        content: "",
        takeaway: "",
        concepts: [],
        background: "",
        sources: [],
        matchedIn: ["Title"],
      },
    ]);

    render(<SearchPage />);
    typeQuery("coding");
    submit();

    expect(
      await screen.findByText("OpenAI Releases New Coding Model"),
    ).toBeInTheDocument();
    expect(screen.getByText("1 story")).toBeInTheDocument();
    expect(screen.getByText("matched in Title")).toBeInTheDocument();
  });

  it("shows an empty state when there are no results", async () => {
    searchNews.mockResolvedValue([]);

    render(<SearchPage />);
    typeQuery("zzzznomatch");
    submit();

    expect(
      await screen.findByText((content) =>
        content.startsWith("Nothing matched") && content.includes("zzzznomatch"),
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Search covers titles, summaries, takeaways, and concepts. Try a broader term:",
      ),
    ).toBeInTheDocument();
  });

  it("shows an error callout and recovers on a successful retry", async () => {
    searchNews.mockRejectedValueOnce(new Error("network down"));

    render(<SearchPage />);
    typeQuery("MCP");
    submit();

    expect(await screen.findByText("Search failed")).toBeInTheDocument();
    expect(
      screen.getByText(
        "The search service didn't respond. Check that the backend is running, then try again.",
      ),
    ).toBeInTheDocument();

    searchNews.mockResolvedValueOnce([]);
    submit();

    expect(
      await screen.findByText((content) => content.startsWith("Nothing matched")),
    ).toBeInTheDocument();
    expect(searchNews).toHaveBeenCalledTimes(2);
  });

  it("does not search on submit when the query is blank", () => {
    render(<SearchPage />);
    submit();

    expect(searchNews).not.toHaveBeenCalled();
  });
});
