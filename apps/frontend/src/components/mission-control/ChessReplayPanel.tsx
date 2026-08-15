"use client";

import React, { memo } from "react";
import {
  SkipBack,
  Play,
  Pause,
  SkipForward,
  ChevronLeft,
  ChevronRight,
  Clock,
  TrendingUp,
  BarChart3,
  RefreshCw,
} from "lucide-react";
import { useReplayControls, useReplayStatus } from "@/hooks/useMissionControl";

interface ReplayFrameData {
  event_id?: string;
  event_type?: string;
  headline?: string;
  timestamp_utc?: string;
  portfolio_snapshot?: Record<string, unknown>;
  market_snapshot?: Record<string, unknown>;
}

function FramePanel({ frame }: { frame: ReplayFrameData | null }) {
  if (!frame) {
    return (
      <div className="flex items-center justify-center h-32 rounded-xl border border-dashed border-slate-700 text-slate-500 text-sm">
        Step through the timeline to inspect frames
      </div>
    );
  }
  return (
    <div className="space-y-3">
      {/* Event context */}
      {frame.headline && (
        <div className="p-3 rounded-xl bg-blue-500/5 border border-blue-500/20">
          <div className="text-[10px] text-blue-400 font-semibold uppercase tracking-wider mb-1">
            Timeline Event
          </div>
          <p className="text-xs text-slate-300">{frame.headline}</p>
          {frame.timestamp_utc && (
            <p className="text-[10px] text-slate-500 mt-1">
              {new Date(frame.timestamp_utc).toLocaleString()}
            </p>
          )}
        </div>
      )}

      {/* Portfolio snapshot */}
      {frame.portfolio_snapshot && (
        <div className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
          <div className="flex items-center gap-2 mb-2">
            <BarChart3 className="w-3 h-3 text-emerald-400" />
            <span className="text-[10px] text-emerald-400 font-semibold uppercase tracking-wider">
              Portfolio Snapshot
            </span>
          </div>
          <pre className="text-[10px] text-slate-400 overflow-x-auto whitespace-pre-wrap max-h-24">
            {JSON.stringify(frame.portfolio_snapshot, null, 2)}
          </pre>
        </div>
      )}

      {/* Market snapshot */}
      {frame.market_snapshot && (
        <div className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-3 h-3 text-amber-400" />
            <span className="text-[10px] text-amber-400 font-semibold uppercase tracking-wider">
              Market Snapshot
            </span>
          </div>
          <pre className="text-[10px] text-slate-400 overflow-x-auto whitespace-pre-wrap max-h-24">
            {JSON.stringify(frame.market_snapshot, null, 2)}
          </pre>
        </div>
      )}

      {!frame.headline && !frame.portfolio_snapshot && !frame.market_snapshot && (
        <div className="p-3 rounded-xl bg-slate-900/40 border border-slate-800">
          <pre className="text-[10px] text-slate-400 overflow-x-auto whitespace-pre-wrap max-h-32">
            {JSON.stringify(frame, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export const ChessReplayPanel = memo(function ChessReplayPanel() {
  const { data: status } = useReplayStatus();
  const { position, isPlaying, frame, step, jump, play, pause } = useReplayControls();

  const totalFrames = status?.total_frames ?? 0;
  const progress = totalFrames > 0 ? Math.min((position / Math.max(totalFrames - 1, 1)) * 100, 100) : 0;

  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-2xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-violet-500/10 border border-violet-500/30 flex items-center justify-center">
            <RefreshCw className="w-3.5 h-3.5 text-violet-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100">Chess Replay</h3>
            <p className="text-[10px] text-slate-500">
              Session: {status?.session_id?.slice(0, 16) ?? "…"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          <Clock className="w-3 h-3 text-slate-500" />
          <span className="text-[10px] text-slate-400 font-mono">
            {position} / {totalFrames} frames
          </span>
        </div>
      </div>

      {/* Frame display */}
      <div className="p-4">
        <FramePanel frame={frame as ReplayFrameData | null} />
      </div>

      {/* Timeline slider */}
      <div className="px-4 pb-2">
        <div className="relative h-1.5 bg-slate-800 rounded-full cursor-pointer">
          <div
            className="absolute h-full bg-violet-500 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
          <input
            type="range"
            min={0}
            max={Math.max(totalFrames - 1, 0)}
            value={position}
            onChange={(e) => void jump(Number(e.target.value))}
            className="absolute inset-0 w-full opacity-0 cursor-pointer h-full"
            aria-label="Replay timeline position"
          />
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-3 p-4 border-t border-slate-800">
        <button
          onClick={() => void jump(0)}
          className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
          aria-label="Jump to start"
        >
          <SkipBack className="w-4 h-4" />
        </button>

        <button
          onClick={() => void step("backward")}
          className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
          aria-label="Previous frame"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <button
          onClick={isPlaying ? pause : play}
          className={`p-2.5 rounded-xl transition-all ${
            isPlaying
              ? "bg-violet-600/20 border border-violet-500/40 text-violet-400 hover:bg-violet-600/30"
              : "bg-violet-600 text-white hover:bg-violet-500 shadow-lg shadow-violet-500/25"
          }`}
          aria-label={isPlaying ? "Pause replay" : "Play replay"}
        >
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </button>

        <button
          onClick={() => void step("forward")}
          className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
          aria-label="Next frame"
        >
          <ChevronRight className="w-4 h-4" />
        </button>

        <button
          onClick={() => void jump(Math.max(totalFrames - 1, 0))}
          className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
          aria-label="Jump to end"
        >
          <SkipForward className="w-4 h-4" />
        </button>
      </div>

      {/* Jump to step input */}
      <div className="px-4 pb-4">
        <div className="flex items-center gap-2">
          <label className="text-[10px] text-slate-500 shrink-0">Jump to step:</label>
          <input
            type="number"
            min={0}
            max={Math.max(totalFrames - 1, 0)}
            defaultValue={0}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                void jump(Number((e.target as HTMLInputElement).value));
              }
            }}
            className="w-20 px-2 py-1 rounded-lg bg-slate-900 border border-slate-700 text-xs text-slate-300 focus:outline-none focus:border-violet-500"
            aria-label="Jump to specific step number"
          />
          <span className="text-[10px] text-slate-600">(press Enter)</span>
        </div>
      </div>
    </div>
  );
});
