"use client";

/**
 * AlphaMind AI v2 — Mission Control Terminal (Milestone 21)
 *
 * The primary institutional workspace. Bloomberg Terminal + GitHub Activity +
 * ChatGPT + TradingView combined into one live, streaming, institutional-grade
 * investment operating system dashboard.
 *
 * Sections:
 *  1. Live Header Bar      — clock, market session, system status, live tick
 *  2. KPI Strip            — AUM, assets, confidence, timeline events, uptime
 *  3. System Health Grid   — all 10 subsystems with status indicators
 *  4. Activity Feed        — GitHub-style unified event timeline
 *  5. Live Fund Dashboard  — 5 virtual AI fund cards
 *  6. Intelligence Panel   — confidence, macro factors, risk alerts, briefing
 *  7. Chess Replay         — bidirectional timeline replay
 *  8. Timeline Stats       — event distribution by type / subsystem
 *  9. Notification Center  — platform-wide notification feed
 * 10. Global Search        — cross-entity command palette search
 */

import React, { memo, Suspense, useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  Brain,
  CheckCircle,
  ChevronRight,
  Clock,
  Cpu,
  ExternalLink,
  Globe2,
  LineChart,
  Search,
  Server,
  Shield,
  Sparkles,
  Target,
  TrendingDown,
  TrendingUp,
  Wifi,
  XCircle,
  Zap,
} from "lucide-react";

import {
  useActivityFeed,
  useDashboard,
  useFunds,
  useGlobalSearch,
  useIntelligence,
  useLiveStream,
  useNotifications,
  useTimelineStats,
} from "@/hooks/useMissionControl";
import { DecisionInspectorModal } from "@/components/mission-control/DecisionInspectorModal";
import { ChessReplayPanel } from "@/components/mission-control/ChessReplayPanel";
import type {
  ActivityFeedItem,
  FundSnapshot,
  MacroFactor,
  Notification,
  RiskAlert,
  SubsystemHealth,
} from "@/lib/missionControlTypes";

// ── Helpers ───────────────────────────────────────────────────────────────────

function fmt(n: number, decimals = 1): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(decimals)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(decimals)}K`;
  return n.toFixed(decimals);
}

function fmtUSD(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
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

// ── Live Clock ────────────────────────────────────────────────────────────────

function LiveClock() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const hour = now.getUTCHours();
  const isNY = hour >= 14 && hour < 21; // 9:30–4 ET = 14:30–21 UTC approx
  const isLDN = hour >= 8 && hour < 16;
  const isTK = hour >= 0 && hour < 7;

  return (
    <div className="flex items-center gap-4">
      <div className="flex items-center gap-1.5">
        <Clock className="w-3.5 h-3.5 text-slate-400" />
        <span className="text-sm font-mono font-bold text-slate-100 tabular-nums">
          {now.toUTCString().slice(17, 25)} UTC
        </span>
      </div>
      <div className="hidden md:flex items-center gap-2 text-[10px] font-semibold">
        <span className={`px-2 py-0.5 rounded-full border ${isNY ? "bg-emerald-500/15 border-emerald-500/30 text-emerald-400" : "bg-slate-800 border-slate-700 text-slate-500"}`}>
          NY {isNY ? "OPEN" : "CLOSED"}
        </span>
        <span className={`px-2 py-0.5 rounded-full border ${isLDN ? "bg-blue-500/15 border-blue-500/30 text-blue-400" : "bg-slate-800 border-slate-700 text-slate-500"}`}>
          LDN {isLDN ? "OPEN" : "CLOSED"}
        </span>
        <span className={`px-2 py-0.5 rounded-full border ${isTK ? "bg-amber-500/15 border-amber-500/30 text-amber-400" : "bg-slate-800 border-slate-700 text-slate-500"}`}>
          TK {isTK ? "OPEN" : "CLOSED"}
        </span>
      </div>
    </div>
  );
}

// ── Pulsing live dot ──────────────────────────────────────────────────────────

function LiveDot({ color = "emerald" }: { color?: string }) {
  return (
    <span className="relative flex h-2 w-2">
      <span className={`animate-ping absolute inline-flex h-full w-full rounded-full bg-${color}-400 opacity-60`} />
      <span className={`relative inline-flex rounded-full h-2 w-2 bg-${color}-500`} />
    </span>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

interface KpiCardProps {
  label: string;
  value: string;
  sub?: string;
  color?: string;
  icon: React.ElementType;
}

const KpiCard = memo(function KpiCard({ label, value, sub, color = "blue", icon: Icon }: KpiCardProps) {
  return (
    <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 hover:border-slate-700 transition-colors group">
      <div className="flex items-start justify-between">
        <div className={`w-8 h-8 rounded-lg bg-${color}-500/10 border border-${color}-500/20 flex items-center justify-center group-hover:scale-105 transition-transform`}>
          <Icon className={`w-4 h-4 text-${color}-400`} />
        </div>
        <LiveDot color={color} />
      </div>
      <div className="mt-3 space-y-0.5">
        <p className="text-xl font-bold text-slate-100 tabular-nums">{value}</p>
        <p className="text-[10px] text-slate-400 font-medium">{label}</p>
        {sub && <p className="text-[10px] text-slate-600">{sub}</p>}
      </div>
    </div>
  );
});

// ── Subsystem Badge ───────────────────────────────────────────────────────────

function SubsystemBadge({ name, health }: { name: string; health: SubsystemHealth }) {
  const up = health.status === "UP";
  return (
    <div className={`flex items-center justify-between p-2.5 rounded-lg border transition-colors ${up ? "bg-emerald-500/5 border-emerald-500/15 hover:border-emerald-500/30" : "bg-rose-500/5 border-rose-500/20"}`}>
      <div className="flex items-center gap-2">
        {up ? (
          <CheckCircle className="w-3 h-3 text-emerald-500" />
        ) : (
          <XCircle className="w-3 h-3 text-rose-500" />
        )}
        <span className="text-[10px] font-semibold text-slate-300">{name.replace(/_/g, " ").toUpperCase()}</span>
      </div>
      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${up ? "text-emerald-400 bg-emerald-500/10" : "text-rose-400 bg-rose-500/10"}`}>
        {health.status}
      </span>
    </div>
  );
}

// ── Activity Feed Item ────────────────────────────────────────────────────────

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

interface ActivityItemProps {
  item: ActivityFeedItem;
  onInspect: (id: string) => void;
}

const ActivityItemRow = memo(function ActivityItemRow({ item, onInspect }: ActivityItemProps) {
  const cls = colorMap[item.color] ?? colorMap.slate;
  return (
    <div className="flex items-start gap-3 py-2.5 border-b border-slate-800/50 last:border-0 group hover:bg-slate-900/30 px-2 -mx-2 rounded-lg transition-colors">
      <div className={`mt-0.5 w-6 h-6 rounded-full border flex items-center justify-center text-xs shrink-0 ${cls}`}>
        {item.icon}
      </div>
      <div className="flex-1 min-w-0 space-y-0.5">
        <p className="text-xs text-slate-300 leading-tight line-clamp-1">{item.headline}</p>
        <div className="flex items-center gap-2">
          <span className="text-[9px] text-slate-600 font-mono">{item.source_subsystem}</span>
          <span className="text-[9px] text-slate-700">·</span>
          <span className="text-[9px] text-slate-600">{new Date(item.timestamp_utc).toLocaleTimeString()}</span>
        </div>
      </div>
      <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
        <button
          onClick={() => onInspect(item.event_id)}
          className="p-1 rounded hover:bg-slate-700 text-slate-500 hover:text-slate-300 transition-colors"
          aria-label="Inspect decision"
          title="Inspect in Decision Inspector"
        >
          <Brain className="w-3 h-3" />
        </button>
        <Link
          href={item.timeline_link}
          className="p-1 rounded hover:bg-slate-700 text-slate-500 hover:text-slate-300 transition-colors"
          aria-label="View in timeline"
        >
          <ExternalLink className="w-3 h-3" />
        </Link>
      </div>
    </div>
  );
});

// ── Fund Card ─────────────────────────────────────────────────────────────────

const riskColor: Record<string, string> = {
  LOW: "text-emerald-400",
  MODERATE: "text-blue-400",
  HIGH: "text-amber-400",
  VERY_HIGH: "text-rose-400",
};

interface FundCardProps {
  fund: FundSnapshot;
  onInspect: (id: string) => void;
}

const FundCard = memo(function FundCard({ fund, onInspect }: FundCardProps) {
  const returnPos = fund.total_return_pct >= 0;
  return (
    <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 hover:border-slate-700 transition-all group space-y-3">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-100">{fund.name}</h3>
          <span className={`text-[10px] font-bold ${riskColor[fund.risk_level] ?? "text-slate-400"}`}>
            {fund.risk_level.replace("_", " ")}
          </span>
        </div>
        <div className="text-right">
          <div className="text-sm font-bold text-slate-100 tabular-nums">{fmtUSD(fund.current_market_value_usd)}</div>
          <div className={`text-xs font-bold tabular-nums ${returnPos ? "text-emerald-400" : "text-rose-400"}`}>
            {fmtPct(fund.total_return_pct)}
          </div>
        </div>
      </div>

      {/* Today P&L */}
      <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${fund.today_pnl_pct >= 0 ? "bg-emerald-500/5 border border-emerald-500/15" : "bg-rose-500/5 border border-rose-500/15"}`}>
        {fund.today_pnl_pct >= 0 ? (
          <TrendingUp className="w-3 h-3 text-emerald-400" />
        ) : (
          <TrendingDown className="w-3 h-3 text-rose-400" />
        )}
        <span className="text-[10px] text-slate-400">Today:</span>
        <span className={`text-[10px] font-bold ${fund.today_pnl_pct >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
          {fmtPct(fund.today_pnl_pct)} ({fmtUSD(fund.today_pnl_usd)})
        </span>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-3 gap-2">
        {[
          { label: "CAGR", value: `${fund.cagr_pct}%`, textColor: "text-blue-400" },
          { label: "Sharpe", value: fund.sharpe_ratio.toFixed(2), textColor: "text-violet-400" },
          { label: "Sortino", value: fund.sortino_ratio.toFixed(2), textColor: "text-cyan-400" },
          { label: "Max DD", value: `${fund.max_drawdown_pct}%`, textColor: "text-rose-400" },
          { label: "Win Rate", value: `${fund.win_rate_pct}%`, textColor: "text-emerald-400" },
          { label: "Brier", value: fund.brier_score.toFixed(3), textColor: "text-amber-400" },
        ].map(({ label, value, textColor }) => (
          <div key={label} className="text-center p-2 rounded-lg bg-slate-900/40 border border-slate-800/60">
            <div className={`text-sm font-bold ${textColor} tabular-nums`}>{value}</div>
            <div className="text-[9px] text-slate-500 font-medium">{label}</div>
          </div>
        ))}
      </div>

      {/* Confidence bar */}
      <div className="space-y-1">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">AI Confidence</span>
          <span className="text-slate-300 font-bold">{Math.round(fund.confidence * 100)}%</span>
        </div>
        <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-violet-500 to-blue-500 rounded-full transition-all duration-700"
            style={{ width: `${fund.confidence * 100}%` }}
          />
        </div>
      </div>

      {/* Top holding + links */}
      <div className="flex items-center justify-between pt-1">
        <div className="text-[10px] text-slate-500">
          Top: <span className="text-slate-300 font-semibold">{fund.top_holding.symbol}</span>{" "}
          <span className="text-slate-600">{(fund.top_holding.weight * 100).toFixed(1)}%</span>
        </div>
        <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => onInspect(fund.fund_id)}
            className="px-2 py-1 rounded-lg bg-violet-600/10 border border-violet-500/20 text-violet-400 text-[10px] hover:bg-violet-600/20 transition-colors"
          >
            Inspect
          </button>
          <Link
            href={`/v2-fund?fund=${fund.fund_id}`}
            className="px-2 py-1 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-[10px] hover:text-slate-200 transition-colors"
          >
            Detail
          </Link>
        </div>
      </div>
    </div>
  );
});

// ── Intelligence Panel ────────────────────────────────────────────────────────

function MacroFactorBadge({ f }: { f: MacroFactor }) {
  const impColor = { LOW: "slate", MEDIUM: "amber", HIGH: "rose" }[f.impact] ?? "slate";
  const dirColor = f.direction === "POSITIVE" ? "emerald" : f.direction === "NEGATIVE" ? "rose" : "slate";
  return (
    <div className="flex items-center justify-between p-2 rounded-lg bg-slate-900/40 border border-slate-800">
      <span className="text-[11px] text-slate-300 font-medium">{f.factor}</span>
      <div className="flex items-center gap-1.5">
        <span className={`text-[9px] font-bold text-${impColor}-400 bg-${impColor}-500/10 px-1.5 py-0.5 rounded`}>
          {f.impact}
        </span>
        <span className={`text-[9px] font-bold text-${dirColor}-400`}>
          {f.direction === "POSITIVE" ? "▲" : f.direction === "NEGATIVE" ? "▼" : "—"}
        </span>
      </div>
    </div>
  );
}

function RiskAlertRow({ a }: { a: RiskAlert }) {
  const sevColor = { LOW: "slate", MEDIUM: "amber", HIGH: "rose", CRITICAL: "red" }[a.severity] ?? "slate";
  return (
    <div className={`flex items-center justify-between p-2 rounded-lg bg-${sevColor}-500/5 border border-${sevColor}-500/20`}>
      <div className="flex items-center gap-2">
        <AlertTriangle className={`w-3 h-3 text-${sevColor}-400`} />
        <span className="text-[11px] text-slate-300">{a.title}</span>
      </div>
      <span className={`text-[9px] font-bold text-${sevColor}-400`}>{a.severity}</span>
    </div>
  );
}

// ── Notification Row ──────────────────────────────────────────────────────────

function NotificationRow({ n }: { n: Notification }) {
  const typeColor: Record<string, string> = {
    BRIEFING: "text-teal-400",
    REBALANCE: "text-violet-400",
    ALERT: "text-rose-400",
    RESEARCH: "text-blue-400",
    SYSTEM: "text-amber-400",
  };
  return (
    <Link
      href={n.link}
      className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-slate-800/50 transition-colors group border border-transparent hover:border-slate-700/50"
    >
      <div className={`mt-0.5 text-[10px] font-bold shrink-0 ${typeColor[n.type] ?? "text-slate-400"}`}>
        {n.type.slice(0, 3)}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs text-slate-300 font-medium line-clamp-1">{n.title}</p>
        <p className="text-[10px] text-slate-600 mt-0.5">{n.message}</p>
      </div>
      {!n.is_read && <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5 shrink-0" />}
    </Link>
  );
}

// ── Global Search Bar ─────────────────────────────────────────────────────────

function GlobalSearchBar() {
  const { query, results, loading, search } = useGlobalSearch();
  const [open, setOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen(true);
        setTimeout(() => inputRef.current?.focus(), 50);
      }
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return (
    <div className="relative">
      <div
        className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-slate-600 cursor-text transition-colors min-w-[200px]"
        onClick={() => { setOpen(true); setTimeout(() => inputRef.current?.focus(), 50); }}
        role="button"
        aria-label="Global search"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === "Enter") { setOpen(true); setTimeout(() => inputRef.current?.focus(), 50); }}}
      >
        <Search className="w-3.5 h-3.5 text-slate-500 shrink-0" />
        <span className="text-xs text-slate-500 flex-1">Search everything…</span>
        <span className="text-[10px] text-slate-600 bg-slate-800 px-1.5 py-0.5 rounded font-mono">⌘K</span>
      </div>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-96 z-50 bg-[#0d1322] border border-slate-700 rounded-2xl shadow-2xl shadow-black/50 overflow-hidden">
          <div className="flex items-center gap-2 p-3 border-b border-slate-800">
            <Search className="w-4 h-4 text-slate-400 shrink-0" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => search(e.target.value)}
              placeholder="Search funds, timeline, reasoning, briefings…"
              className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-600 focus:outline-none"
              aria-label="Search input"
            />
            {loading && <div className="animate-spin w-3.5 h-3.5 border-2 border-blue-500 border-t-transparent rounded-full" />}
          </div>

          {results && results.results.length > 0 && (
            <div className="max-h-72 overflow-y-auto divide-y divide-slate-800/50">
              {results.results.map((r) => (
                <Link
                  key={r.id}
                  href={r.link}
                  onClick={() => setOpen(false)}
                  className="flex items-start gap-3 p-3 hover:bg-slate-800/50 transition-colors group"
                >
                  <span className="text-[9px] font-bold text-slate-500 bg-slate-800 px-1.5 py-0.5 rounded shrink-0 mt-0.5">
                    {r.type.slice(0, 4)}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-slate-300 group-hover:text-slate-100 font-medium line-clamp-1">{r.label}</p>
                    <p className="text-[10px] text-slate-600 mt-0.5">{r.sub}</p>
                  </div>
                  <ChevronRight className="w-3 h-3 text-slate-600 shrink-0 mt-0.5" />
                </Link>
              ))}
            </div>
          )}

          {results && results.results.length === 0 && query && (
            <div className="p-6 text-center text-slate-600 text-sm">No results for &quot;{query}&quot;</div>
          )}

          <div className="p-2 border-t border-slate-800 text-center text-[10px] text-slate-600">
            Press Esc to close
          </div>
        </div>
      )}

      {open && <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} aria-hidden="true" />}
    </div>
  );
}

// ── Loading Skeleton ──────────────────────────────────────────────────────────

function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse bg-slate-800/60 rounded ${className}`} />;
}

// ── Section Header ────────────────────────────────────────────────────────────

const headerColorMap: Record<string, { bg: string; border: string; text: string }> = {
  blue: { bg: "bg-blue-500/10", border: "border-blue-500/20", text: "text-blue-400" },
  violet: { bg: "bg-violet-500/10", border: "border-violet-500/20", text: "text-violet-400" },
  emerald: { bg: "bg-emerald-500/10", border: "border-emerald-500/20", text: "text-emerald-400" },
  amber: { bg: "bg-amber-500/10", border: "border-amber-500/20", text: "text-amber-400" },
  teal: { bg: "bg-teal-500/10", border: "border-teal-500/20", text: "text-teal-400" },
  cyan: { bg: "bg-cyan-500/10", border: "border-cyan-500/20", text: "text-cyan-400" },
  rose: { bg: "bg-rose-500/10", border: "border-rose-500/20", text: "text-rose-400" },
  purple: { bg: "bg-purple-500/10", border: "border-purple-500/20", text: "text-purple-400" },
};

function SectionHeader({
  icon: Icon,
  title,
  sub,
  color = "blue",
  action,
}: {
  icon: React.ElementType;
  title: string;
  sub?: string;
  color?: string;
  action?: React.ReactNode;
}) {
  const theme = headerColorMap[color] ?? headerColorMap.blue;
  return (
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2">
        <div className={`w-7 h-7 rounded-lg ${theme.bg} border ${theme.border} flex items-center justify-center`}>
          <Icon className={`w-3.5 h-3.5 ${theme.text}`} />
        </div>
        <div>
          <h2 className="text-sm font-bold text-slate-100">{title}</h2>
          {sub && <p className="text-[10px] text-slate-500">{sub}</p>}
        </div>
      </div>
      {action}
    </div>
  );
}

// ── MAIN PAGE ─────────────────────────────────────────────────────────────────

export default function MissionControlPage() {
  const { data: dashboard, loading: dashLoading } = useDashboard();
  const { data: activityData } = useActivityFeed(30);
  const { data: fundsData } = useFunds();
  const { data: intelligence } = useIntelligence();
  const { data: notifData } = useNotifications(8);
  const { data: timelineStats } = useTimelineStats();
  const liveTickRaw = useLiveStream();

  // Decision Inspector state
  const [inspectedId, setInspectedId] = useState<string | null>(null);
  const handleInspect = useCallback((id: string) => setInspectedId(id), []);
  const handleCloseInspector = useCallback(() => setInspectedId(null), []);

  // Use dashboard data as fallback when individual feeds are still loading
  const funds = fundsData?.funds ?? dashboard?.funds ?? [];
  const activityItems = activityData?.items ?? dashboard?.activity_feed ?? [];
  const notifications = notifData?.notifications ?? dashboard?.notifications ?? [];
  const stats = timelineStats ?? dashboard?.timeline_stats;
  const health = dashboard?.system_health;
  const intel = intelligence ?? dashboard?.intelligence;

  const liveTick = liveTickRaw;

  return (
    <>
      {/* Decision Inspector Modal */}
      <DecisionInspectorModal reasoningId={inspectedId} onClose={handleCloseInspector} />

      <div className="space-y-4 max-w-[1600px] mx-auto">
        {/* ── 1. Live Header Bar ─────────────────────────────────────── */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 p-4 rounded-2xl bg-gradient-to-r from-blue-950/60 via-slate-900 to-violet-950/40 border border-blue-500/20 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold text-slate-100 tracking-tight">
                  Mission Control Terminal
                </h1>
                <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                  <LiveDot color="emerald" />
                  <span className="text-[10px] font-semibold text-emerald-400">LIVE</span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500">
                AlphaMind AI v2 — 24×7 Autonomous Investment Operating System
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 flex-wrap">
            <LiveClock />
            {liveTick && (
              <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900/60 border border-slate-700/50 text-[10px] font-mono text-slate-400">
                <Wifi className="w-3 h-3 text-blue-400" />
                <span>Tick #{liveTick.tick}</span>
                {liveTick.total_aum_usd && (
                  <span className="text-slate-600 ml-1">AUM {fmtUSD(liveTick.total_aum_usd)}</span>
                )}
              </div>
            )}
            <GlobalSearchBar />
          </div>
        </div>

        {/* ── 2. KPI Strip ──────────────────────────────────────────── */}
        {dashLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-24 rounded-xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
            <KpiCard label="Total AUM" value={fmtUSD(dashboard?.total_aum_usd ?? 0)} sub="5 Virtual Funds" color="blue" icon={BarChart3} />
            <KpiCard label="Assets Covered" value={`${dashboard?.total_assets_covered ?? 142}`} sub="SEC + Polygon" color="cyan" icon={Globe2} />
            <KpiCard label="AI Confidence" value={`${Math.round((dashboard?.avg_confidence ?? 0) * 100)}%`} sub="Avg across all decisions" color="violet" icon={Brain} />
            <KpiCard label="Timeline Events" value={fmt(stats?.total_events ?? 0, 0)} sub="Unified immutable log" color="emerald" icon={Activity} />
            <KpiCard label="System Uptime" value={uptime(dashboard?.uptime_seconds ?? 0)} sub="AlphaMind OS Core" color="amber" icon={Server} />
            <KpiCard label="Subsystems Up" value={`${Object.values(health?.subsystems ?? {}).filter(s => s.status === "UP").length} / ${Object.keys(health?.subsystems ?? {}).length}`} sub="All services nominal" color="teal" icon={CheckCircle} />
          </div>
        )}

        {/* ── 3. Main Three-Column Layout ─────────────────────────── */}
        <div className="grid grid-cols-1 xl:grid-cols-[340px_1fr_320px] gap-4">

          {/* LEFT: System Health + Notifications */}
          <div className="space-y-4">
            {/* System Health */}
            <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
              <SectionHeader icon={Server} title="System Health" sub="All platform subsystems" color="emerald"
                action={
                  <div className={`flex items-center gap-1.5 px-2 py-1 rounded-full text-[10px] font-bold ${health?.status === "HEALTHY" ? "bg-emerald-500/10 border border-emerald-500/20 text-emerald-400" : "bg-rose-500/10 border border-rose-500/20 text-rose-400"}`}>
                    <LiveDot color={health?.status === "HEALTHY" ? "emerald" : "rose"} />
                    {health?.status ?? "…"}
                  </div>
                }
              />
              <div className="space-y-1.5">
                {health ? (
                  Object.entries(health.subsystems).map(([name, sub]) => (
                    <SubsystemBadge key={name} name={name} health={sub} />
                  ))
                ) : (
                  Array.from({ length: 8 }).map((_, i) => <Skeleton key={i} className="h-8 rounded-lg" />)
                )}
              </div>
            </div>

            {/* Notification Center */}
            <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
              <SectionHeader icon={Bell} title="Notifications"
                sub={`${notifData?.unread_count ?? 0} unread`} color="amber"
                action={
                  notifData?.unread_count ? (
                    <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full">
                      {notifData.unread_count} new
                    </span>
                  ) : null
                }
              />
              <div className="space-y-0.5">
                {notifications.length === 0 && (
                  <p className="text-center py-4 text-slate-600 text-xs">No notifications</p>
                )}
                {notifications.map((n) => <NotificationRow key={n.notification_id} n={n} />)}
              </div>
            </div>

            {/* Chess Replay */}
            <Suspense fallback={<Skeleton className="h-64 rounded-2xl" />}>
              <ChessReplayPanel />
            </Suspense>
          </div>

          {/* CENTRE: Activity Feed + Fund Dashboard */}
          <div className="space-y-4">
            {/* Activity Feed */}
            <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
              <SectionHeader icon={Activity} title="Unified Activity Feed"
                sub={`${activityData?.total ?? 0} total events · GitHub-style timeline`}
                color="blue"
                action={
                  <Link href="/timeline" className="text-[10px] text-blue-400 hover:text-blue-300 flex items-center gap-1">
                    View all <ExternalLink className="w-3 h-3" />
                  </Link>
                }
              />
              <div className="max-h-64 overflow-y-auto pr-1">
                {activityItems.length === 0 && (
                  Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-10 rounded-lg mb-2" />)
                )}
                {activityItems.map((item) => (
                  <ActivityItemRow key={item.event_id} item={item} onInspect={handleInspect} />
                ))}
              </div>
            </div>

            {/* Live Fund Dashboard */}
            <div>
              <SectionHeader icon={LineChart} title="Live AI Fund Dashboard"
                sub="5 continuously running virtual strategies"
                color="violet"
                action={
                  <Link href="/v2-fund" className="text-[10px] text-violet-400 hover:text-violet-300 flex items-center gap-1">
                    Full leaderboard <ExternalLink className="w-3 h-3" />
                  </Link>
                }
              />
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                {funds.length === 0 && (
                  Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-52 rounded-xl" />)
                )}
                {funds.map((fund) => (
                  <FundCard key={fund.fund_id} fund={fund} onInspect={handleInspect} />
                ))}
              </div>
            </div>

            {/* Timeline Stats */}
            {stats && (
              <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
                <SectionHeader icon={BarChart3} title="Timeline Statistics"
                  sub={`${stats.total_events} total events across the Unified Timeline`}
                  color="teal"
                />
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider mb-2">By Event Type</p>
                    <div className="space-y-1.5">
                      {Object.entries(stats.by_type ?? {}).slice(0, 6).map(([type, count]) => (
                        <div key={type} className="flex items-center gap-2">
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-teal-500 rounded-full"
                              style={{ width: `${Math.min((count / Math.max(stats.total_events, 1)) * 100, 100)}%` }}
                            />
                          </div>
                          <span className="text-[10px] text-slate-500 w-6 text-right tabular-nums">{count}</span>
                          <span className="text-[10px] text-slate-400 truncate max-w-[100px]">{type.replace(/_/g, " ")}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider mb-2">By Subsystem</p>
                    <div className="space-y-1.5">
                      {Object.entries(stats.by_subsystem ?? {}).slice(0, 6).map(([sub, count]) => (
                        <div key={sub} className="flex items-center gap-2">
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-blue-500 rounded-full"
                              style={{ width: `${Math.min((count / Math.max(stats.total_events, 1)) * 100, 100)}%` }}
                            />
                          </div>
                          <span className="text-[10px] text-slate-500 w-6 text-right tabular-nums">{count}</span>
                          <span className="text-[10px] text-slate-400 truncate max-w-[100px]">{sub}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* RIGHT: Intelligence Dashboard */}
          <div className="space-y-4">
            {/* AI Confidence + Reasoning */}
            <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
              <SectionHeader icon={Brain} title="Intelligence" sub="Live AI reasoning state" color="purple" />

              {intel ? (
                <div className="space-y-4">
                  {/* Avg confidence gauge */}
                  <div className="p-3 rounded-xl bg-purple-500/5 border border-purple-500/15 text-center">
                    <div className="text-3xl font-bold text-purple-400 tabular-nums">
                      {Math.round(intel.avg_confidence_score * 100)}%
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">Avg AI Confidence</div>
                    <div className="mt-2 h-1.5 bg-slate-800 rounded-full overflow-hidden mx-4">
                      <div
                        className="h-full bg-gradient-to-r from-purple-500 to-violet-400 rounded-full transition-all duration-1000"
                        style={{ width: `${intel.avg_confidence_score * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* High / Low confidence */}
                  <div className="grid grid-cols-2 gap-2">
                    {intel.highest_confidence && (
                      <button
                        onClick={() => handleInspect(intel.highest_confidence!.reasoning_id)}
                        className="p-2 rounded-xl bg-emerald-500/5 border border-emerald-500/15 hover:border-emerald-500/30 transition-colors text-left"
                      >
                        <div className="text-[9px] text-emerald-400 font-semibold uppercase">Highest ↑</div>
                        <div className="text-sm font-bold text-emerald-400 mt-0.5 tabular-nums">
                          {Math.round(intel.highest_confidence.confidence * 100)}%
                        </div>
                        <div className="text-[9px] text-slate-500 mt-0.5 line-clamp-1">{intel.highest_confidence.action}</div>
                      </button>
                    )}
                    {intel.largest_uncertainty && (
                      <button
                        onClick={() => handleInspect(intel.largest_uncertainty!.reasoning_id)}
                        className="p-2 rounded-xl bg-amber-500/5 border border-amber-500/15 hover:border-amber-500/30 transition-colors text-left"
                      >
                        <div className="text-[9px] text-amber-400 font-semibold uppercase">Uncertainty ↓</div>
                        <div className="text-sm font-bold text-amber-400 mt-0.5 tabular-nums">
                          {Math.round(intel.largest_uncertainty.confidence * 100)}%
                        </div>
                        <div className="text-[9px] text-slate-500 mt-0.5 line-clamp-1">{intel.largest_uncertainty.action}</div>
                      </button>
                    )}
                  </div>

                  {/* Latest Briefing */}
                  {intel.latest_briefing && (
                    <div className="p-3 rounded-xl bg-teal-500/5 border border-teal-500/15">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-[10px] font-semibold text-teal-400 uppercase tracking-wider">
                          Latest Briefing
                        </span>
                        <Link href={`/briefings?id=${intel.latest_briefing.briefing_id}`}
                          className="text-[10px] text-slate-500 hover:text-slate-300">
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      </div>
                      <p className="text-[10px] text-slate-400 font-medium">{intel.latest_briefing.period_label}</p>
                      <p className="text-[10px] text-slate-500 mt-1 line-clamp-3">{intel.latest_briefing.summary}</p>
                    </div>
                  )}

                  {/* Macro Factors */}
                  <div className="space-y-2">
                    <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-1">
                      <Globe2 className="w-3 h-3" /> Macro Factors
                    </p>
                    {intel.macro_factors.map((f) => <MacroFactorBadge key={f.factor} f={f} />)}
                  </div>

                  {/* Risk Alerts */}
                  <div className="space-y-2">
                    <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-1">
                      <Shield className="w-3 h-3" /> Risk Alerts
                    </p>
                    {intel.risk_alerts.map((a) => <RiskAlertRow key={a.alert_id} a={a} />)}
                  </div>

                  {/* Recent Reasoning */}
                  {intel.current_reasoning.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-1">
                        <Zap className="w-3 h-3" /> Recent Decisions
                      </p>
                      {intel.current_reasoning.slice(0, 4).map((r) => (
                        <button
                          key={r.reasoning_id}
                          onClick={() => handleInspect(r.reasoning_id)}
                          className="w-full flex items-center justify-between p-2 rounded-lg bg-slate-900/40 border border-slate-800 hover:border-slate-700 transition-colors text-left group"
                        >
                          <div className="flex-1 min-w-0">
                            <p className="text-[11px] text-slate-300 font-medium line-clamp-1 group-hover:text-slate-100">
                              {r.action}
                            </p>
                            <p className="text-[9px] text-slate-600">{new Date(r.timestamp_utc).toLocaleTimeString()}</p>
                          </div>
                          <div className="text-[10px] font-bold text-violet-400 ml-2 shrink-0">
                            {Math.round(r.confidence * 100)}%
                          </div>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-3">
                  {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}
                </div>
              )}
            </div>

            {/* Quick Links */}
            <div className="p-4 rounded-2xl bg-[#0d1322] border border-slate-800">
              <SectionHeader icon={Target} title="Quick Links" color="slate" />
              <div className="grid grid-cols-2 gap-2">
                {[
                  { label: "Timeline", href: "/timeline", icon: Activity, color: "blue" },
                  { label: "Briefings", href: "/briefings", icon: Sparkles, color: "teal" },
                  { label: "AI Funds", href: "/v2-fund", icon: BarChart3, color: "violet" },
                  { label: "Research", href: "/research", icon: Search, color: "emerald" },
                  { label: "Reasoning", href: "/reasoning-memory", icon: Brain, color: "purple" },
                  { label: "Risk", href: "/risk", icon: AlertTriangle, color: "rose" },
                  { label: "Workspace", href: "/workspace", icon: Cpu, color: "cyan" },
                  { label: "Alerts", href: "/alerts", icon: Bell, color: "amber" },
                ].map(({ label, href, icon: Icon, color }) => (
                  <Link
                    key={href}
                    href={href}
                    className={`flex items-center gap-2 p-2.5 rounded-xl bg-${color}-500/5 border border-${color}-500/15 hover:border-${color}-500/30 hover:bg-${color}-500/10 transition-all text-xs font-medium text-${color}-400`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ── SEC/FINRA Disclaimer ─────────────────────────────────── */}
        <div className="p-3 rounded-xl bg-slate-900/40 border border-slate-800 text-center">
          <p className="text-[10px] text-slate-600">
            <strong className="text-slate-500">DISCLAIMER:</strong> AlphaMind AI Mission Control is for research and
            informational purposes only. All virtual fund activities are simulations. No financial advice or trade
            execution is provided. Past performance does not guarantee future results. Compliant with SEC/FINRA
            research standards. All probability estimates carry inherent uncertainty.
          </p>
        </div>
      </div>
    </>
  );
}
