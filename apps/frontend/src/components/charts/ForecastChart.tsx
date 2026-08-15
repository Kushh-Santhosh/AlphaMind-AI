"use client";

interface ForecastChartProps {
  symbol: string;
  meanEstimatePct?: number;
  lowerBoundPct?: number;
  upperBoundPct?: number;
}

export function ForecastChart({
  symbol,
  meanEstimatePct = 3.4,
  lowerBoundPct = -12.0,
  upperBoundPct = 18.0,
}: ForecastChartProps) {
  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-slate-100 text-sm">30-Day Probabilistic Return Distribution</h3>
          <p className="text-xs text-slate-400">95% Confidence Interval Bounds ({symbol})</p>
        </div>
        <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs px-2.5 py-1 rounded-full font-medium">
          Mean: +{meanEstimatePct}%
        </span>
      </div>

      {/* SVG Interactive Scenario Fan Chart */}
      <div className="h-48 w-full bg-[#090d16] rounded-lg p-4 relative overflow-hidden flex flex-col justify-between border border-slate-900">
        <svg className="w-full h-full overflow-visible" viewBox="0 0 400 120">
          {/* Grid lines */}
          <line x1="0" y1="20" x2="400" y2="20" stroke="#1e293b" strokeDasharray="3 3" />
          <line x1="0" y1="60" x2="400" y2="60" stroke="#334155" />
          <line x1="0" y1="100" x2="400" y2="100" stroke="#1e293b" strokeDasharray="3 3" />

          {/* 95% Confidence Fan Area */}
          <polygon
            points="0,60 100,55 200,45 300,30 400,15 400,105 300,90 200,75 100,65 0,60"
            fill="rgba(59, 130, 246, 0.15)"
            stroke="rgba(59, 130, 246, 0.3)"
            strokeWidth="1"
          />

          {/* Bull Scenario Line */}
          <path d="M 0,60 Q 200,30 400,15" fill="none" stroke="#10b981" strokeWidth="2" strokeDasharray="4 4" />

          {/* Mean Path Line */}
          <path d="M 0,60 Q 200,50 400,42" fill="none" stroke="#3b82f6" strokeWidth="2.5" />

          {/* Bear Scenario Line */}
          <path d="M 0,60 Q 200,75 400,95" fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="4 4" />
        </svg>

        {/* Legend */}
        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
            <span>Bull ({upperBoundPct}%)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block" />
            <span>Mean Base (+{meanEstimatePct}%)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block" />
            <span>Bear ({lowerBoundPct}%)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
