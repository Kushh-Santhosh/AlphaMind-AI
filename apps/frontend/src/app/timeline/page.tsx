import { Activity, Clock } from "lucide-react";

const sampleTimelineEvents = [
  { timestamp: "2026-08-04 19:00 UTC", type: "WORKFLOW_COMPLETED", title: "Analyze Company Workflow Completed — AAPL", details: "Extracted 12 GAAP financial factors and generated 5-tier return distribution." },
  { timestamp: "2026-08-04 18:45 UTC", type: "FORECAST_GENERATED", title: "Probabilistic Forecast Compiled — NVDA", details: "Ensemble Bayesian BSTS model forecast calculated with Brier score 0.065." },
  { timestamp: "2026-08-04 18:30 UTC", type: "DRIFT_ALERT", title: "Feature Drift Detected — tft_v1", details: "Interest rate feature distribution shift detected (p=0.038)." },
];

export default function TimelinePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Platform Activity Execution Timeline</h1>
        <p className="text-xs text-slate-400">Structured audit log of workflow executions, model forecasts, and background alerts.</p>
      </div>

      <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-5 shadow-xl space-y-4">
        {sampleTimelineEvents.map((evt, idx) => (
          <div key={idx} className="flex gap-4 items-start pb-4 border-b border-slate-800/60 last:border-0 last:pb-0">
            <div className="w-8 h-8 rounded-lg bg-blue-600/15 border border-blue-500/30 text-blue-400 flex items-center justify-center shrink-0 mt-1">
              <Activity className="w-4 h-4" />
            </div>
            <div className="space-y-1 text-xs">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-100">{evt.title}</span>
                <span className="bg-slate-800 text-slate-400 text-[10px] px-2 py-0.5 rounded font-mono">{evt.type}</span>
              </div>
              <p className="text-slate-400">{evt.details}</p>
              <span className="text-[10px] text-slate-500 flex items-center gap-1">
                <Clock className="w-3 h-3" /> {evt.timestamp}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
