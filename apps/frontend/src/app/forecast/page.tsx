import { ForecastChart } from "@/components/charts/ForecastChart";
import { MonteCarloChart } from "@/components/charts/MonteCarloChart";

export default function ForecastDashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Probabilistic Forecast Engine</h1>
        <p className="text-xs text-slate-400">Multi-scenario fan charts and 10,000 Monte Carlo stochastic trajectories.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ForecastChart symbol="AAPL" />
        <MonteCarloChart symbol="AAPL" />
      </div>
    </div>
  );
}
