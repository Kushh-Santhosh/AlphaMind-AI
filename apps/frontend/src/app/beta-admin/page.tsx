"use client";

import React, { useState } from "react";
import {
  ShieldAlert,
  Users,
  Activity,
  FileSpreadsheet,
  FileCode,
  Bug,
  Sparkles,
  Layout,
  Gauge,
  Calendar,
} from "lucide-react";

interface FeedbackItem {
  feedback_id: string;
  category: "Bug" | "UI Issue" | "AI Quality" | "Performance" | "Feature Request" | "Other";
  triage_priority: "Critical" | "High" | "Medium" | "Low";
  title: string;
  description: string;
  affected_page: string;
  browser: string;
  timestamp_utc: string;
  app_version: string;
  status: string;
}

const SAMPLE_FEEDBACK_QUEUE: FeedbackItem[] = [
  {
    feedback_id: "fb_001",
    category: "UI Issue",
    triage_priority: "Low",
    title: "Sidebar version badge tooltip",
    description: "Beta version badge text is crisp; recommend adding hover tooltip.",
    affected_page: "/mission-control",
    browser: "Chrome 127.0 (macOS)",
    timestamp_utc: "2026-08-04T22:30:00Z",
    app_version: "v3.0.0-beta",
    status: "TRIAGED",
  },
  {
    feedback_id: "fb_002",
    category: "Feature Request",
    triage_priority: "Medium",
    title: "Export portfolio allocations to PDF",
    description: "Requesting a one-click PDF export for the 5 Virtual AI Fund snapshots.",
    affected_page: "/v2-fund",
    browser: "Safari 17.5 (macOS)",
    timestamp_utc: "2026-08-04T23:15:00Z",
    app_version: "v3.0.0-beta",
    status: "TRIAGED",
  },
];

const priorityColor: Record<string, string> = {
  Critical: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  High: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  Medium: "bg-blue-500/10 text-blue-400 border-blue-500/30",
  Low: "bg-slate-800 text-slate-400 border-slate-700",
};

const categoryIcon: Record<string, React.ElementType> = {
  Bug: Bug,
  "UI Issue": Layout,
  "AI Quality": Sparkles,
  Performance: Gauge,
  "Feature Request": Sparkles,
  Other: Activity,
};

export default function BetaAdminPage() {
  const [feedbackQueue] = useState<FeedbackItem[]>(SAMPLE_FEEDBACK_QUEUE);
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");

  const filteredQueue =
    selectedCategory === "ALL"
      ? feedbackQueue
      : feedbackQueue.filter((f) => f.category === selectedCategory);

  const handleExportJSON = () => {
    const blob = new Blob([JSON.stringify(feedbackQueue, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `alphamind_beta_feedback_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportCSV = () => {
    const headers = "feedback_id,category,triage_priority,title,affected_page,app_version,timestamp_utc\n";
    const rows = feedbackQueue.map(
      (f) => `${f.feedback_id},${f.category},${f.triage_priority},"${f.title}",${f.affected_page},${f.app_version},${f.timestamp_utc}`
    );
    const blob = new Blob([headers + rows.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `alphamind_beta_feedback_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold text-slate-100">Private Beta Operations & Admin Control</h1>
            <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
              v3.0.0-beta
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Monitor Private Beta active telemetry, triaged bug queue, feedback export, and weekly beta operational metrics.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleExportCSV}
            className="px-3 py-2 rounded-lg bg-emerald-600/15 hover:bg-emerald-600/25 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <FileSpreadsheet className="w-3.5 h-3.5" /> Export CSV
          </button>
          <button
            onClick={handleExportJSON}
            className="px-3 py-2 rounded-lg bg-blue-600/15 hover:bg-blue-600/25 border border-blue-500/30 text-blue-300 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <FileCode className="w-3.5 h-3.5" /> Export JSON
          </button>
        </div>
      </div>

      {/* Analytics Telemetry Strip (Marked Awaiting Beta Data) */}
      <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Users className="w-4 h-4 text-blue-400" /> Beta Telemetry & User Analytics
          </span>
          <span className="bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2.5 py-0.5 rounded text-[10px] font-bold">
            Awaiting Beta Data
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {[
            { label: "New Users", val: "Awaiting Beta Data" },
            { label: "Daily Active Users (DAU)", val: "Awaiting Beta Data" },
            { label: "Avg Session Duration", val: "Awaiting Beta Data" },
            { label: "7-Day Retention", val: "Awaiting Beta Data" },
            { label: "System Crash Count", val: "0 Crashes" },
          ].map(({ label, val }) => (
            <div key={label} className="p-3 rounded-lg bg-[#0d1322] border border-slate-800">
              <div className="text-[10px] text-slate-500">{label}</div>
              <div className="text-xs font-bold text-slate-300 mt-1">{val}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Beta Metrics Matrix (Marked Awaiting Beta Data) */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {[
          { label: "Activation Rate", value: "Awaiting Beta Data" },
          { label: "Time to First Value", value: "Awaiting Beta Data" },
          { label: "Task Completion Rate", value: "Awaiting Beta Data" },
          { label: "Retention Rate", value: "Awaiting Beta Data" },
          { label: "User Satisfaction", value: "Awaiting Beta Data" },
        ].map(({ label, value }) => (
          <div key={label} className="p-3.5 rounded-xl bg-[#0d1322] border border-slate-800 text-center space-y-1">
            <span className="text-[10px] text-slate-500 font-medium">{label}</span>
            <p className="text-xs font-bold text-amber-400">{value}</p>
          </div>
        ))}
      </div>

      {/* Categorized Bug Triage & Feedback Queue */}
      <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
          <div>
            <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-violet-400" /> Categorized Bug Triage & Feedback Queue
            </h2>
            <p className="text-[11px] text-slate-400">
              Showing {filteredQueue.length} feedback submissions. Each bug links to affected page, browser, timestamp, and version.
            </p>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {["ALL", "Bug", "UI Issue", "AI Quality", "Performance", "Feature Request", "Other"].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold border transition-colors ${
                  selectedCategory === cat
                    ? "bg-violet-600/20 text-violet-300 border-violet-500/40"
                    : "bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Queue Table */}
        <div className="space-y-3">
          {filteredQueue.map((item) => {
            const Icon = categoryIcon[item.category] ?? Activity;
            const prioCls = priorityColor[item.triage_priority] ?? priorityColor.Low;
            return (
              <div
                key={item.feedback_id}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all space-y-2"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400">
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-slate-100">{item.title}</span>
                        <span className="text-[9px] text-slate-500 font-mono bg-slate-800 px-1.5 py-0.5 rounded">
                          {item.feedback_id}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">{item.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${prioCls}`}>
                      {item.triage_priority} Priority
                    </span>
                    <span className="text-[10px] font-semibold text-slate-400 bg-slate-800 border border-slate-700 px-2 py-0.5 rounded">
                      {item.category}
                    </span>
                  </div>
                </div>

                {/* Metadata details */}
                <div className="flex items-center gap-4 text-[10px] text-slate-500 pt-2 border-t border-slate-800/60">
                  <span>
                    Affected Page: <code className="text-slate-300 font-mono">{item.affected_page}</code>
                  </span>
                  <span>·</span>
                  <span>Browser: <span className="text-slate-400">{item.browser}</span></span>
                  <span>·</span>
                  <span>Time: <span className="text-slate-400">{new Date(item.timestamp_utc).toLocaleTimeString()}</span></span>
                  <span>·</span>
                  <span>Version: <span className="text-blue-400 font-mono">{item.app_version}</span></span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Weekly Beta Summary Generation Card */}
      <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Calendar className="w-4 h-4 text-emerald-400" /> Weekly Beta Operations Summary
          </h3>
          <span className="text-[10px] text-emerald-400 font-mono font-bold bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
            Week 1 Active
          </span>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          Operational Summary: 2 triaged feedback items logged, 0 critical/high bugs, 0 crashes observed, user telemetry marked <strong>Awaiting Beta Data</strong> until first live beta cohorts onboard.
        </p>
      </div>
    </div>
  );
}
