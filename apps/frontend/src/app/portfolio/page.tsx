import { CorrelationMatrix } from "@/components/charts/CorrelationMatrix";

export default function PortfolioPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Multi-Asset Portfolio Intelligence</h1>
        <p className="text-xs text-slate-400">Position tracking, effective asset count (N_eff = 8.0), asset & sector allocation breakdowns.</p>
      </div>

      <CorrelationMatrix />
    </div>
  );
}
