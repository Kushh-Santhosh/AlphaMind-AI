"use client";

import { useState } from "react";
import { GitBranch, Layers, Filter } from "lucide-react";

interface NodeItem {
  id: string;
  label: string;
  type: string;
  x: number;
  y: number;
}

interface EdgeItem {
  source: string;
  target: string;
  relation: string;
}

const sampleNodes: NodeItem[] = [
  { id: "comp_aapl", label: "Apple Inc.", type: "Company", x: 200, y: 120 },
  { id: "tick_aapl", label: "AAPL", type: "Ticker", x: 80, y: 60 },
  { id: "exec_cook", label: "Tim Cook", type: "Executive", x: 320, y: 60 },
  { id: "ind_tech", label: "Consumer Hardware", type: "Industry", x: 200, y: 220 },
  { id: "comp_tsmc", label: "TSMC", type: "Company", x: 340, y: 200 },
];

const sampleEdges: EdgeItem[] = [
  { source: "comp_aapl", target: "tick_aapl", relation: "REPORTS" },
  { source: "exec_cook", target: "comp_aapl", relation: "BELONGS_TO" },
  { source: "comp_aapl", target: "ind_tech", relation: "BELONGS_TO" },
  { source: "comp_tsmc", target: "comp_aapl", relation: "SUPPLIES" },
];

export function GraphViewer() {
  const [selectedNode, setSelectedNode] = useState<NodeItem | null>(sampleNodes[0]);
  const [filterRelation, setFilterRelation] = useState("ALL");

  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col h-[600px]">
      {/* Header Controls */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
        <div className="flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-blue-400" />
          <h2 className="font-semibold text-slate-100 text-sm">Knowledge Graph Interactive Explorer</h2>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <select
            value={filterRelation}
            onChange={(e) => setFilterRelation(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded px-2.5 py-1 text-slate-300 outline-none"
          >
            <option value="ALL">All Relations (12 Types)</option>
            <option value="SUPPLIES">SUPPLIES</option>
            <option value="COMPETES_WITH">COMPETES_WITH</option>
            <option value="BELONGS_TO">BELONGS_TO</option>
          </select>
        </div>
      </div>

      <div className="flex-1 flex gap-4 overflow-hidden">
        {/* Canvas SVG Graph */}
        <div className="flex-1 bg-[#090d16] rounded-lg border border-slate-900 relative overflow-hidden flex items-center justify-center">
          <svg className="w-full h-full">
            {/* Edges */}
            {sampleEdges.map((e, idx) => {
              const src = sampleNodes.find((n) => n.id === e.source);
              const tgt = sampleNodes.find((n) => n.id === e.target);
              if (!src || !tgt) return null;
              return (
                <g key={idx}>
                  <line
                    x1={src.x}
                    y1={src.y}
                    x2={tgt.x}
                    y2={tgt.y}
                    stroke="#334155"
                    strokeWidth="1.5"
                    strokeDasharray={e.relation === "SUPPLIES" ? "4 4" : "0"}
                  />
                  <text
                    x={(src.x + tgt.x) / 2}
                    y={(src.y + tgt.y) / 2 - 5}
                    fill="#64748b"
                    fontSize="9"
                    textAnchor="middle"
                  >
                    {e.relation}
                  </text>
                </g>
              );
            })}

            {/* Nodes */}
            {sampleNodes.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  onClick={() => setSelectedNode(node)}
                  className="cursor-pointer"
                >
                  <circle
                    r={isSelected ? 22 : 18}
                    fill={isSelected ? "#2563eb" : "#1e293b"}
                    stroke={isSelected ? "#60a5fa" : "#475569"}
                    strokeWidth="2"
                    className="transition-all hover:scale-110"
                  />
                  <text
                    y="4"
                    fill="#f8fafc"
                    fontSize="10"
                    fontWeight="bold"
                    textAnchor="middle"
                  >
                    {node.label.slice(0, 5)}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Node Detail Inspector Panel */}
        <div className="w-64 bg-slate-900/80 border border-slate-800 rounded-lg p-4 text-xs space-y-3 shrink-0">
          <div className="font-semibold text-slate-200 border-b border-slate-800 pb-2 flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-400" />
            <span>Entity Inspector</span>
          </div>
          {selectedNode ? (
            <div className="space-y-2">
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold">Canonical Label</span>
                <p className="font-semibold text-slate-100">{selectedNode.label}</p>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold">Entity Type</span>
                <p className="text-blue-400 font-medium">{selectedNode.type}</p>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold">Connected Edges</span>
                <p className="text-slate-300">3 Relationships</p>
              </div>
              <div className="pt-2 border-t border-slate-800">
                <span className="text-[10px] text-slate-500 uppercase font-bold block mb-1">Source Evidence</span>
                <div className="p-2 rounded bg-slate-950 border border-slate-800 text-[10px] text-slate-400">
                  SEC Form 10-K FY2025 Item 1 Exhibit 21.1
                </div>
              </div>
            </div>
          ) : (
            <p className="text-slate-500">Click a node to inspect entity properties and source citations.</p>
          )}
        </div>
      </div>
    </div>
  );
}
