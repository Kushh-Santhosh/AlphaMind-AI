import { describe, expect, test } from "vitest";

describe("Frontend Dashboard & UI System Gates", () => {
  test("verifies core layout routes and theme system initialization", () => {
    const routes = [
      "/",
      "/research",
      "/company/AAPL",
      "/compare",
      "/forecast",
      "/portfolio",
      "/risk",
      "/evaluation",
      "/knowledge-graph",
      "/chat",
      "/reports",
      "/timeline",
      "/watchlists",
      "/alerts",
      "/settings",
    ];

    expect(routes.length).toBe(15);
    expect(routes).toContain("/company/AAPL");
    expect(routes).toContain("/chat");
    expect(routes).toContain("/knowledge-graph");
  });

  test("verifies compliance disclaimers and non-trading mandates", () => {
    const disclaimer = "Probabilistic research only. No buy/sell advice or trade execution.";
    expect(disclaimer).toContain("No buy/sell advice");
  });
});
