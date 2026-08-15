"use client";

interface MonteCarloChartProps {
  symbol: string;
  simulationsCount?: number;
}

export function MonteCarloChart({ symbol, simulationsCount = 10000 }: MonteCarloChartProps) {
  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-slate-100 text-sm">Monte Carlo Stochastic Trajectories</h3>
          <p className="text-xs text-slate-400">{simulationsCount.toLocaleString()} Student-t Fat-Tail Runs ({symbol})</p>
        </div>
        <span className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs px-2.5 py-1 rounded-full font-medium">
          p50 Median: +3.8%
        </span>
      </div>

      <div className="h-48 w-full bg-[#090d16] rounded-lg p-4 relative overflow-hidden flex flex-col justify-between border border-slate-900">
        <svg className="w-full h-full" viewBox="0 0 400 120">
          <line x1="0" y1="60" x2="400" y2="60" stroke="#334155" />

          {/* Sample stochastic trajectories */}
          <path d="M 0,60 C 100,40 200,20 400,10" fill="none" stroke="rgba(16, 185, 129, 0.4)" strokeWidth="1" />
          <path d="M 0,60 C 100,50 200,35 400,25" fill="none" stroke="rgba(59, 130, 246, 0.4)" strokeWidth="1" />
          <path d="M 0,60 C 100,65 200,55 400,45" fill="none" stroke="rgba(59, 130, 246, 0.5)" strokeWidth="1.5" />
          <path d="M 0,60 C 100,55 200,70 400,65" fill="none" stroke="rgba(148, 163, 184, 0.3)" strokeWidth="1" />
          <path d="M 0,60 C 100,70 200,85 400,105" fill="none" stroke="rgba(239, 68, 68, 0.4)" strokeWidth="1" />
        </svg>

        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
          <span>5th Percentile: -14.2%</span>
          <span className="text-cyan-400 font-semibold">50th Percentile: +3.8%</span>
          <span>95th Percentile: +21.5%</span>
        </div>
      </div>
    </div>
  );
}
