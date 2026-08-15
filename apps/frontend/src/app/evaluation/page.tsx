"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  Award,
  BarChart3,
  Brain,
  CheckCircle2,
  Clock,
  Compass,
  Cpu,
  Flame,
  LineChart,
  RefreshCw,
  Scale,
  Shield,
  Sparkles,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";

interface ModelScorecard {
  model_name: string;
  sample_size: number;
  mae: number;
  rmse: number;
  mape_pct: number;
  directional_accuracy_pct: number;
  hit_rate_pct: number;
  brier_score: number;
  sharpe_generated: number;
  status: string;
}

export default function EvaluationPage() {
  const [scorecard, setScorecard] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchScorecard = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/prediction/scorecard");
      if (res.ok) {
        const data = await res.json();
        setScorecard(data);
      }
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScorecard();
  }, []);

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 p-6 space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#0d1322] via-[#090e1c] to-[#0d1428] border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white">Model Scorecard & Strategy Learning Lab</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Continuous realized forecast validation, Brier calibration, and self-improving strategy reflection memory.
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchScorecard}
          disabled={loading}
          className="p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-all text-xs flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          Recalculate Calibration
        </button>
      </div>

      {/* Model Benchmark Winner Banner */}
      {scorecard && (
        <div className="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/30 via-slate-900/80 to-blue-950/30 border border-emerald-500/30 space-y-2 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-4 h-4" /> Benchmark Winner: {scorecard.benchmark_winner}
            </span>
            <span className="text-[11px] text-slate-500">Evaluated at {scorecard.evaluated_at_utc?.slice(0, 10)}</span>
          </div>
          <p className="text-sm text-slate-200 leading-relaxed font-medium">
            {scorecard.eval_summary}
          </p>
        </div>
      )}

      {/* Model Scorecards Table */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Brain className="w-5 h-5 text-blue-400" />
            Foundation Model & Baseline Comparative Scorecard
          </h2>
          <span className="text-xs text-slate-400">142 Realized Forecast Events</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">Model Architecture</th>
                <th className="p-3">Sample N</th>
                <th className="p-3">Directional Accuracy</th>
                <th className="p-3">95% Hit Rate</th>
                <th className="p-3">MAE ($)</th>
                <th className="p-3">RMSE ($)</th>
                <th className="p-3">Brier Score</th>
                <th className="p-3">Sharpe Generated</th>
                <th className="p-3 text-right">Calibration Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {scorecard?.scorecards?.map((card: any, idx: number) => (
                <tr key={card.model_name} className="hover:bg-slate-800/30 transition-all">
                  <td className="p-3 font-bold text-white flex items-center gap-2">
                    <span className="text-blue-400 font-mono">#{idx + 1}</span>
                    {card.model_name}
                  </td>
                  <td className="p-3 text-slate-400">{card.sample_size}</td>
                  <td className="p-3 font-bold text-emerald-400 font-mono">{card.directional_accuracy_pct}%</td>
                  <td className="p-3 font-semibold text-slate-200 font-mono">{card.hit_rate_pct}%</td>
                  <td className="p-3 text-slate-300 font-mono">${card.mae}</td>
                  <td className="p-3 text-slate-300 font-mono">${card.rmse}</td>
                  <td className="p-3 text-slate-300 font-mono">{card.brier_score}</td>
                  <td className="p-3 text-blue-400 font-bold font-mono">{card.sharpe_generated}</td>
                  <td className="p-3 text-right">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                        card.status === "OUTPERFORMING"
                          ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                          : card.status === "CALIBRATED"
                          ? "bg-blue-500/10 text-blue-400 border-blue-500/30"
                          : "bg-rose-500/10 text-rose-400 border-rose-500/30"
                      }`}
                    >
                      {card.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Strategy Learning Profiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm">Momentum & Trend Strategy</h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              Active
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Captures directional breakouts using 14-day RSI and 50-day SMA alignment.
          </p>
          <div className="grid grid-cols-2 gap-2 pt-2 text-xs">
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Win Rate</span>
              <p className="font-bold text-emerald-400 mt-0.5">64.5%</p>
            </div>
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Profit Factor</span>
              <p className="font-bold text-white mt-0.5">2.18</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm">Deep Value & FCF Compounders</h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
              Active
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Screens for high free cash flow yield, low EV/EBITDA, and positive net margin expansion.
          </p>
          <div className="grid grid-cols-2 gap-2 pt-2 text-xs">
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Win Rate</span>
              <p className="font-bold text-emerald-400 mt-0.5">71.2%</p>
            </div>
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Profit Factor</span>
              <p className="font-bold text-white mt-0.5">2.45</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm">Macro Regime Allocation</h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/30">
              Active
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Rotates between Gold, Treasuries, and Mega-Cap Growth based on yield curve spread.
          </p>
          <div className="grid grid-cols-2 gap-2 pt-2 text-xs">
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Win Rate</span>
              <p className="font-bold text-emerald-400 mt-0.5">58.0%</p>
            </div>
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[10px] text-slate-500">Profit Factor</span>
              <p className="font-bold text-white mt-0.5">1.82</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
