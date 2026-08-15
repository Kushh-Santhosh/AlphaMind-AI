"use client";

import React, { useState } from "react";
import {
  BrainCircuit,
  ChevronLeft,
  ChevronRight,
  SkipBack,
  Play,
  Search,
  FileText,
  AlertTriangle,
  CheckCircle,
  Lightbulb,
  GitBranch,
  RotateCcw,
} from "lucide-react";

interface ReasoningRecord {
  reasoning_id: string;
  decision_id: string;
  parent_reasoning_id?: string;
  timestamp_utc: string;
  workflow_id: string;
  evidence_references: string[];
  confidence_score: number;
  contradictory_evidence: string[];
  assumptions: string[];
  alternative_actions_considered: Array<{ action: string; rejected: boolean }>;
  selected_action: string;
  replay_snapshot_id: string;
}

interface ReplayFrame {
  step_index: number;
  direction: string;
  total_frames: number;
  replayed_at_utc: string;
  market_context: Record<string, string>;
  research_context: Record<string, string | boolean>;
  forecast_context: Record<string, string | boolean>;
  portfolio_context: Record<string, unknown>;
  ai_reasoning_snapshot?: { reasoning_id: string; selected_action: string } | null;
  confidence_at_step?: number | null;
  current_event: {
    event_id: string;
    event_type: string;
    headline: string;
    details: string;
    source_subsystem: string;
    timestamp_utc: string;
  };
}

const MOCK_RECORDS: ReasoningRecord[] = [
  {
    reasoning_id: "rsn_a4b2c18d91",
    decision_id: "dec_growth_q3_2026",
    timestamp_utc: "2026-08-04T14:30:00Z",
    workflow_id: "wf_sector_rotation_42",
    evidence_references: ["NVDA Q2 2026 10-K Item 7", "FRED PCE Inflation 2026-07", "Polygon NVDA Quote $132.40"],
    confidence_score: 0.88,
    contradictory_evidence: ["Rising 10Y Treasury yields may compress growth multiples", "Bearish RSI divergence on NVDA weekly chart"],
    assumptions: ["AI compute demand sustains ≥ 25% YoY growth through 2027", "Fed holds rates at 4.25% in September meeting"],
    alternative_actions_considered: [
      { action: "Hold existing weights (QQQ 40%, NVDA 25%)", rejected: true },
      { action: "Rotate into defensive TLT (increase to 30%)", rejected: true },
    ],
    selected_action: "Increase NVDA allocation to 40% based on strong semiconductor factor momentum and sustained AI compute demand.",
    replay_snapshot_id: "snap_7f2a9e01",
  },
  {
    reasoning_id: "rsn_b7d4e92f12",
    decision_id: "dec_conservative_hedge",
    timestamp_utc: "2026-08-04T12:15:00Z",
    workflow_id: "wf_macro_hedge_11",
    evidence_references: ["FRED Federal Reserve Rate Decision July 2026", "SEC Treasury Yield Spread Filing"],
    confidence_score: 0.92,
    contradictory_evidence: ["Equity momentum still positive per 12-month factor"],
    assumptions: ["Inflation re-accelerates to 3.2% by Q4 2026"],
    alternative_actions_considered: [{ action: "Maintain current allocation", rejected: true }],
    selected_action: "Increase TLT fixed income weighting to 50% as rate sensitivity hedge.",
    replay_snapshot_id: "snap_3c8b2a14",
  },
];

const MOCK_REPLAY_FRAME: ReplayFrame = {
  step_index: 3,
  direction: "FORWARD",
  total_frames: 12,
  replayed_at_utc: "2026-08-04T14:35:00Z",
  market_context: { quote_symbol: "NVDA", source: "market_feed" },
  research_context: { filing_type: "10-K", source: "sec_edgar" },
  forecast_context: { probability_update: "true", source: "forecast_engine" },
  portfolio_context: {},
  ai_reasoning_snapshot: { reasoning_id: "rsn_a4b2c18d91", selected_action: "Increase NVDA to 40%" },
  confidence_at_step: 0.88,
  current_event: {
    event_id: "evt_c918a2b4f1",
    event_type: "FORECAST_UPDATED",
    headline: "Reasoning Stored: Increase NVDA allocation to 40% based on semiconductor factor",
    details: "Decision dec_growth_q3_2026 | Confidence 88% | Evidence: NVDA Q2 2026 10-K Item 7, FRED PCE Inflation 2026-07",
    source_subsystem: "intelligence_memory",
    timestamp_utc: "2026-08-04T14:30:00Z",
  },
};

const ConfidenceBar = ({ score }: { score: number }) => (
  <div className="space-y-1">
    <div className="flex justify-between text-xs font-mono">
      <span className="text-slate-400">Confidence</span>
      <span className={score >= 0.85 ? "text-emerald-400" : score >= 0.70 ? "text-amber-400" : "text-rose-400"}>
        {(score * 100).toFixed(0)}%
      </span>
    </div>
    <div className="w-full bg-slate-800 rounded-full h-2">
      <div
        className={`h-2 rounded-full transition-all ${score >= 0.85 ? "bg-emerald-500" : score >= 0.70 ? "bg-amber-500" : "bg-rose-500"}`}
        style={{ width: `${score * 100}%` }}
      />
    </div>
  </div>
);

export default function ReasoningMemoryPage() {
  const [selectedRecord, setSelectedRecord] = useState<ReasoningRecord>(MOCK_RECORDS[0]);
  const [replayFrame] = useState<ReplayFrame>(MOCK_REPLAY_FRAME);
  const [replayStep, setReplayStep] = useState(3);

  const handleForward = () => setReplayStep((s) => Math.min(s + 1, replayFrame.total_frames));
  const handleBackward = () => setReplayStep((s) => Math.max(s - 1, 1));
  const handleReset = () => setReplayStep(1);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-violet-500/10 text-violet-400 border border-violet-500/20">
              AlphaMind v2.0 — Milestone 19
            </span>
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
              Intelligence Reasoning Memory
            </span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <BrainCircuit className="w-8 h-8 text-violet-400" />
            Intelligence Reasoning Memory & Decision Inspector
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Every AI decision is fully traceable — evidence, alternatives, assumptions, contradictions, and confidence.
          </p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

          {/* Reasoning Memory Explorer — Left Panel */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Search className="w-4 h-4 text-slate-400" />
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Reasoning Memory Explorer</h2>
            </div>
            <div className="space-y-3">
              {MOCK_RECORDS.map((rec) => (
                <button
                  key={rec.reasoning_id}
                  onClick={() => setSelectedRecord(rec)}
                  className={`w-full text-left rounded-xl p-4 border transition-all ${
                    selectedRecord.reasoning_id === rec.reasoning_id
                      ? "bg-slate-900 border-violet-500 ring-1 ring-violet-500"
                      : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="text-xs font-mono text-violet-300">{rec.reasoning_id}</span>
                    <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${rec.confidence_score >= 0.85 ? "bg-emerald-500/10 text-emerald-400" : "bg-amber-500/10 text-amber-400"}`}>
                      {(rec.confidence_score * 100).toFixed(0)}% conf
                    </span>
                  </div>
                  <p className="text-sm text-slate-200 line-clamp-2">{rec.selected_action}</p>
                  <p className="text-xs text-slate-500 mt-1">{rec.timestamp_utc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Decision Inspector — Center Panel */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <FileText className="w-4 h-4 text-violet-400" />
                <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Decision Inspector</h2>
              </div>
              <p className="text-xs font-mono text-slate-500">{selectedRecord.reasoning_id}</p>
            </div>

            <ConfidenceBar score={selectedRecord.confidence_score} />

            {/* Selected Action */}
            <div className="rounded-lg bg-violet-500/10 border border-violet-500/20 p-3">
              <div className="text-xs text-violet-300 font-semibold mb-1 flex items-center gap-1.5">
                <Play className="w-3.5 h-3.5" /> Selected Action
              </div>
              <p className="text-sm text-slate-200">{selectedRecord.selected_action}</p>
            </div>

            {/* Evidence References */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> Evidence Citations
              </div>
              <ul className="space-y-1">
                {selectedRecord.evidence_references.map((e, i) => (
                  <li key={i} className="text-xs text-emerald-300 font-mono bg-emerald-500/5 border border-emerald-500/10 rounded px-2 py-1">
                    {e}
                  </li>
                ))}
              </ul>
            </div>

            {/* Contradictory Evidence */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-rose-400" /> Contradictory Evidence
              </div>
              <ul className="space-y-1">
                {selectedRecord.contradictory_evidence.map((c, i) => (
                  <li key={i} className="text-xs text-rose-300 bg-rose-500/5 border border-rose-500/10 rounded px-2 py-1">
                    {c}
                  </li>
                ))}
              </ul>
            </div>

            {/* Assumptions */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
                <Lightbulb className="w-3.5 h-3.5 text-amber-400" /> Assumptions
              </div>
              <ul className="space-y-1">
                {selectedRecord.assumptions.map((a, i) => (
                  <li key={i} className="text-xs text-amber-300 bg-amber-500/5 border border-amber-500/10 rounded px-2 py-1">
                    {a}
                  </li>
                ))}
              </ul>
            </div>

            {/* Alternatives Considered */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
                <GitBranch className="w-3.5 h-3.5 text-blue-400" /> Alternatives Considered & Rejected
              </div>
              <ul className="space-y-1">
                {selectedRecord.alternative_actions_considered.map((alt, i) => (
                  <li key={i} className="text-xs text-slate-400 line-through bg-slate-800/60 border border-slate-700 rounded px-2 py-1">
                    {alt.action}
                  </li>
                ))}
              </ul>
            </div>

            <div className="text-xs font-mono text-slate-600 border-t border-slate-800 pt-3">
              Replay Snapshot ID: {selectedRecord.replay_snapshot_id}
            </div>
          </div>

          {/* Chess Replay Viewer — Right Panel */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
            <div className="flex items-center gap-2">
              <RotateCcw className="w-4 h-4 text-teal-400" />
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Chess-Style Replay Viewer</h2>
            </div>

            {/* Playback Controls */}
            <div className="flex items-center justify-between gap-2">
              <button onClick={handleReset} className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition">
                <SkipBack className="w-4 h-4" />
              </button>
              <button onClick={handleBackward} className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <div className="flex-1 text-center">
                <span className="text-sm font-mono text-slate-200">
                  Frame {replayStep} / {replayFrame.total_frames}
                </span>
              </div>
              <button onClick={handleForward} className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            {/* Progress bar */}
            <div className="w-full bg-slate-800 rounded-full h-1.5">
              <div
                className="bg-teal-500 h-1.5 rounded-full transition-all"
                style={{ width: `${(replayStep / replayFrame.total_frames) * 100}%` }}
              />
            </div>

            {/* Active Frame Details */}
            <div className="space-y-3">
              <div className="rounded-lg bg-teal-500/5 border border-teal-500/20 p-3">
                <div className="text-xs font-semibold text-teal-400 mb-1">Current Event</div>
                <p className="text-sm text-slate-200 line-clamp-2">{replayFrame.current_event.headline}</p>
                <p className="text-xs text-slate-500 mt-1">{replayFrame.current_event.timestamp_utc}</p>
              </div>

              {replayFrame.ai_reasoning_snapshot && (
                <div className="rounded-lg bg-violet-500/5 border border-violet-500/20 p-3">
                  <div className="text-xs font-semibold text-violet-400 mb-1">AI Reasoning at This Step</div>
                  <p className="text-sm text-slate-300">{replayFrame.ai_reasoning_snapshot.selected_action}</p>
                  {replayFrame.confidence_at_step && (
                    <ConfidenceBar score={replayFrame.confidence_at_step} />
                  )}
                </div>
              )}

              {Object.keys(replayFrame.market_context).length > 0 && (
                <div className="rounded-lg bg-slate-800/60 border border-slate-700 p-3">
                  <div className="text-xs font-semibold text-slate-400 mb-1">Market Context</div>
                  {Object.entries(replayFrame.market_context).map(([k, v]) => (
                    <div key={k} className="flex justify-between text-xs py-0.5">
                      <span className="text-slate-400">{k}</span>
                      <span className="font-mono text-slate-200">{String(v)}</span>
                    </div>
                  ))}
                </div>
              )}

              {Object.keys(replayFrame.research_context).length > 0 && (
                <div className="rounded-lg bg-slate-800/60 border border-slate-700 p-3">
                  <div className="text-xs font-semibold text-slate-400 mb-1">Research Context</div>
                  {Object.entries(replayFrame.research_context).map(([k, v]) => (
                    <div key={k} className="flex justify-between text-xs py-0.5">
                      <span className="text-slate-400">{k}</span>
                      <span className="font-mono text-slate-200">{String(v)}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
