import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import EmptyState from "../../components/EmptyState";

describe("EmptyState", () => {
  it("renders the icon, title, and description", () => {
    render(
      <EmptyState
        icon={<svg data-testid="icon" />}
        title="No matching stories"
        description="Try a different keyword."
      />,
    );

    expect(screen.getByTestId("icon")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "No matching stories" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Try a different keyword.")).toBeInTheDocument();
  });
});
