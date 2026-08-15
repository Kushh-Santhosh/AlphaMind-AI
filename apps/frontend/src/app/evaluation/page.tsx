export default function EvaluationPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Continuous Evaluation & Drift Monitoring</h1>
        <p className="text-xs text-slate-400">Model leaderboards, Brier score calibration, walk-forward backtests, and statistical drift alerts.</p>
      </div>

      <div className="bg-[#0d1322] border border-slate-800 rounded-xl overflow-hidden shadow-xl p-5 space-y-4">
        <h3 className="font-semibold text-slate-100 text-sm">Global Predictive Model Leaderboard</h3>
        <table className="w-full text-left text-xs">
          <thead className="bg-[#090d16] text-slate-400 border-b border-slate-800 uppercase text-[10px] tracking-wider font-semibold">
            <tr>
              <th className="p-3">Rank</th>
              <th className="p-3">Model Architecture</th>
              <th className="p-3">Directional Hit Rate</th>
              <th className="p-3">Brier Score</th>
              <th className="p-3">Inference Latency</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            <tr>
              <td className="p-3 font-bold text-amber-400">#1</td>
              <td className="p-3 font-semibold text-slate-100">Bayesian BSTS Model</td>
              <td className="p-3 font-mono text-emerald-400">72.0%</td>
              <td className="p-3 font-mono text-slate-200">0.065</td>
              <td className="p-3 font-mono text-slate-400">45ms</td>
            </tr>
            <tr>
              <td className="p-3 font-bold text-slate-400">#2</td>
              <td className="p-3 font-semibold text-slate-100">Temporal Fusion Transformer (TFT)</td>
              <td className="p-3 font-mono text-emerald-400">71.2%</td>
              <td className="p-3 font-mono text-slate-200">0.068</td>
              <td className="p-3 font-mono text-slate-400">85ms</td>
            </tr>
            <tr>
              <td className="p-3 font-bold text-slate-400">#3</td>
              <td className="p-3 font-semibold text-slate-100">XGBoost Gradient Boosted Trees</td>
              <td className="p-3 font-mono text-emerald-400">69.5%</td>
              <td className="p-3 font-mono text-slate-200">0.072</td>
              <td className="p-3 font-mono text-slate-400">12ms</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
