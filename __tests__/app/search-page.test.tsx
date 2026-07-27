import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const { searchNews } = vi.hoisted(() => ({ searchNews: vi.fn() }));

vi.mock("../../services/api", () => ({ searchNews }));

import SearchPage from "../../app/search/page";

function typeQuery(value: string) {
  fireEvent.change(screen.getByPlaceholderText("Search articles..."), {
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
        relatedNews: [],
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
    expect(screen.getByText("1 story found")).toBeInTheDocument();
    expect(screen.getByText("Matched in Title")).toBeInTheDocument();
  });

  it("shows an empty state when there are no results", async () => {
    searchNews.mockResolvedValue([]);

    render(<SearchPage />);
    typeQuery("zzzznomatch");
    submit();

    expect(await screen.findByText("No matching stories")).toBeInTheDocument();
    expect(
      screen.getByText('We couldn\'t find anything for "zzzznomatch". Try a different keyword or concept.'),
    ).toBeInTheDocument();
  });

  it("shows an error callout with a working retry on failure", async () => {
    searchNews.mockRejectedValueOnce(new Error("network down"));

    render(<SearchPage />);
    typeQuery("MCP");
    submit();

    expect(
      await screen.findByText("Something went wrong. Please try again."),
    ).toBeInTheDocument();

    searchNews.mockResolvedValueOnce([]);
    fireEvent.click(screen.getByRole("button", { name: "Retry" }));

    expect(await screen.findByText("No matching stories")).toBeInTheDocument();
    expect(searchNews).toHaveBeenCalledTimes(2);
  });

  it("does not search on submit when the query is blank", () => {
    render(<SearchPage />);
    submit();

    expect(searchNews).not.toHaveBeenCalled();
  });
});
