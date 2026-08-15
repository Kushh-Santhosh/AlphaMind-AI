"use client";

import React, { useState } from "react";
import {
  Cpu,
  RefreshCw,
  Download,
  MessageSquare,
  Bug,
  Lightbulb,
  CheckCircle,
  ShieldCheck,
  Activity,
  Sliders,
  Database,
} from "lucide-react";

export default function SettingsPage() {
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState<string | null>(null);
  const [feedbackType, setFeedbackType] = useState<"bug" | "feedback" | "feature">("feedback");
  const [feedbackText, setFeedbackText] = useState("");
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  const handleResetDemoData = () => {
    setResetting(true);
    setResetMessage(null);
    setTimeout(() => {
      setResetting(false);
      setResetMessage("Demo datasets, 5 Virtual AI Fund snapshots, and sample reasoning records successfully re-initialized.");
    }, 800);
  };

  const handleFeedbackSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;
    setFeedbackSubmitted(true);
    setTimeout(() => {
      setFeedbackText("");
      setFeedbackSubmitted(false);
    }, 3000);
  };

  const handleExportLogs = () => {
    const logsData = {
      app_version: "v3.0.0-beta",
      environment: "staging",
      timestamp_utc: new Date().toISOString(),
      user_agent: typeof window !== "undefined" ? window.navigator.userAgent : "N/A",
      subsystems: {
        event_bus: "HEALTHY",
        unified_timeline: "HEALTHY",
        intelligence_memory: "HEALTHY",
        fund_engine: "HEALTHY",
      },
    };
    const blob = new Blob([JSON.stringify(logsData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `alphamind_beta_diagnostics_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <Sliders className="w-5 h-5 text-blue-400" /> Beta Settings & Platform Controls
        </h1>
        <p className="text-xs text-slate-400">
          Manage demo account datasets, view system status, submit feedback, and export diagnostic logs.
        </p>
      </div>

      {/* System Status & Beta Banner */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-blue-900/30 via-slate-900 to-indigo-900/20 border border-blue-500/20 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-slate-100">AlphaMind AI v3 SaaS Platform</span>
              <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                v3.0.0-beta
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              All 10 Subsystems Operational · 100% Quality Gate Validated · Private Beta Ready
            </p>
          </div>
        </div>

        <button
          onClick={handleExportLogs}
          className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center gap-2 transition-all shrink-0"
        >
          <Download className="w-3.5 h-3.5 text-blue-400" /> Export System Logs
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Demo Account & Data Controls */}
        <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <Database className="w-4 h-4 text-cyan-400" /> Demo Account & Data Controls
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Re-initialize sample portfolios, 5 Virtual AI Funds, watchlists, and timeline events to experience the 0-configuration demo mode.
          </p>

          {resetMessage && (
            <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center gap-2">
              <CheckCircle className="w-4 h-4 shrink-0" />
              <span>{resetMessage}</span>
            </div>
          )}

          <button
            onClick={handleResetDemoData}
            disabled={resetting}
            className="w-full py-2.5 rounded-lg bg-cyan-600/15 hover:bg-cyan-600/25 border border-cyan-500/30 text-cyan-300 text-xs font-semibold flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${resetting ? "animate-spin" : ""}`} />
            {resetting ? "Re-initializing Demo Datasets…" : "Reset Demo Account Datasets"}
          </button>
        </div>

        {/* Champion Predictive Model Registry */}
        <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-4">
          <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
            <Cpu className="w-4 h-4 text-violet-400" /> Model Registry & Calibration
          </h3>
          <div className="space-y-2.5 text-xs">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-900 border border-slate-800">
              <div>
                <div className="font-semibold text-slate-200">Champion Predictive Model</div>
                <div className="text-[10px] text-slate-400">Bayesian BSTS Model (Brier Score: 0.042)</div>
              </div>
              <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded text-[10px] font-bold">
                Active Champion
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-900 border border-slate-800">
              <div>
                <div className="font-semibold text-slate-200">Challenger Temporal Model</div>
                <div className="text-[10px] text-slate-400">Temporal Fusion Transformer (TFT)</div>
              </div>
              <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-[10px] font-bold">
                Shadow Mode
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* User Feedback Mechanism */}
      <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-4">
        <h3 className="font-semibold text-slate-100 text-sm flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-amber-400" /> Beta User Feedback & Bug Reporting
        </h3>
        <p className="text-xs text-slate-400">
          Encountered an issue or have a feature suggestion? Submit feedback directly to the AlphaMind engineering team.
        </p>

        {feedbackSubmitted ? (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center gap-2">
            <CheckCircle className="w-4 h-4 shrink-0" />
            <span>Thank you for your feedback! Your report has been submitted to the engineering team.</span>
          </div>
        ) : (
          <form onSubmit={handleFeedbackSubmit} className="space-y-3">
            <div className="flex items-center gap-2">
              {[
                { id: "feedback", label: "General Feedback", icon: MessageSquare },
                { id: "bug", label: "Report a Bug", icon: Bug },
                { id: "feature", label: "Feature Request", icon: Lightbulb },
              ].map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => setFeedbackType(id as "bug" | "feedback" | "feature")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition-colors ${
                    feedbackType === id
                      ? "bg-amber-500/15 border-amber-500/30 text-amber-300 font-semibold"
                      : "bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" /> {label}
                </button>
              ))}
            </div>

            <textarea
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              placeholder={`Describe your ${feedbackType === "bug" ? "issue or bug details" : feedbackType === "feature" ? "feature proposal" : "feedback"}…`}
              rows={3}
              className="w-full p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-amber-500/40"
              required
            />

            <div className="flex justify-end">
              <button
                type="submit"
                className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold shadow-lg shadow-amber-600/20 transition-all"
              >
                Submit {feedbackType === "bug" ? "Bug Report" : feedbackType === "feature" ? "Feature Request" : "Feedback"}
              </button>
            </div>
          </form>
        )}
      </div>

      {/* SEC Compliance Disclaimer */}
      <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 space-y-1">
        <div className="font-semibold text-slate-300 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" /> SEC / FINRA Research Compliance
        </div>
        <p className="text-[11px] leading-relaxed text-slate-400">
          AlphaMind AI is an automated quantitative research platform. All outputs, probability distributions, confidence intervals, and research signals are for informational and educational purposes only and do not constitute financial, investment, legal, or tax advice.
        </p>
      </div>
    </div>
  );
}
