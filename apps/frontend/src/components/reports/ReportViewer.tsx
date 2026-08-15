"use client";

import { FileCode, FileText, Printer, ShieldCheck } from "lucide-react";

interface ReportViewerProps {
  reportId?: string;
  title?: string;
  summaryText?: string;
}

export function ReportViewer({
  reportId = "rep_exec_8f12a9",
  title = "Standardized Institutional Executive Summary — AAPL",
  summaryText = "Multi-engine research evaluation compiled across SEC 10-K financial statements, FRED interest rate macro series, and 10,000 Monte Carlo stochastic return trajectories.",
}: ReportViewerProps) {
  const handleExportMarkdown = () => {
    const md = `# ${title}\n\n${summaryText}\n\n*Report ID: ${reportId}*`;
    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${reportId}.md`;
    a.click();
  };

  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6">
      {/* Report Action Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-slate-100 text-base">{title}</h1>
            <p className="text-xs text-slate-400">Report ID: {reportId} | 100% Audit Lineage Verified</p>
          </div>
        </div>

        {/* Export Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExportMarkdown}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
          >
            <FileCode className="w-3.5 h-3.5" /> Export Markdown
          </button>
          <button
            onClick={() => window.print()}
            className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shadow-lg shadow-blue-500/20"
          >
            <Printer className="w-3.5 h-3.5" /> Print / PDF
          </button>
        </div>
      </div>

      {/* Body Content */}
      <div className="space-y-4 text-xs leading-relaxed text-slate-300">
        <div className="p-4 rounded-lg bg-slate-900/80 border border-slate-800">
          <h3 className="font-semibold text-slate-100 text-xs mb-1 uppercase tracking-wider text-blue-400">
            Executive Summary
          </h3>
          <p>{summaryText}</p>
        </div>

        <div className="space-y-2">
          <h3 className="font-semibold text-slate-100 text-sm">Key Findings & Factor Lineage</h3>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Operating Income Margin: 29.8% (Source: SEC Form 10-K Item 8)</li>
            <li>30-Day Mean Implied Return: +3.4% (95% CI: [-12.0%, +18.0%])</li>
            <li>Concentration HHI Index: 0.1250 (N_eff = 8.0 effective position count)</li>
          </ul>
        </div>
      </div>

      {/* Audit Metadata Box */}
      <div className="p-3 rounded-lg bg-[#090d16] border border-slate-800/80 text-[11px] text-slate-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Versions: Forecast v1.2 | Model v3.0 | KG v1.0</span>
        </div>
        <span className="font-mono text-slate-500">SEC / FINRA Educational Disclaimer Applied</span>
      </div>
    </div>
  );
}
