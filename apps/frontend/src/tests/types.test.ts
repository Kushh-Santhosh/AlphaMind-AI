/**
 * AlphaMind AI — Shared Type Definitions Unit Tests
 */

import { describe, it, expect } from "vitest";
import type { PredictionSafetyPayload, UserRole } from "@/lib/types";

describe("PredictionSafetyPayload type contract", () => {
  it("should accept a valid prediction payload", () => {
    const payload: PredictionSafetyPayload = {
      asset: "AAPL",
      predictionHorizonDays: 30,
      probabilityDistribution: {
        bullScenarioPct: 25,
        baseScenarioPct: 60,
        bearScenarioPct: 15,
      },
      confidenceInterval95: {
        lowerBoundPct: -5.2,
        expectedReturnPct: 4.5,
        upperBoundPct: 12.1,
      },
      modelConfidenceScore: 0.82,
      dataQualityScore: 0.94,
      predictionExpiryTimestamp: "2026-09-04T18:30:00Z",
      supportingEvidence: ["Strong Q2 earnings"],
      contradictingEvidence: ["Antitrust risk"],
      knownUnknowns: ["DOJ verdict pending"],
      historicalModelAccuracyBrierScore: 0.14,
      disclaimer: "For informational purposes only.",
    };

    expect(payload.asset).toBe("AAPL");
    expect(payload.predictionHorizonDays).toBe(30);
    expect(payload.probabilityDistribution.bullScenarioPct).toBe(25);
    expect(payload.disclaimer).toContain("informational");
  });

  it("should enforce UserRole literals", () => {
    const roles: UserRole[] = ["guest", "trader", "quant_analyst", "admin"];
    expect(roles).toHaveLength(4);
    expect(roles).toContain("admin");
  });
});

describe("API client module", () => {
  it("should export apiClient with expected keys", async () => {
    const { apiClient } = await import("@/lib/api");
    expect(apiClient).toHaveProperty("health");
    expect(apiClient).toHaveProperty("market");
    expect(apiClient).toHaveProperty("research");
    expect(typeof apiClient.market.search).toBe("function");
  });
});
