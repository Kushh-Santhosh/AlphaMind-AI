"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Building2,
  CheckCircle2,
  ChevronRight,
  Clock,
  Flame,
  Plus,
  RefreshCw,
  Scale,
  Search,
  Sparkles,
  TrendingUp,
  X,
} from "lucide-react";

interface AssetProfile {
  symbol: string;
  price: number;
  change_pct: number;
  market_cap_usd: number;
  forward_pe: number;
  ev_to_ebitda: number;
  rsi_14: number;
  ai_opportunity_score: number;
  valuation_verdict: string;
  provenance?: any;
}

export default function ComparePeersPage() {
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>(["NVDA", "MSFT", "AAPL", "GOOGL"]);
  const [inputTicker, setInputTicker] = useState<string>("");
  const [profiles, setProfiles] = useState<AssetProfile[]>([]);
  const [synthesis, setSynthesis] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchComparison = async () => {
    if (selectedSymbols.length < 2) return;
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch("/api/v1/compare/assets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbols: selectedSymbols }),
      });
      if (res.ok) {
        const data = await res.json();
        setProfiles(data.profiles || []);
        setSynthesis(data.synthesis || null);
      } else {
        const err = await res.json();
        setErrorMsg(err.detail || "Failed to compare selected assets");
      }
    } catch (err: any) {
      setErrorMsg("Network error connecting to compare service");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison();
  }, [selectedSymbols]);

  const addTicker = () => {
    const sym = inputTicker.trim().toUpperCase();
    if (sym && !selectedSymbols.includes(sym) && selectedSymbols.length < 10) {
      setSelectedSymbols([...selectedSymbols, sym]);
      setInputTicker("");
    }
  };

  const removeTicker = (sym: string) => {
    if (selectedSymbols.length > 2) {
      setSelectedSymbols(selectedSymbols.filter((s) => s !== sym));
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 p-6 space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#0d1322] via-[#090e1c] to-[#0d1428] border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
              <Scale className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white">Multi-Asset Peer Comparison</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Benchmark 2 to 10 assets side-by-side using live provider market data and quantitative factors.
              </p>
            </div>
          </div>
        </div>

        {/* Add Ticker Input */}
        <div className="flex items-center gap-2 w-full md:w-auto">
          <div className="relative flex-1 md:w-48">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Add Ticker (e.g. TSLA, BTC)"
              value={inputTicker}
              onChange={(e) => setInputTicker(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addTicker()}
              className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>
          <button
            onClick={addTicker}
            className="p-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition-all text-xs font-semibold flex items-center gap-1"
          >
            <Plus className="w-4 h-4" />
            Add
          </button>
          <button
            onClick={fetchComparison}
            disabled={loading}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-all text-xs"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* Selected Ticker Chips */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-slate-400 font-medium mr-2">Active Candidates ({selectedSymbols.length}/10):</span>
        {selectedSymbols.map((sym) => (
          <div
            key={sym}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-white shadow-sm"
          >
            <span>{sym}</span>
            {selectedSymbols.length > 2 && (
              <button
                onClick={() => removeTicker(sym)}
                className="text-slate-500 hover:text-rose-400 transition-all"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        ))}
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {errorMsg}
        </div>
      )}

      {/* Side-by-Side Comparison Matrix */}
      <div className="rounded-2xl bg-slate-900/60 border border-slate-800 overflow-hidden shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-400" />
            <h2 className="text-base font-bold text-white">Quantitative & Valuation Matrix</h2>
          </div>
          <span className="text-xs text-slate-400">Live Provider Data</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-4">Asset Symbol</th>
                <th className="p-4">Live Price</th>
                <th className="p-4">24h Change</th>
                <th className="p-4">Market Cap</th>
                <th className="p-4">Forward P/E</th>
                <th className="p-4">EV/EBITDA</th>
                <th className="p-4">RSI (14)</th>
                <th className="p-4">AI Score</th>
                <th className="p-4">Valuation Verdict</th>
                <th className="p-4">Freshness</th>
                <th className="p-4 text-right">Deep Dive</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr>
                  <td colSpan={11} className="p-12 text-center text-slate-400">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto text-blue-400 mb-2" />
                    Calculating multi-asset quantitative factors from live feeds...
                  </td>
                </tr>
              ) : profiles.length === 0 ? (
                <tr>
                  <td colSpan={11} className="p-8 text-center text-slate-500">
                    No comparison data returned.
                  </td>
                </tr>
              ) : (
                profiles.map((p) => (
                  <tr key={p.symbol} className="hover:bg-slate-800/30 transition-all">
                    <td className="p-4 font-bold text-white flex items-center gap-2">
                      <div className="w-6 h-6 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-[10px] text-blue-400">
                        {p.symbol.slice(0, 2)}
                      </div>
                      {p.symbol}
                    </td>
                    <td className="p-4 font-semibold text-white">
                      {p.symbol.endsWith(".NS") ? "₹" : "$"}{p.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className={`p-4 font-semibold ${p.change_pct >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                      {p.change_pct >= 0 ? "+" : ""}{p.change_pct.toFixed(2)}%
                    </td>
                    <td className="p-4 text-slate-300">
                      {p.market_cap_usd > 1e12
                        ? `$${(p.market_cap_usd / 1e12).toFixed(2)}T`
                        : `$${(p.market_cap_usd / 1e9).toFixed(2)}B`}
                    </td>
                    <td className="p-4 text-slate-300">{p.forward_pe ? `${p.forward_pe.toFixed(1)}x` : "N/A"}</td>
                    <td className="p-4 text-slate-300">{p.ev_to_ebitda ? `${p.ev_to_ebitda.toFixed(1)}x` : "N/A"}</td>
                    <td className="p-4 text-slate-300 font-medium">{p.rsi_14.toFixed(1)}</td>
                    <td className="p-4">
                      <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                        {p.ai_opportunity_score.toFixed(1)}
                      </span>
                    </td>
                    <td className="p-4">
                      <span
                        className={`px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${
                          p.valuation_verdict === "UNDERVALUED"
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                            : "bg-slate-800 text-slate-400 border-slate-700"
                        }`}
                      >
                        {p.valuation_verdict}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className="flex items-center gap-1 text-[10px] text-slate-400">
                        <Clock className="w-3 h-3 text-slate-500" />
                        {p.provenance?.freshness || "LIVE"}
                      </span>
                    </td>
                    <td className="p-4 text-right">
                      <Link
                        href={`/company/${p.symbol}`}
                        className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 font-semibold text-xs"
                      >
                        Research <ChevronRight className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Synthesis Insight Card */}
      {synthesis && (
        <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-950/20 via-slate-900/60 to-purple-950/20 border border-slate-800 space-y-3 shadow-lg">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-blue-400" />
            <h2 className="text-base font-bold text-white">AI Relative Benchmarking Synthesis</h2>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            {synthesis.portfolio_allocation_recommendation}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
              <span className="text-[10px] font-semibold text-blue-400 uppercase tracking-wider">Top Overall Conviction</span>
              <p className="text-base font-bold text-white mt-0.5">{synthesis.top_overall_conviction}</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
              <span className="text-[10px] font-semibold text-emerald-400 uppercase tracking-wider">Top Momentum Leader</span>
              <p className="text-base font-bold text-white mt-0.5">{synthesis.top_momentum_asset}</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
              <span className="text-[10px] font-semibold text-purple-400 uppercase tracking-wider">Top Relative Value</span>
              <p className="text-base font-bold text-white mt-0.5">{synthesis.top_value_asset}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
