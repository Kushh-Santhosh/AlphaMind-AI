import Link from "next/link";
import { Search, ArrowRight } from "lucide-react";

const sampleResearchList = [
  { symbol: "AAPL", name: "Apple Inc.", sector: "Technology", mcap: "$2.85T", healthTrend: "+0.75", confidence: "94%" },
  { symbol: "NVDA", name: "NVIDIA Corporation", sector: "Technology", mcap: "$3.10T", healthTrend: "+0.88", confidence: "96%" },
  { symbol: "MSFT", name: "Microsoft Corporation", sector: "Technology", mcap: "$3.05T", healthTrend: "+0.82", confidence: "95%" },
  { symbol: "GOOGL", name: "Alphabet Inc.", sector: "Communication", mcap: "$2.15T", healthTrend: "+0.70", confidence: "92%" },
];

export default function ResearchDashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-100">Financial Research Intelligence Engine</h1>
          <p className="text-xs text-slate-400">Normalized SEC EDGAR filings, news articles, macro series, and corporate events.</p>
        </div>
      </div>

      {/* Search Input */}
      <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 flex items-center gap-3">
        <Search className="w-4 h-4 text-slate-400" />
        <input
          type="text"
          placeholder="Enter asset ticker symbol (e.g. AAPL, NVDA, MSFT)..."
          className="flex-1 bg-transparent text-xs text-slate-100 outline-none placeholder:text-slate-500"
        />
        <button className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-all">
          Trigger Deep Research
        </button>
      </div>

      {/* Asset Table */}
      <div className="bg-[#0d1322] border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#090d16] text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-semibold">
            <tr>
              <th className="p-3.5">Asset</th>
              <th className="p-3.5">Sector</th>
              <th className="p-3.5">Market Cap</th>
              <th className="p-3.5">Health Trend</th>
              <th className="p-3.5">Data Confidence</th>
              <th className="p-3.5 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {sampleResearchList.map((item) => (
              <tr key={item.symbol} className="hover:bg-slate-900/50 transition-colors">
                <td className="p-3.5">
                  <div className="flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-slate-200 text-[11px]">
                      {item.symbol.slice(0, 2)}
                    </div>
                    <div>
                      <div className="font-semibold text-slate-200">{item.symbol}</div>
                      <div className="text-[10px] text-slate-400">{item.name}</div>
                    </div>
                  </div>
                </td>
                <td className="p-3.5 text-slate-300">{item.sector}</td>
                <td className="p-3.5 font-mono text-slate-300">{item.mcap}</td>
                <td className="p-3.5">
                  <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded font-mono text-[11px]">
                    {item.healthTrend}
                  </span>
                </td>
                <td className="p-3.5 text-slate-300">{item.confidence}</td>
                <td className="p-3.5 text-right">
                  <Link
                    href={`/company/${item.symbol}`}
                    className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 font-semibold text-xs"
                  >
                    <span>Inspect</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
