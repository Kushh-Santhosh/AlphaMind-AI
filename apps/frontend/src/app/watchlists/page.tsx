import { Plus } from "lucide-react";

export default function WatchlistsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-100">Asset Watchlists & Monitoring</h1>
          <p className="text-xs text-slate-400">Custom asset watchlists for automated research updates and drift alerts.</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 transition-all">
          <Plus className="w-4 h-4" /> Create New Watchlist
        </button>
      </div>

      <div className="p-5 rounded-xl bg-[#0d1322] border border-slate-800 space-y-3">
        <h3 className="font-semibold text-slate-100 text-sm">Core Institutional Watchlist (4 Symbols)</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          {["AAPL", "NVDA", "MSFT", "GOOGL"].map((sym) => (
            <div key={sym} className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs space-y-1">
              <div className="font-bold text-slate-200">{sym}</div>
              <div className="text-[10px] text-slate-400">30D Forecast: +3.4%</div>
              <div className="text-[10px] text-emerald-400 font-medium">Health Score: +0.75</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
