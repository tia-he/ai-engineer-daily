import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Badge from "../../components/Badge";

describe("Badge", () => {
  it("renders the given text", () => {
    render(<Badge text="LLM" />);

    expect(screen.getByText("LLM")).toBeInTheDocument();
  });
});
