/**
 * AlphaMind AI v2 — Mission Control TypeScript type definitions.
 * All types derive from the /api/v1/mission-control/* backend contract.
 */

// ── Subsystem health ──────────────────────────────────────────────────────────

export interface SubsystemHealth {
  status: "UP" | "DOWN" | "DEGRADED";
  description: string;
  events?: number;
  records?: number;
  funds?: number;
  handlers?: number;
  briefings?: number;
  users?: number;
  session_id?: string;
  current_step?: number;
}

export interface SystemHealth {
  status: "HEALTHY" | "DEGRADED" | "CRITICAL";
  generated_at_utc: string;
  uptime_seconds: number;
  subsystems: Record<string, SubsystemHealth>;
}

// ── Virtual AI Fund ───────────────────────────────────────────────────────────

export interface FundAllocation {
  symbol: string;
  weight: number;
}

export interface FundSnapshot {
  fund_id: string;
  name: string;
  description: string;
  current_market_value_usd: number;
  initial_capital_usd: number;
  total_return_pct: number;
  cagr_pct: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  max_drawdown_pct: number;
  win_rate_pct: number;
  brier_score: number;
  confidence: number;
  risk_level: "LOW" | "MODERATE" | "HIGH" | "VERY_HIGH";
  allocations: Record<string, number>;
  top_holding: { symbol: string; weight: number };
  last_rebalance_utc: string;
  today_pnl_usd: number;
  today_pnl_pct: number;
}

// ── Timeline & Activity ───────────────────────────────────────────────────────

export interface TimelineEvent {
  event_id: string;
  event_type: string;
  headline: string;
  source_subsystem: string;
  timestamp_utc: string;
}

export interface ActivityFeedItem extends TimelineEvent {
  icon: string;
  color: string;
  timeline_link: string;
  reasoning_link: string | null;
  replay_link: string;
}

export interface TimelineStats {
  total_events: number;
  by_type: Record<string, number>;
  by_subsystem: Record<string, number>;
  oldest_event_utc: string | null;
  newest_event_utc: string | null;
}

// ── Reasoning / Decision Inspector ───────────────────────────────────────────

export interface ShapFactor {
  factor: string;
  importance: number;
  direction: "positive" | "negative";
}

export interface ProbabilityDistribution {
  bull_pct: number;
  base_pct: number;
  bear_pct: number;
}

export interface Citations {
  sec_filings: string[];
  macro_sources: string[];
  news_sources: string[];
}

export interface ReasoningRecord {
  reasoning_id: string;
  decision_id: string;
  parent_reasoning_id: string | null;
  selected_action: string;
  confidence_score: number;
  timestamp_utc: string;
  assumptions: string[];
  evidence_references: string[];
  contradicting_evidence: string[];
  alternative_actions_considered: (string | Record<string, unknown>)[];
  probability_distribution: ProbabilityDistribution;
  shap_factors: ShapFactor[];
  citations: Citations;
  replay_snapshot_id: string | null;
  audit_metadata: Record<string, string>;
}

export interface ReasoningListItem {
  reasoning_id: string;
  decision_id: string;
  selected_action: string;
  confidence_score: number;
  assumptions: string[];
  evidence_references: string[];
  contradicting_evidence: string[];
  alternative_actions: string[];
  timestamp_utc: string;
}

// ── Intelligence Dashboard ────────────────────────────────────────────────────

export interface MacroFactor {
  factor: string;
  impact: "LOW" | "MEDIUM" | "HIGH";
  direction: "POSITIVE" | "NEGATIVE" | "NEUTRAL";
}

export interface RiskAlert {
  alert_id: string;
  title: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  affected_funds: string[];
}

export interface IntelligenceSnapshot {
  generated_at_utc: string;
  current_reasoning: Array<{
    reasoning_id: string;
    action: string;
    confidence: number;
    timestamp_utc: string;
  }>;
  avg_confidence_score: number;
  highest_confidence: { reasoning_id: string; action: string; confidence: number } | null;
  largest_uncertainty: { reasoning_id: string; action: string; confidence: number } | null;
  total_reasoning_records: number;
  latest_briefing: {
    briefing_id: string;
    briefing_type: string;
    period_label: string;
    summary: string;
    generated_at_utc: string;
  } | null;
  macro_factors: MacroFactor[];
  risk_alerts: RiskAlert[];
}

// ── Notifications ─────────────────────────────────────────────────────────────

export interface Notification {
  notification_id: string;
  type: "BRIEFING" | "REBALANCE" | "ALERT" | "RESEARCH" | "SYSTEM";
  title: string;
  message: string;
  is_read: boolean;
  created_at_utc: string;
  link: string;
}

// ── Chess Replay ──────────────────────────────────────────────────────────────

export interface ReplayPosition {
  current_step: number;
  total_steps?: number;
  session_id?: string;
}

export interface ReplayFrame {
  event_id?: string;
  event_type?: string;
  headline?: string;
  timestamp_utc?: string;
  portfolio_snapshot?: Record<string, unknown>;
  market_snapshot?: Record<string, unknown>;
}

export interface ReplayStatus {
  generated_at_utc: string;
  session_id: string;
  position: ReplayPosition;
  total_frames: number;
}

// ── Dashboard state ───────────────────────────────────────────────────────────

export interface DashboardState {
  generated_at_utc: string;
  uptime_seconds: number;
  system_health: SystemHealth;
  funds: FundSnapshot[];
  timeline: TimelineEvent[];
  reasoning: ReasoningListItem[];
  activity_feed: ActivityFeedItem[];
  intelligence: IntelligenceSnapshot;
  latest_briefing: {
    briefing_id: string;
    briefing_type: string;
    period_label: string;
    executive_summary: string;
    generated_at_utc: string;
  } | null;
  notifications: Notification[];
  timeline_stats: TimelineStats;
  total_aum_usd: number;
  total_assets_covered: number;
  avg_confidence: number;
  replay_position: ReplayPosition;
}

// ── Global search ─────────────────────────────────────────────────────────────

export interface SearchResult {
  type: "TIMELINE" | "REASONING" | "FUND" | "BRIEFING" | "ASSET";
  id: string;
  label: string;
  sub: string;
  link: string;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total: number;
  generated_at_utc: string;
}

// ── SSE live tick ─────────────────────────────────────────────────────────────

export interface LiveTick {
  tick: number;
  event_id?: string;
  event_type?: string;
  headline?: string;
  source_subsystem?: string;
  timestamp_utc: string;
  total_timeline_events?: number;
  total_aum_usd?: number;
  uptime_seconds: number;
  status?: string;
}
