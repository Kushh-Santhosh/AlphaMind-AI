import { ReportViewer } from "@/components/reports/ReportViewer";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Standardized Research Reports Library</h1>
        <p className="text-xs text-slate-400">Audit-ready research artifacts with 100% calculation lineage and evidence citations.</p>
      </div>

      <ReportViewer />
    </div>
  );
}
