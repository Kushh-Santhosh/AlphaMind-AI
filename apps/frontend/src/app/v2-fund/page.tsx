"use client";

import React, { useState } from "react";
import { Trophy, BarChart3, Sparkles } from "lucide-react";

interface FundStrategy {
  fund_id: string;
  name: string;
  description: string;
  initial_capital_usd: number;
  current_market_value_usd: number;
  target_volatility_pct: number;
  max_drawdown_limit_pct: number;
  cagr_pct: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  brier_score: number;
  allocations: Record<string, number>;
}

const DEFAULT_FUNDS: FundStrategy[] = [
  {
    fund_id: "CONSERVATIVE",
    name: "Conservative Capital Preservation AI Fund",
    description: "Low-volatility capital preservation focusing on fixed income, quality dividend ETFs, and cash.",
    initial_capital_usd: 10000,
    current_market_value_usd: 10650,
    target_volatility_pct: 8.0,
    max_drawdown_limit_pct: -5.0,
    cagr_pct: 6.5,
    sharpe_ratio: 1.85,
    sortino_ratio: 2.40,
    brier_score: 0.042,
    allocations: { TLT: 0.4, SPY: 0.3, CASH: 0.3 },
  },
  {
    fund_id: "BALANCED",
    name: "Balanced Multi-Asset Growth AI Fund",
    description: "Classic 60/40 risk-adjusted growth balancing mega-cap equities and fixed income.",
    initial_capital_usd: 10000,
    current_market_value_usd: 11120,
    target_volatility_pct: 14.0,
    max_drawdown_limit_pct: -12.0,
    cagr_pct: 11.2,
    sharpe_ratio: 1.62,
    sortino_ratio: 2.10,
    brier_score: 0.048,
    allocations: { SPY: 0.5, TLT: 0.3, AAPL: 0.1, MSFT: 0.1 },
  },
  {
    fund_id: "GROWTH",
    name: "High-Growth Technology AI Fund",
    description: "Capital appreciation focusing on technology, semiconductor, and high-growth innovation factors.",
    initial_capital_usd: 10000,
    current_market_value_usd: 11850,
    target_volatility_pct: 20.0,
    max_drawdown_limit_pct: -18.0,
    cagr_pct: 18.5,
    sharpe_ratio: 1.45,
    sortino_ratio: 1.80,
    brier_score: 0.055,
    allocations: { QQQ: 0.4, NVDA: 0.25, AAPL: 0.2, MSFT: 0.15 },
  },
  {
    fund_id: "AGGRESSIVE",
    name: "Aggressive Momentum Alpha AI Fund",
    description: "High-beta momentum strategies seeking maximum equity alpha across market cycles.",
    initial_capital_usd: 10000,
    current_market_value_usd: 12640,
    target_volatility_pct: 28.0,
    max_drawdown_limit_pct: -25.0,
    cagr_pct: 26.4,
    sharpe_ratio: 1.28,
    sortino_ratio: 1.55,
    brier_score: 0.062,
    allocations: { NVDA: 0.35, QQQ: 0.35, AAPL: 0.3 },
  },
  {
    fund_id: "CRYPTO",
    name: "Digital Asset & Crypto Intelligence AI Fund",
    description: "Cryptocurrency and Web3 digital asset intelligence tracking spot BTC, ETH, and layer-1 protocols.",
    initial_capital_usd: 10000,
    current_market_value_usd: 14200,
    target_volatility_pct: 45.0,
    max_drawdown_limit_pct: -35.0,
    cagr_pct: 42.0,
    sharpe_ratio: 1.15,
    sortino_ratio: 1.35,
    brier_score: 0.071,
    allocations: { "BTC-USD": 0.6, "ETH-USD": 0.4 },
  },
];

export default function V2FundDashboardPage() {
  const [funds] = useState<FundStrategy[]>(DEFAULT_FUNDS);
  const [selectedFund, setSelectedFund] = useState<FundStrategy>(DEFAULT_FUNDS[0]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                AlphaMind v2.0 AI-OS
              </span>
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Multi-Fund Public Leaderboard
              </span>
            </div>
            <h1 className="text-3xl font-bold tracking-tight text-white mt-2 flex items-center gap-3">
              <Trophy className="w-8 h-8 text-amber-400" />
              Multi-Strategy Virtual AI Funds
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              5 permanent autonomous AI investment strategies competing 24×7 on paper capital.
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 text-right">
            <div className="text-xs text-slate-400">Total Virtual AUM</div>
            <div className="text-2xl font-mono font-bold text-emerald-400">$60,460.00</div>
            <div className="text-xs text-slate-500 mt-0.5">5 Virtual Paper Funds</div>
          </div>
        </div>

        {/* Public Leaderboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Top Ranking Cards */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-indigo-400" />
              Strategy Funds Leaderboard & Allocations
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {funds.map((f, idx) => (
                <div
                  key={f.fund_id}
                  onClick={() => setSelectedFund(f)}
                  className={`cursor-pointer rounded-xl p-5 border transition-all ${
                    selectedFund.fund_id === f.fund_id
                      ? "bg-slate-900 border-indigo-500 ring-1 ring-indigo-500"
                      : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      Rank #{idx + 1}
                    </span>
                    <span className="text-xs font-mono text-emerald-400 font-semibold">
                      +{f.cagr_pct}% CAGR
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-white mt-2 line-clamp-1">{f.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2">{f.description}</p>
                  
                  <div className="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase">Sharpe</div>
                      <div className="text-sm font-mono font-semibold text-indigo-300">{f.sharpe_ratio}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase">Sortino</div>
                      <div className="text-sm font-mono font-semibold text-teal-300">{f.sortino_ratio}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase">Brier Calibration</div>
                      <div className="text-sm font-mono font-semibold text-amber-300">{f.brier_score}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Selected Fund Inspector Panel */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
            <div>
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Fund Deep Inspection</span>
              <h3 className="text-xl font-bold text-white mt-1">{selectedFund.name}</h3>
              <p className="text-xs text-slate-400 mt-2">{selectedFund.description}</p>
            </div>

            <div className="space-y-3 pt-2">
              <div className="flex justify-between items-center text-sm py-1.5 border-b border-slate-800">
                <span className="text-slate-400">Current Valuation:</span>
                <span className="font-mono font-bold text-emerald-400">${selectedFund.current_market_value_usd.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center text-sm py-1.5 border-b border-slate-800">
                <span className="text-slate-400">Target Volatility:</span>
                <span className="font-mono text-white">{selectedFund.target_volatility_pct}%</span>
              </div>
              <div className="flex justify-between items-center text-sm py-1.5 border-b border-slate-800">
                <span className="text-slate-400">Max Drawdown Limit:</span>
                <span className="font-mono text-rose-400">{selectedFund.max_drawdown_limit_pct}%</span>
              </div>
              <div className="flex justify-between items-center text-sm py-1.5 border-b border-slate-800">
                <span className="text-slate-400">Sortino Ratio:</span>
                <span className="font-mono text-indigo-300 font-semibold">{selectedFund.sortino_ratio}</span>
              </div>
            </div>

            {/* Target Allocations */}
            <div>
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Asset Allocation Weights</h4>
              <div className="space-y-2">
                {Object.entries(selectedFund.allocations).map(([symbol, weight]) => (
                  <div key={symbol} className="space-y-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-200">{symbol}</span>
                      <span className="text-slate-400">{(weight * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5">
                      <div
                        className="bg-indigo-500 h-1.5 rounded-full"
                        style={{ width: `${weight * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-xs text-indigo-300 flex items-start gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
              <span>
                All 5 Virtual Funds are continuously rebalanced by the AlphaMind v2 Live OS Kernel based on incoming SEC filings and factor risk updates.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
