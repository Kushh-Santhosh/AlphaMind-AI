"use client";

const sampleSymbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"];
const matrixData = [
  [1.0, 0.65, 0.72, 0.58, 0.61],
  [0.65, 1.0, 0.68, 0.62, 0.59],
  [0.72, 0.68, 1.0, 0.54, 0.52],
  [0.58, 0.62, 0.54, 1.0, 0.71],
  [0.61, 0.59, 0.52, 0.71, 1.0],
];

export function CorrelationMatrix() {
  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-slate-100 text-sm">Asset Return Correlation Matrix</h3>
          <p className="text-xs text-slate-400">252-Day Historical Return Cross-Correlation</p>
        </div>
        <span className="text-xs text-slate-400">HHI: 0.1250 (Diversified)</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-center text-xs">
          <thead>
            <tr>
              <th className="p-2 text-left text-slate-500 font-semibold">Asset</th>
              {sampleSymbols.map((sym) => (
                <th key={sym} className="p-2 text-slate-400 font-semibold">{sym}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sampleSymbols.map((sym, rIdx) => (
              <tr key={sym} className="border-t border-slate-800/60">
                <td className="p-2 text-left font-semibold text-slate-300">{sym}</td>
                {matrixData[rIdx].map((val, cIdx) => {
                  const isDiag = rIdx === cIdx;
                  const bgAlpha = isDiag ? 0.8 : val * 0.5;
                  return (
                    <td key={cIdx} className="p-2">
                      <div
                        className="py-1.5 rounded font-mono font-medium text-[11px]"
                        style={{
                          backgroundColor: isDiag
                            ? "rgba(59, 130, 246, 0.3)"
                            : `rgba(59, 130, 246, ${bgAlpha})`,
                          color: isDiag ? "#93c5fd" : "#cbd5e1",
                        }}
                      >
                        {val.toFixed(2)}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
