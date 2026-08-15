"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Activity,
  ArrowRight,
  BarChart3,
  Brain,
  Building2,
  CheckCircle2,
  ChevronRight,
  Cpu,
  Eye,
  Flame,
  Globe,
  Layers,
  LineChart,
  PieChart,
  Radar,
  Scale,
  Search,
  ShieldAlert,
  Sparkles,
  Swords,
  TrendingUp,
  Zap,
} from "lucide-react";

export default function HomePage() {
  const [activeWorkflowStep, setActiveWorkflowStep] = useState<number>(2);

  const workflowSteps = [
    {
      step: 1,
      title: "Universal Data Ingestion",
      desc: "Live stream ingestion across SEC EDGAR 10-K/8-K, Yahoo Finance, FRED macro feeds, and crypto markets with provenance and freshness badging.",
      badge: "DATA LAYER",
    },
    {
      step: 2,
      title: "8 Specialized AI Analysts Fan-Out",
      desc: "Technical, Fundamental, Valuation (DCF), News, Sentiment, Macro, Regime, and Earnings Analysts compute structured domain vectors in parallel.",
      badge: "ANALYST TEAM",
    },
    {
      step: 3,
      title: "Adversarial Bull vs Bear Debate",
      desc: "Dialectical debate between Bull and Bear researchers. Contradictions are refereed by Research Manager to form probabilistic distributions.",
      badge: "DEBATE LAYER",
    },
    {
      step: 4,
      title: "Trader & Risk Committee Oversight",
      desc: "Trader Agent proposes entry zones and sizing; Risk Committee (Conservative, Moderate, Aggressive debaters) enforce position and drawdown caps.",
      badge: "GOVERNANCE",
    },
    {
      step: 5,
      title: "5 Virtual AI Strategy Funds",
      desc: "Allocations execute in realistic paper exchange with dynamic slippage, spreads, and transaction fee models; feedback feeds strategy learning memory.",
      badge: "EXECUTION & LEARNING",
    },
  ];

  return (
    <div className="space-y-12 pb-16 text-slate-100">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-[#0e162b] via-[#090e1c] to-[#060a14] border border-blue-500/20 p-8 md:p-14 shadow-2xl">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-cyan-500/10 via-blue-600/10 to-transparent blur-3xl pointer-events-none" />
        
        <div className="relative z-10 max-w-4xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 animate-spin" /> AlphaMind AI v4 — TradingAgents-Level Intelligence
          </div>

          <h1 className="text-4xl md:text-6xl font-black tracking-tight text-white leading-tight">
            Your Institutional AI Investment Research{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400">
              Operating System
            </span>
          </h1>

          <p className="text-base md:text-lg text-slate-300 leading-relaxed max-w-3xl">
            Unifying multi-agent dialectical research debate, SEC EDGAR filing lineage, 7 mathematical portfolio optimization solvers, 
            universal opportunity scanning, and realistic paper simulation. Built for quantitative researchers and institutional analysts.
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              href="/mission-control"
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 text-slate-950 font-extrabold text-sm shadow-xl shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-[1.02] transition-all flex items-center gap-2"
            >
              <Brain className="w-4 h-4 text-slate-950" />
              <span>Explore Mission Control 2.0</span>
              <ArrowRight className="w-4 h-4 text-slate-950" />
            </Link>

            <Link
              href="/scanner"
              className="px-6 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700 text-slate-200 font-bold text-sm transition-all flex items-center gap-2 shadow-lg"
            >
              <Radar className="w-4 h-4 text-cyan-400" />
              <span>AI Opportunity Scanner</span>
            </Link>

            <Link
              href="/company/NVDA"
              className="px-5 py-3.5 rounded-xl bg-slate-900/50 hover:bg-slate-800/80 border border-slate-800 text-slate-400 hover:text-slate-200 font-medium text-sm transition-all flex items-center gap-2"
            >
              <Building2 className="w-4 h-4" />
              <span>NVDA Research Terminal</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Interactive AI Workflow Visualization */}
      <section className="bg-[#0b101f] border border-slate-800/90 rounded-2xl p-6 md:p-8 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-4">
          <div>
            <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-cyan-400" /> How AlphaMind AI Makes Investment Decisions
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Deterministic single-prompt LLM questions are strictly prohibited. Every recommendation flows through a 5-stage dialectical graph.
            </p>
          </div>
          <span className="text-[11px] font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-full border border-cyan-500/20">
            Interactive Architecture Diagram
          </span>
        </div>

        {/* Step Selector Pills */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
          {workflowSteps.map((s, idx) => (
            <button
              key={s.step}
              onClick={() => setActiveWorkflowStep(idx)}
              className={`p-3 rounded-xl text-left border transition-all text-xs flex flex-col justify-between gap-1.5 ${
                activeWorkflowStep === idx
                  ? "bg-cyan-500/15 border-cyan-500/60 text-white shadow-lg shadow-cyan-950/40"
                  : "bg-slate-950/60 border-slate-800/80 text-slate-400 hover:border-slate-700"
              }`}
            >
              <span className="text-[10px] font-mono font-bold text-cyan-400 uppercase">{s.badge}</span>
              <span className="font-bold text-slate-200">{s.title}</span>
            </button>
          ))}
        </div>

        {/* Active Step Showcase Card */}
        <div className="p-6 rounded-xl bg-gradient-to-r from-slate-950 via-[#0d1428] to-slate-950 border border-cyan-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
              Stage {workflowSteps[activeWorkflowStep].step}: {workflowSteps[activeWorkflowStep].badge}
            </span>
            <h3 className="text-lg font-bold text-white">{workflowSteps[activeWorkflowStep].title}</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {workflowSteps[activeWorkflowStep].desc}
            </p>
          </div>

          <div className="shrink-0">
            <Link
              href="/mission-control"
              className="px-4 py-2 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30 text-xs font-bold transition-all flex items-center gap-1.5"
            >
              <span>View in Mission Control</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Core Terminal Pillars (6 Pillars Grid) */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Pillar 1: Adversarial Debate */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Swords className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            Adversarial Research Debate
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Bull Researcher and Bear Researcher engage in multi-round dialectical confrontation. Contradictions are resolved into probabilistic scenarios.
          </p>
          <Link href="/compare" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Debate Workbench</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Pillar 2: Opportunity Scanner */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Radar className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            Universal Opportunity Scanner
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Continuous screening across US Equities, Indian Equities (NSE), Global ETFs, and Crypto by Momentum, Value, Earnings Surprises, and Macro fit.
          </p>
          <Link href="/scanner" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Launch Scanner</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Pillar 3: Walk-Forward Backtester */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <LineChart className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            Institutional Backtesting
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Rigorous walk-forward validation with explicit in-sample and out-of-sample segmentation, slippage modeling, and benchmark attribution.
          </p>
          <Link href="/backtesting" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Run Backtester</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Pillar 4: Crisis Stress Testing */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            Crisis Stress Engine
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Simulate portfolio capital preservation against 2008 Subprime, 2020 COVID crash, 2022 Fed rate shocks, and crypto flash liquidity freezes.
          </p>
          <Link href="/risk" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Inspect Risk Suite</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Pillar 5: 5 Virtual AI Strategy Funds */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <PieChart className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            5 Virtual AI Strategy Funds
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Autonomous multi-strategy funds competing under transparent risk constraints: Deep Value, Momentum Alpha, Macro Tactical, Risk Parity, and Tech Growth.
          </p>
          <Link href="/portfolio" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Fund Leaderboards</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Pillar 6: Brier Calibration & Learning Memory */}
        <div className="p-6 rounded-2xl bg-[#0a0f1d] border border-slate-800/90 hover:border-cyan-500/40 transition-all space-y-3 group">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
            Self-Improving Learning Memory
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Realized outcome tracking, directional accuracy verification, Brier score calibration, and historical reflection memory adaptation.
          </p>
          <Link href="/evaluation" className="text-xs font-bold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 pt-2">
            <span>Calibration Dashboard</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </section>

      {/* Live System Telemetry Banner */}
      <section className="p-6 rounded-2xl bg-[#080d1a] border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-3 h-3 rounded-full bg-emerald-400 animate-ping shrink-0" />
          <div>
            <div className="text-xs font-bold text-white flex items-center gap-2">
              <span>Universal Model Gateway & Provider Registry Active</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                HEALTHY (99.9%)
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Supporting OpenAI (GPT-4o, o1), Anthropic (Claude 3.5), Google (Gemini 2.5), DeepSeek, and Ollama.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/settings"
            className="px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 transition-all"
          >
            Configure Gateways
          </Link>
          <Link
            href="/mission-control"
            className="px-4 py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-xs font-bold transition-all"
          >
            Terminal Live Feed →
          </Link>
        </div>
      </section>
    </div>
  );
}
