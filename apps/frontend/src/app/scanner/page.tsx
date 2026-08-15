"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Brain,
  Building2,
  Calendar,
  CheckCircle2,
  ChevronRight,
  Clock,
  Cpu,
  Filter,
  Flame,
  Globe,
  Layers,
  LineChart,
  RefreshCw,
  Search,
  Shield,
  Sparkles,
  TrendingDown,
  TrendingUp,
  Zap,
} from "lucide-react";

interface OpportunityItem {
  symbol: string;
  name: string;
  asset_class: string;
  sector: string;
  opportunity_score: number;
  theme: string;
  price: number;
  change_24h_pct: number;
  factors: {
    momentum?: number;
    trend?: number;
    valuation?: number;
    risk_stability?: number;
    volume_profile?: number;
  };
  factor_inputs?: {
    rsi_14?: number;
    forward_pe?: number;
    trailing_pe?: number;
    volatility_annualized?: number;
    sma_50?: number;
  };
  recommendation: string;
  provenance?: {
    source: string;
    provider: string;
    freshness: string;
    age_seconds: number;
    market_status: string;
  };
  scanned_at_utc: string;
}

export default function OpportunityScannerPage() {
  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [minScore, setMinScore] = useState<number>(55);
  const [selectedUniverse, setSelectedUniverse] = useState<string>("ALL");
  const [selectedTheme, setSelectedTheme] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchOpportunities = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const url =
        selectedUniverse !== "ALL"
          ? `/api/v1/scanner/opportunities?min_score=${minScore}&asset_class=${encodeURIComponent(
              selectedUniverse
            )}`
          : `/api/v1/scanner/opportunities?min_score=${minScore}`;

      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setOpportunities(data.opportunities || []);
      } else {
        const err = await res.json();
        setErrorMsg(err.detail || "Failed to fetch scanner opportunities");
      }
    } catch {
      setErrorMsg("Network error connecting to opportunity scanner");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOpportunities();
  }, [minScore, selectedUniverse]);

  const filteredOpportunities = opportunities.filter((op) => {
    const matchesSearch =
      op.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
      op.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      op.sector.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTheme = selectedTheme === "ALL" || op.theme === selectedTheme;
    return matchesSearch && matchesTheme;
  });

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 p-6 space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#0d1322] via-[#090e1c] to-[#0d1428] border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white">AI Opportunity Scanner</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Dynamic quantitative ranking across Momentum, RSI, Valuation Multiples, Volatility, and Macro Regimes.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchOpportunities}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-all text-xs font-semibold flex items-center gap-2"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            Rescan Universe
          </button>
        </div>
      </div>

      {/* Filter and Control Bar */}
      <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
        {/* Search */}
        <div className="relative flex-1 min-w-[240px]">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
          <input
            type="text"
            placeholder="Search ticker, company name, or sector..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Universe Toggles */}
        <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
          {[
            { id: "ALL", label: "All Universes" },
            { id: "US_EQUITY", label: "US Equities" },
            { id: "INDIAN_EQUITY", label: "NSE India" },
            { id: "GLOBAL_ETF", label: "Global ETFs" },
            { id: "CRYPTO", label: "Crypto" },
          ].map((u) => (
            <button
              key={u.id}
              onClick={() => setSelectedUniverse(u.id)}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all ${
                selectedUniverse === u.id
                  ? "bg-blue-600/20 text-blue-400 border border-blue-500/40"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              {u.label}
            </button>
          ))}
        </div>

        {/* Min Score Slider */}
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>Min Score:</span>
          <input
            type="range"
            min="40"
            max="90"
            step="5"
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            className="w-20 accent-blue-500"
          />
          <span className="font-bold text-white w-6">{minScore}</span>
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {errorMsg}
        </div>
      )}

      {/* Opportunities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full p-16 text-center text-slate-400">
            <RefreshCw className="w-8 h-8 animate-spin mx-auto text-blue-400 mb-3" />
            <p className="font-semibold text-sm">Computing real-time factor models across active universe...</p>
            <p className="text-xs text-slate-500 mt-1">Executing yfinance live price feeds and mathematical factor matrices</p>
          </div>
        ) : filteredOpportunities.length === 0 ? (
          <div className="col-span-full p-16 text-center text-slate-500">
            No opportunities meet the current filter criteria. Try adjusting the score threshold.
          </div>
        ) : (
          filteredOpportunities.map((op) => (
            <div
              key={op.symbol}
              className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4 shadow-xl hover:shadow-2xl hover:shadow-blue-500/5"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 font-bold text-sm">
                      {op.symbol.slice(0, 3)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white text-base">{op.symbol}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-medium">
                          {op.asset_class}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 truncate max-w-[170px]">{op.name}</p>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-xs font-semibold text-slate-400">Opportunity Score</div>
                    <div className="text-2xl font-black text-blue-400 mt-0.5">
                      {op.opportunity_score.toFixed(1)}
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  <div>
                    <span className="text-slate-500">Price:</span>{" "}
                    <span className="font-semibold text-white">
                      {op.symbol.endsWith(".NS") ? "₹" : "$"}{op.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                  </div>
                  <div
                    className={`font-semibold flex items-center gap-0.5 ${
                      op.change_24h_pct >= 0 ? "text-emerald-400" : "text-rose-400"
                    }`}
                  >
                    {op.change_24h_pct >= 0 ? "+" : ""}
                    {op.change_24h_pct.toFixed(2)}% (24h)
                  </div>
                </div>

                {/* Factor Contribution Bars */}
                <div className="mt-4 space-y-2 text-xs">
                  <div className="flex justify-between text-[11px] text-slate-400 font-medium">
                    <span>Factor Breakdown</span>
                    <span className="text-blue-400">{op.theme}</span>
                  </div>
                  <div className="grid grid-cols-4 gap-1.5 pt-1">
                    <div className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-center">
                      <p className="text-[9px] text-slate-500">Momentum</p>
                      <p className="text-xs font-bold text-white">
                        {((op.factors.momentum || 0.5) * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-center">
                      <p className="text-[9px] text-slate-500">Trend</p>
                      <p className="text-xs font-bold text-white">
                        {((op.factors.trend || 0.5) * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-center">
                      <p className="text-[9px] text-slate-500">Valuation</p>
                      <p className="text-xs font-bold text-white">
                        {((op.factors.valuation || 0.5) * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-center">
                      <p className="text-[9px] text-slate-500">Stability</p>
                      <p className="text-xs font-bold text-white">
                        {((op.factors.risk_stability || 0.5) * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-4 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs text-slate-300">
                  <div className="flex items-center gap-1.5 font-semibold text-slate-400 mb-1">
                    <Zap className="w-3.5 h-3.5 text-amber-400" />
                    Recommendation: <span className="text-emerald-400">{op.recommendation}</span>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    RSI-14: {op.factor_inputs?.rsi_14?.toFixed(1) || "50.0"} • Fwd P/E: {op.factor_inputs?.forward_pe?.toFixed(1) || "N/A"}x
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                <span className="flex items-center gap-1 text-slate-500 text-[10px]">
                  <Clock className="w-3 h-3" />
                  {op.provenance?.freshness || "LIVE"}
                </span>
                <Link
                  href={`/company/${op.symbol}`}
                  className="px-3 py-1.5 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-blue-400 font-semibold flex items-center gap-1 transition-all"
                >
                  Research Deep Dive <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
