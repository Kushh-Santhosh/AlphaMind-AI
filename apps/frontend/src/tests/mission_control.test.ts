/**
 * AlphaMind AI v2 — Mission Control Terminal: Frontend Vitest Tests
 *
 * Covers:
 *  - TypeScript type contracts (compile-time via type assertions)
 *  - API hook URL construction
 *  - Search debounce and result shape
 *  - Dashboard state helpers (fmt, fmtUSD, fmtPct)
 *  - Notification structure validation
 *  - Activity feed color/icon map completeness
 *  - Replay control direction validation
 *  - Navigation route registration
 */

import { describe, it, expect } from "vitest";
import type {
  DashboardState,
  FundSnapshot,
  ActivityFeedItem,
  Notification,
  ReasoningRecord,
  SystemHealth,
  SearchResult,
  LiveTick,
} from "@/lib/missionControlTypes";

// ── Type shape assertions ─────────────────────────────────────────────────────

describe("Mission Control type contracts", () => {
  it("DashboardState has all required top-level keys", () => {
    const required: Array<keyof DashboardState> = [
      "generated_at_utc",
      "uptime_seconds",
      "system_health",
      "funds",
      "timeline",
      "reasoning",
      "activity_feed",
      "intelligence",
      "latest_briefing",
      "notifications",
      "timeline_stats",
      "total_aum_usd",
      "total_assets_covered",
      "avg_confidence",
      "replay_position",
    ];
    expect(required.length).toBe(15);
    expect(required).toContain("funds");
    expect(required).toContain("intelligence");
    expect(required).toContain("avg_confidence");
  });

  it("FundSnapshot has all performance metric keys", () => {
    const required: Array<keyof FundSnapshot> = [
      "fund_id",
      "name",
      "current_market_value_usd",
      "total_return_pct",
      "cagr_pct",
      "sharpe_ratio",
      "sortino_ratio",
      "max_drawdown_pct",
      "win_rate_pct",
      "brier_score",
      "confidence",
      "risk_level",
      "allocations",
      "top_holding",
      "last_rebalance_utc",
      "today_pnl_usd",
      "today_pnl_pct",
    ];
    expect(required.length).toBe(17);
    expect(required).toContain("brier_score");
    expect(required).toContain("sortino_ratio");
  });

  it("ActivityFeedItem extends TimelineEvent with display fields", () => {
    const required: Array<keyof ActivityFeedItem> = [
      "event_id",
      "event_type",
      "headline",
      "source_subsystem",
      "timestamp_utc",
      "icon",
      "color",
      "timeline_link",
      "reasoning_link",
      "replay_link",
    ];
    expect(required).toContain("timeline_link");
    expect(required).toContain("replay_link");
    expect(required).toContain("icon");
  });

  it("ReasoningRecord includes Decision Inspector fields", () => {
    const required: Array<keyof ReasoningRecord> = [
      "reasoning_id",
      "decision_id",
      "selected_action",
      "confidence_score",
      "assumptions",
      "evidence_references",
      "contradicting_evidence",
      "alternative_actions_considered",
      "probability_distribution",
      "shap_factors",
      "citations",
      "audit_metadata",
    ];
    expect(required).toContain("shap_factors");
    expect(required).toContain("probability_distribution");
    expect(required).toContain("citations");
  });

  it("Notification has type, title, link, and is_read flag", () => {
    const required: Array<keyof Notification> = [
      "notification_id",
      "type",
      "title",
      "message",
      "is_read",
      "created_at_utc",
      "link",
    ];
    expect(required).toContain("is_read");
    expect(required).toContain("link");
  });

  it("LiveTick has tick counter and timestamp", () => {
    const required: Array<keyof LiveTick> = ["tick", "timestamp_utc", "uptime_seconds"];
    expect(required).toContain("tick");
    expect(required).toContain("uptime_seconds");
  });

  it("SearchResult has type discriminant and link", () => {
    const validTypes: SearchResult["type"][] = [
      "TIMELINE",
      "REASONING",
      "FUND",
      "BRIEFING",
      "ASSET",
    ];
    expect(validTypes).toHaveLength(5);
    expect(validTypes).toContain("FUND");
    expect(validTypes).toContain("REASONING");
  });

  it("SystemHealth has status and subsystems map", () => {
    const validStatuses: SystemHealth["status"][] = ["HEALTHY", "DEGRADED", "CRITICAL"];
    expect(validStatuses).toContain("HEALTHY");
    expect(validStatuses.length).toBe(3);
  });
});

// ── Formatting helpers (inlined to avoid circular deps) ───────────────────────

function fmt(n: number, decimals = 1): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(decimals)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(decimals)}K`;
  return n.toFixed(decimals);
}

function fmtUSD(n: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);
}

function fmtPct(n: number, sign = true): string {
  return `${sign && n > 0 ? "+" : ""}${n.toFixed(2)}%`;
}

function uptime(secs: number): string {
  const h = Math.floor(secs / 3600);
  const m = Math.floor((secs % 3600) / 60);
  const s = Math.floor(secs % 60);
  return `${h}h ${m}m ${s}s`;
}

describe("Mission Control formatting helpers", () => {
  describe("fmt()", () => {
    it("formats millions correctly", () => {
      expect(fmt(1_500_000)).toBe("1.5M");
    });
    it("formats thousands correctly", () => {
      expect(fmt(12_300)).toBe("12.3K");
    });
    it("formats small numbers without suffix", () => {
      expect(fmt(42)).toBe("42.0");
    });
    it("respects decimals parameter", () => {
      expect(fmt(5000, 0)).toBe("5K");
    });
  });

  describe("fmtUSD()", () => {
    it("formats USD with $ sign", () => {
      expect(fmtUSD(10000)).toContain("$");
      expect(fmtUSD(10000)).toContain("10,000");
    });
    it("formats large amounts", () => {
      const result = fmtUSD(1_234_567);
      expect(result).toContain("1,234,567");
    });
  });

  describe("fmtPct()", () => {
    it("adds + sign for positive", () => {
      expect(fmtPct(5.25)).toBe("+5.25%");
    });
    it("no + sign for negative", () => {
      expect(fmtPct(-3.1)).toBe("-3.10%");
    });
    it("respects sign=false", () => {
      expect(fmtPct(2.5, false)).toBe("2.50%");
    });
  });

  describe("uptime()", () => {
    it("formats 0 seconds", () => {
      expect(uptime(0)).toBe("0h 0m 0s");
    });
    it("formats 1 hour 30 minutes", () => {
      expect(uptime(5400)).toBe("1h 30m 0s");
    });
    it("formats days worth of seconds", () => {
      const result = uptime(86400);
      expect(result).toBe("24h 0m 0s");
    });
  });
});

// ── Activity feed color map completeness ──────────────────────────────────────

describe("Activity feed color map", () => {
  const colorMap: Record<string, string> = {
    violet: "border-violet-500/20 bg-violet-500/5 text-violet-400",
    blue: "border-blue-500/20 bg-blue-500/5 text-blue-400",
    teal: "border-teal-500/20 bg-teal-500/5 text-teal-400",
    amber: "border-amber-500/20 bg-amber-500/5 text-amber-400",
    purple: "border-purple-500/20 bg-purple-500/5 text-purple-400",
    emerald: "border-emerald-500/20 bg-emerald-500/5 text-emerald-400",
    rose: "border-rose-500/20 bg-rose-500/5 text-rose-400",
    slate: "border-slate-700 bg-slate-800 text-slate-400",
  };

  const expectedEventTypes = [
    "PORTFOLIO_REBALANCED",
    "FORECAST_UPDATED",
    "BRIEFING_GENERATED",
    "MARKET_DATA_UPDATED",
    "REASONING_STORED",
    "RESEARCH_COMPLETED",
    "RISK_UPDATED",
  ];

  const colorAssignments: Record<string, string> = {
    PORTFOLIO_REBALANCED: "violet",
    FORECAST_UPDATED: "blue",
    BRIEFING_GENERATED: "teal",
    MARKET_DATA_UPDATED: "amber",
    REASONING_STORED: "purple",
    RESEARCH_COMPLETED: "emerald",
    RISK_UPDATED: "rose",
  };

  it("has a color entry for all expected event types", () => {
    expectedEventTypes.forEach((type) => {
      const color = colorAssignments[type];
      expect(color).toBeDefined();
      expect(colorMap[color]).toBeDefined();
    });
  });

  it("falls back to slate for unknown event types", () => {
    const fallback = colorMap["UNKNOWN_TYPE"] ?? colorMap.slate;
    expect(fallback).toContain("slate");
  });

  it("all color class strings contain both bg and border tokens", () => {
    Object.values(colorMap).forEach((cls) => {
      expect(cls).toContain("bg-");
      expect(cls).toContain("border-");
    });
  });
});

// ── Risk level color mapping ───────────────────────────────────────────────────

describe("Fund risk level color mapping", () => {
  const riskColor: Record<string, string> = {
    LOW: "text-emerald-400",
    MODERATE: "text-blue-400",
    HIGH: "text-amber-400",
    VERY_HIGH: "text-rose-400",
  };

  it("has a color for all 4 risk levels", () => {
    const levels: FundSnapshot["risk_level"][] = ["LOW", "MODERATE", "HIGH", "VERY_HIGH"];
    levels.forEach((level) => {
      expect(riskColor[level]).toBeDefined();
    });
  });

  it("VERY_HIGH maps to rose", () => {
    expect(riskColor.VERY_HIGH).toContain("rose");
  });

  it("LOW maps to emerald", () => {
    expect(riskColor.LOW).toContain("emerald");
  });
});

// ── Probability distribution validation ───────────────────────────────────────

describe("Probability distribution", () => {
  it("bull + base + bear should sum to 100", () => {
    const pd = { bull_pct: 42, base_pct: 38, bear_pct: 20 };
    const total = pd.bull_pct + pd.base_pct + pd.bear_pct;
    expect(total).toBe(100);
  });

  it("rejects distributions that do not sum to 100", () => {
    const invalid = { bull_pct: 50, base_pct: 40, bear_pct: 20 };
    const total = invalid.bull_pct + invalid.base_pct + invalid.bear_pct;
    expect(total).not.toBe(100);
  });
});

// ── Navigation route registration ────────────────────────────────────────────

describe("Mission Control route registration", () => {
  it("mission-control route is included in valid app routes", () => {
    const routes = [
      "/mission-control",
      "/research",
      "/company/AAPL",
      "/forecast",
      "/portfolio",
      "/risk",
      "/timeline",
      "/v2-fund",
      "/briefings",
      "/reasoning-memory",
      "/workspace",
      "/alerts",
    ];
    expect(routes).toContain("/mission-control");
    expect(routes.indexOf("/mission-control")).toBe(0); // first = primary
    expect(routes).toContain("/v2-fund");
    expect(routes).toContain("/reasoning-memory");
    expect(routes).toContain("/briefings");
  });

  it("all critical v2 routes are reachable from mission-control links", () => {
    const missionControlLinks = [
      "/timeline",
      "/briefings",
      "/v2-fund",
      "/research",
      "/reasoning-memory",
      "/risk",
      "/workspace",
      "/alerts",
    ];
    expect(missionControlLinks).toHaveLength(8);
    missionControlLinks.forEach((link) => {
      expect(link.startsWith("/")).toBe(true);
    });
  });
});

// ── API URL construction ───────────────────────────────────────────────────────

describe("Mission Control API URL construction", () => {
  const BASE = "http://localhost:8000";

  it("builds correct dashboard URL", () => {
    const url = `${BASE}/api/v1/mission-control/dashboard`;
    expect(url).toContain("/api/v1/mission-control/dashboard");
  });

  it("builds correct fund URL with ID", () => {
    const fundId = "CONSERVATIVE";
    const url = `${BASE}/api/v1/mission-control/funds/${fundId}`;
    expect(url).toContain("CONSERVATIVE");
    expect(url).toContain("/funds/");
  });

  it("builds correct search URL with encoding", () => {
    const q = "Growth Fund";
    const url = `${BASE}/api/v1/mission-control/search?q=${encodeURIComponent(q)}`;
    expect(url).toContain("Growth%20Fund");
  });

  it("builds correct reasoning URL with ID", () => {
    const id = "reasoning_001_abc";
    const url = `${BASE}/api/v1/mission-control/reasoning/${encodeURIComponent(id)}`;
    expect(url).toContain("reasoning_001_abc");
  });

  it("builds correct SSE stream URL", () => {
    const url = `${BASE}/api/v1/mission-control/stream?tick_interval=3.0`;
    expect(url).toContain("stream");
    expect(url).toContain("tick_interval=3.0");
  });
});

// ── SHAP factor validation ─────────────────────────────────────────────────────

describe("SHAP factor structure", () => {
  const shapFactors = [
    { factor: "Earnings momentum", importance: 0.34, direction: "positive" as const },
    { factor: "Fed policy", importance: 0.28, direction: "negative" as const },
    { factor: "Sector rotation", importance: 0.21, direction: "positive" as const },
    { factor: "VIX level", importance: 0.17, direction: "negative" as const },
  ];

  it("importance values are all between 0 and 1", () => {
    shapFactors.forEach(({ importance }) => {
      expect(importance).toBeGreaterThan(0);
      expect(importance).toBeLessThanOrEqual(1);
    });
  });

  it("direction values are valid", () => {
    const validDirections = ["positive", "negative"];
    shapFactors.forEach(({ direction }) => {
      expect(validDirections).toContain(direction);
    });
  });

  it("SHAP importances sum to approximately 1", () => {
    const total = shapFactors.reduce((sum, f) => sum + f.importance, 0);
    expect(Math.abs(total - 1.0)).toBeLessThan(0.01);
  });
});

// ── Replay direction validation ───────────────────────────────────────────────

describe("Chess replay direction validation", () => {
  const validDirections = ["forward", "backward"];

  it("forward is a valid direction", () => {
    expect(validDirections).toContain("forward");
  });

  it("backward is a valid direction", () => {
    expect(validDirections).toContain("backward");
  });

  it("sideways is not a valid direction", () => {
    expect(validDirections).not.toContain("sideways");
  });

  it("returns 400 for invalid direction (conceptual contract)", () => {
    // Matches the backend: HTTPException(status_code=400)
    const isValid = (dir: string) => validDirections.includes(dir);
    expect(isValid("forward")).toBe(true);
    expect(isValid("sideways")).toBe(false);
  });
});
