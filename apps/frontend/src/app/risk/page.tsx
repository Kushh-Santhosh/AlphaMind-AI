export default function RiskPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Quantitative Risk & Macro Stress Testing Engine</h1>
        <p className="text-xs text-slate-400">Euler Marginal Contribution to Risk (MCR), VaR 95/99, Expected Shortfall CVaR, and 2008 / Rate Shock scenarios.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400">Parametric VaR (95% Daily)</span>
          <p className="text-xl font-bold text-rose-400">-1.85%</p>
        </div>
        <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400">Expected Shortfall CVaR (95%)</span>
          <p className="text-xl font-bold text-rose-500">-2.65%</p>
        </div>
        <div className="p-4 rounded-xl bg-[#0d1322] border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400">Sharpe Ratio (Annualized)</span>
          <p className="text-xl font-bold text-emerald-400">1.62</p>
        </div>
      </div>
    </div>
  );
}
