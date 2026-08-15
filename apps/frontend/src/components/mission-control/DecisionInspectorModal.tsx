"use client";

import React, { useCallback, useEffect } from "react";
import {
  X,
  Brain,
  FileText,
  TrendingUp,
  AlertTriangle,
  BarChart3,
  ExternalLink,
  Play,
  CheckCircle,
  XCircle,
  Target,
  Zap,
} from "lucide-react";
import { useReasoningRecord } from "@/hooks/useMissionControl";
import type { ShapFactor } from "@/lib/missionControlTypes";

interface DecisionInspectorModalProps {
  reasoningId: string | null;
  onClose: () => void;
}

function ShapBar({ factor }: { factor: ShapFactor }) {
  const pct = Math.round(factor.importance * 100);
  const isPositive = factor.direction === "positive";
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-300 font-medium">{factor.factor}</span>
        <span className={`font-bold ${isPositive ? "text-emerald-400" : "text-rose-400"}`}>
          {isPositive ? "+" : "−"}
          {pct}%
        </span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${isPositive ? "bg-emerald-500" : "bg-rose-500"}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export function DecisionInspectorModal({ reasoningId, onClose }: DecisionInspectorModalProps) {
  const { data: record, loading, error } = useReasoningRecord(reasoningId);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    },
    [onClose],
  );

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  if (!reasoningId) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="Decision Inspector"
    >
      <div
        className="relative w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-[#0d1322] border border-slate-700/70 rounded-2xl shadow-2xl shadow-black/60"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between p-5 border-b border-slate-800 bg-[#0d1322] rounded-t-2xl">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-violet-500/10 border border-violet-500/30 flex items-center justify-center">
              <Brain className="w-4 h-4 text-violet-400" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-100">Decision Inspector</h2>
              <p className="text-[10px] text-slate-500 font-mono">{reasoningId?.slice(0, 24)}…</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
            aria-label="Close Decision Inspector"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-6">
          {loading && (
            <div className="flex items-center justify-center py-16 text-slate-400">
              <div className="animate-spin w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full mr-3" />
              Loading decision record…
            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm">
              Failed to load: {error}
            </div>
          )}

          {record && (
            <>
              {/* Decision summary */}
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1 flex-1">
                    <div className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-violet-400" />
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                        Selected Action
                      </span>
                    </div>
                    <p className="text-sm font-bold text-slate-100">{record.selected_action}</p>
                    <p className="text-[10px] text-slate-500">
                      {new Date(record.timestamp_utc).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-2xl font-bold text-violet-400">
                      {Math.round(record.confidence_score * 100)}%
                    </div>
                    <div className="text-[10px] text-slate-500">Confidence</div>
                  </div>
                </div>
              </div>

              {/* Probability Distribution */}
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-3.5 h-3.5 text-blue-400" />
                  <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                    Probability Distribution
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { label: "Bull", value: record.probability_distribution.bull_pct, bg: "bg-emerald-500/5", border: "border-emerald-500/20", text: "text-emerald-400" },
                    { label: "Base", value: record.probability_distribution.base_pct, bg: "bg-blue-500/5", border: "border-blue-500/20", text: "text-blue-400" },
                    { label: "Bear", value: record.probability_distribution.bear_pct, bg: "bg-rose-500/5", border: "border-rose-500/20", text: "text-rose-400" },
                  ].map(({ label, value, bg, border, text }) => (
                    <div
                      key={label}
                      className={`p-3 rounded-xl ${bg} border ${border} text-center`}
                    >
                      <div className={`text-xl font-bold ${text}`}>{value}%</div>
                      <div className="text-[10px] text-slate-500 mt-0.5">{label} Scenario</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* SHAP Feature Importance */}
              {record.shap_factors && record.shap_factors.length > 0 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Zap className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                      SHAP Feature Importance
                    </span>
                  </div>
                  <div className="space-y-2.5">
                    {record.shap_factors.map((f) => (
                      <ShapBar key={f.factor} factor={f} />
                    ))}
                  </div>
                </div>
              )}

              {/* Evidence + Contradictions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                      Supporting Evidence
                    </span>
                  </div>
                  <ul className="space-y-1.5">
                    {(record.evidence_references.length > 0
                      ? record.evidence_references
                      : ["No explicit evidence references stored"]
                    ).map((ev, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-[11px] text-slate-300 p-2 rounded-lg bg-emerald-500/5 border border-emerald-500/10"
                      >
                        <CheckCircle className="w-3 h-3 text-emerald-500 mt-0.5 shrink-0" />
                        {ev}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-3.5 h-3.5 text-rose-400" />
                    <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                      Contradicting Evidence
                    </span>
                  </div>
                  <ul className="space-y-1.5">
                    {record.contradicting_evidence.map((ev, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-[11px] text-slate-300 p-2 rounded-lg bg-rose-500/5 border border-rose-500/10"
                      >
                        <AlertTriangle className="w-3 h-3 text-rose-500 mt-0.5 shrink-0" />
                        {ev}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Alternatives */}
              {record.alternative_actions_considered.length > 0 && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-3.5 h-3.5 text-cyan-400" />
                    <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                      Alternatives Considered
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {record.alternative_actions_considered.map((alt, i) => (
                      <span
                        key={i}
                        className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-[11px] text-slate-400 font-medium"
                      >
                        {typeof alt === "object" && alt !== null ? String((alt as Record<string, unknown>).action || JSON.stringify(alt)) : String(alt)}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Citations */}
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <FileText className="w-3.5 h-3.5 text-slate-400" />
                  <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                    Citations
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { label: "SEC Filings", items: record.citations.sec_filings },
                    { label: "Macro Sources", items: record.citations.macro_sources },
                    { label: "News", items: record.citations.news_sources },
                  ].map(({ label, items }) => (
                    <div key={label} className="p-3 rounded-xl bg-slate-900/40 border border-slate-800">
                      <div className="text-[10px] text-slate-500 font-semibold mb-1.5">{label}</div>
                      {items.map((item, i) => (
                        <div key={i} className="text-[10px] text-slate-400 py-0.5">
                          {item}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex items-center gap-3 pt-2 border-t border-slate-800">
                {record.replay_snapshot_id && (
                  <a
                    href={`/reasoning-memory?replay=${record.replay_snapshot_id}`}
                    className="flex items-center gap-2 px-3 py-2 rounded-lg bg-violet-600/10 border border-violet-500/30 text-violet-400 hover:bg-violet-600/20 transition-colors text-xs font-medium"
                  >
                    <Play className="w-3 h-3" /> Replay This Decision
                  </a>
                )}
                <a
                  href={`/timeline?reasoning_id=${record.reasoning_id}`}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 hover:text-slate-200 transition-colors text-xs font-medium"
                >
                  <ExternalLink className="w-3 h-3" /> View in Timeline
                </a>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
