import { AlertTriangle } from "lucide-react";

export default function AlertsCenterPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Research & Platform Alerts Center</h1>
        <p className="text-xs text-slate-400">Drift notifications, SEC filing disclosures, and data quality alerts. (Zero trading alerts).</p>
      </div>

      <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-3">
        <div className="flex items-center gap-3 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs">
          <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
          <div>
            <div className="font-semibold text-amber-300">Statistical Feature Drift Alert — AAPL</div>
            <div className="text-[11px] text-amber-200/80">Interest rate feature distribution shift detected following Federal Reserve policy meeting (p=0.038).</div>
          </div>
        </div>
      </div>
    </div>
  );
}
