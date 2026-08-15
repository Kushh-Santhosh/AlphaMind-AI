"use client";

import React, { useState } from "react";
import {
  LayoutDashboard,
  Star,
  Copy,
  BarChart3,
  BookMarked,
  Bell,
  BellRing,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Plus,
  Trash2,
  Eye,
} from "lucide-react";

interface PaperPortfolio {
  portfolio_id: string;
  name: string;
  cloned_from_fund_id: string;
  current_value: number;
  returns_pct: number;
  sharpe_ratio: number;
  allocations: Record<string, number>;
}

interface WorkspaceAlert {
  alert_id: string;
  title: string;
  message: string;
  alert_type: string;
  is_read: boolean;
  created_at_utc: string;
}

interface WatchlistItem {
  symbol: string;
  asset_class: string;
  notes: string;
}

type Tab = "overview" | "portfolios" | "watchlist" | "alerts";

const MOCK_FOLLOWED = ["GROWTH", "BALANCED", "CONSERVATIVE"];

const MOCK_PORTFOLIOS: PaperPortfolio[] = [
  {
    portfolio_id: "pp_a1b2c3d4",
    name: "My Growth Clone",
    cloned_from_fund_id: "GROWTH",
    current_value: 11850.0,
    returns_pct: 18.5,
    sharpe_ratio: 1.32,
    allocations: { QQQ: 0.35, NVDA: 0.40, MSFT: 0.15, AMZN: 0.10 },
  },
  {
    portfolio_id: "pp_b3c4d5e6",
    name: "Conservative Hedge",
    cloned_from_fund_id: "CONSERVATIVE",
    current_value: 10650.0,
    returns_pct: 6.5,
    sharpe_ratio: 1.72,
    allocations: { TLT: 0.50, GLD: 0.20, SPY: 0.30 },
  },
];

const MOCK_WATCHLIST: WatchlistItem[] = [
  { symbol: "NVDA", asset_class: "EQUITY", notes: "Semiconductor momentum play" },
  { symbol: "BTC-USD", asset_class: "CRYPTO", notes: "Volatility hedge" },
  { symbol: "TLT", asset_class: "FIXED_INCOME", notes: "Rate sensitivity" },
];

const MOCK_ALERTS: WorkspaceAlert[] = [
  {
    alert_id: "alert_a1b2c3",
    title: "Growth Fund Rebalanced",
    message: "The AlphaMind Growth AI Fund rebalanced allocations. NVDA weight increased to 40%.",
    alert_type: "REBALANCE",
    is_read: false,
    created_at_utc: "2026-08-04T14:30:00Z",
  },
  {
    alert_id: "alert_b2c3d4",
    title: "Morning Brief Ready",
    message: "Your 2026-08-04 Morning Brief has been generated and is available in the Briefings section.",
    alert_type: "BRIEFING",
    is_read: false,
    created_at_utc: "2026-08-04T05:00:00Z",
  },
  {
    alert_id: "alert_c3d4e5",
    title: "VaR Improved",
    message: "Portfolio Value-at-Risk (95%) improved by 0.3% across all followed funds.",
    alert_type: "RISK",
    is_read: true,
    created_at_utc: "2026-08-03T18:00:00Z",
  },
];

const FUNDS = [
  { id: "CONSERVATIVE", name: "Conservative", cagr: 6.5, sharpe: 1.85, color: "teal" },
  { id: "BALANCED", name: "Balanced", cagr: 11.2, sharpe: 1.62, color: "blue" },
  { id: "GROWTH", name: "Growth", cagr: 18.5, sharpe: 1.45, color: "emerald" },
  { id: "AGGRESSIVE", name: "Aggressive", cagr: 26.4, sharpe: 1.28, color: "amber" },
  { id: "CRYPTO", name: "Crypto", cagr: 42.0, sharpe: 1.15, color: "rose" },
];

const alertTypeColor: Record<string, string> = {
  REBALANCE: "text-violet-400 bg-violet-500/10 border-violet-500/20",
  BRIEFING: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  RISK: "text-rose-400 bg-rose-500/10 border-rose-500/20",
  FORECAST: "text-amber-400 bg-amber-500/10 border-amber-500/20",
  INFO: "text-slate-400 bg-slate-500/10 border-slate-500/20",
};

const fundColorMap: Record<string, string> = {
  teal: "border-teal-500/30 text-teal-400",
  blue: "border-blue-500/30 text-blue-400",
  emerald: "border-emerald-500/30 text-emerald-400",
  amber: "border-amber-500/30 text-amber-400",
  rose: "border-rose-500/30 text-rose-400",
};

export default function WorkspacePage() {
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [followed, setFollowed] = useState<string[]>(MOCK_FOLLOWED);
  const [portfolios] = useState<PaperPortfolio[]>(MOCK_PORTFOLIOS);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>(MOCK_WATCHLIST);
  const [alerts, setAlerts] = useState<WorkspaceAlert[]>(MOCK_ALERTS);

  const unreadCount = alerts.filter((a) => !a.is_read).length;

  const toggleFollow = (id: string) =>
    setFollowed((f) => (f.includes(id) ? f.filter((x) => x !== id) : [...f, id]));

  const removeWatchlist = (symbol: string) =>
    setWatchlist((w) => w.filter((i) => i.symbol !== symbol));

  const markRead = (id: string) =>
    setAlerts((a) => a.map((al) => (al.alert_id === id ? { ...al, is_read: true } : al)));

  const TABS: { id: Tab; label: string; Icon: React.ElementType }[] = [
    { id: "overview", label: "Overview", Icon: LayoutDashboard },
    { id: "portfolios", label: "My Portfolios", Icon: Copy },
    { id: "watchlist", label: "Watchlist", Icon: BookMarked },
    { id: "alerts", label: `Alerts${unreadCount > 0 ? ` (${unreadCount})` : ""}`, Icon: Bell },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-5xl mx-auto space-y-8">

        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-violet-500/10 text-violet-400 border border-violet-500/20">AlphaMind v2.0 — Milestone 20</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <LayoutDashboard className="w-8 h-8 text-violet-400" />
            User Strategy Workspace
          </h1>
          <p className="text-slate-400 text-sm mt-1">Follow AI funds, clone allocations, compare performance, and manage your watchlists.</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
          {TABS.map(({ id, label, Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-semibold transition-all ${
                activeTab === id
                  ? "bg-violet-600 text-white shadow"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Icon className="w-4 h-4" /> {label}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Star className="w-4 h-4 text-amber-400" /> Follow AI Funds
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {FUNDS.map((fund) => {
                const isFollowing = followed.includes(fund.id);
                return (
                  <div key={fund.id} className={`bg-slate-900 border rounded-xl p-5 transition-all ${isFollowing ? "border-violet-500 ring-1 ring-violet-500" : "border-slate-800"}`}>
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded border ${fundColorMap[fund.color]}`}>{fund.name}</span>
                        <div className="mt-2 flex gap-4">
                          <div>
                            <div className="text-xs text-slate-500">CAGR</div>
                            <div className="text-sm font-bold text-emerald-400">{fund.cagr}%</div>
                          </div>
                          <div>
                            <div className="text-xs text-slate-500">Sharpe</div>
                            <div className="text-sm font-bold text-blue-400">{fund.sharpe.toFixed(2)}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => toggleFollow(fund.id)}
                        className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs font-semibold transition ${isFollowing ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-300 hover:bg-slate-700"}`}
                      >
                        {isFollowing ? <CheckCircle className="w-3.5 h-3.5" /> : <Star className="w-3.5 h-3.5" />}
                        {isFollowing ? "Following" : "Follow"}
                      </button>
                      <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">
                        <Copy className="w-3.5 h-3.5" /> Clone
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Portfolios Tab */}
        {activeTab === "portfolios" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <Copy className="w-4 h-4 text-blue-400" /> Paper Portfolios
              </h2>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-violet-600 text-white hover:bg-violet-700 transition">
                <Plus className="w-3.5 h-3.5" /> Clone Fund
              </button>
            </div>
            {portfolios.map((pp) => (
              <div key={pp.portfolio_id} className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-slate-100">{pp.name}</h3>
                    <p className="text-xs text-slate-500">Cloned from {pp.cloned_from_fund_id} · {pp.portfolio_id}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-white">${pp.current_value.toLocaleString()}</div>
                    <div className={`text-sm font-semibold flex items-center gap-1 justify-end ${pp.returns_pct >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                      {pp.returns_pct >= 0 ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
                      {pp.returns_pct}% CAGR
                    </div>
                  </div>
                </div>
                <div className="flex gap-6 mb-4">
                  <div>
                    <div className="text-xs text-slate-500">Sharpe Ratio</div>
                    <div className="text-sm font-bold text-blue-400">{pp.sharpe_ratio.toFixed(2)}</div>
                  </div>
                </div>
                {/* Allocation bars */}
                <div className="space-y-1.5">
                  {Object.entries(pp.allocations).map(([sym, wt]) => (
                    <div key={sym} className="flex items-center gap-3">
                      <span className="text-xs font-mono text-slate-400 w-10">{sym}</span>
                      <div className="flex-1 h-1.5 bg-slate-800 rounded-full">
                        <div className="h-1.5 bg-violet-500 rounded-full" style={{ width: `${wt * 100}%` }} />
                      </div>
                      <span className="text-xs font-mono text-slate-300 w-8 text-right">{(wt * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                </div>
                <div className="mt-3 flex gap-2">
                  <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">
                    <BarChart3 className="w-3.5 h-3.5" /> Compare vs Fund
                  </button>
                  <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition">
                    <Eye className="w-3.5 h-3.5" /> View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Watchlist Tab */}
        {activeTab === "watchlist" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <BookMarked className="w-4 h-4 text-teal-400" /> Watchlist
              </h2>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-violet-600 text-white hover:bg-violet-700 transition">
                <Plus className="w-3.5 h-3.5" /> Add Symbol
              </button>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-xs text-slate-400 border-b border-slate-800 bg-slate-900/80">
                    <th className="text-left px-4 py-3">Symbol</th>
                    <th className="text-left px-4 py-3">Asset Class</th>
                    <th className="text-left px-4 py-3">Notes</th>
                    <th className="px-4 py-3" />
                  </tr>
                </thead>
                <tbody>
                  {watchlist.map((item) => (
                    <tr key={item.symbol} className="border-b border-slate-800/50 last:border-0 hover:bg-slate-800/30">
                      <td className="px-4 py-3 font-mono font-bold text-slate-100">{item.symbol}</td>
                      <td className="px-4 py-3">
                        <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">{item.asset_class}</span>
                      </td>
                      <td className="px-4 py-3 text-slate-400 text-xs">{item.notes}</td>
                      <td className="px-4 py-3 text-right">
                        <button onClick={() => removeWatchlist(item.symbol)} className="p-1.5 rounded text-slate-600 hover:text-rose-400 hover:bg-rose-500/10 transition">
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Alerts Tab */}
        {activeTab === "alerts" && (
          <div className="space-y-4">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <BellRing className="w-4 h-4 text-amber-400" /> Alert Center
            </h2>
            {alerts.map((alert) => (
              <div
                key={alert.alert_id}
                className={`bg-slate-900 border rounded-xl p-4 transition-all ${alert.is_read ? "border-slate-800 opacity-60" : "border-slate-700"}`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs font-bold px-2 py-0.5 rounded border ${alertTypeColor[alert.alert_type] || alertTypeColor.INFO}`}>
                        {alert.alert_type}
                      </span>
                      {!alert.is_read && <span className="w-2 h-2 rounded-full bg-violet-500" />}
                    </div>
                    <h3 className="font-semibold text-slate-100 text-sm">{alert.title}</h3>
                    <p className="text-xs text-slate-400 mt-0.5">{alert.message}</p>
                    <p className="text-xs text-slate-600 mt-1">{alert.created_at_utc}</p>
                  </div>
                  {!alert.is_read && (
                    <button
                      onClick={() => markRead(alert.alert_id)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition flex-shrink-0"
                    >
                      <CheckCircle className="w-3.5 h-3.5" /> Mark Read
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
