import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const { usePathname } = vi.hoisted(() => ({ usePathname: vi.fn() }));

vi.mock("next/navigation", () => ({ usePathname }));

import NavBar from "../../components/NavBar";

describe("NavBar", () => {
  it("marks Home as active on the homepage", () => {
    usePathname.mockReturnValue("/");
    render(<NavBar />);

    expect(screen.getByRole("link", { name: "Home" })).toHaveClass(
      "text-gray-900",
    );
    expect(screen.getByRole("link", { name: "Search" })).toHaveClass(
      "text-gray-500",
    );
  });

  it("marks Search as active on the search page", () => {
    usePathname.mockReturnValue("/search");
    render(<NavBar />);

    expect(screen.getByRole("link", { name: "Search" })).toHaveClass(
      "text-gray-900",
    );
    expect(screen.getByRole("link", { name: "Home" })).toHaveClass(
      "text-gray-500",
    );
  });

  it("marks neither link active on an unrelated route", () => {
    usePathname.mockReturnValue("/news/some-article");
    render(<NavBar />);

    expect(screen.getByRole("link", { name: "Home" })).toHaveClass(
      "text-gray-500",
    );
    expect(screen.getByRole("link", { name: "Search" })).toHaveClass(
      "text-gray-500",
    );
  });
});
