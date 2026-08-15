import { GraphViewer } from "@/components/graph/GraphViewer";

export default function KnowledgeGraphPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Financial Knowledge Intelligence Graph</h1>
        <p className="text-xs text-slate-400">Interactive graph visualization of corporate entities, executive boards, subsidiaries, and supply chain triples.</p>
      </div>

      <GraphViewer />
    </div>
  );
}
