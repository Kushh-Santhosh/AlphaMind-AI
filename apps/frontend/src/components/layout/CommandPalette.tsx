"use client";

import { useEffect, useState } from "react";
import { Search, X } from "lucide-react";
import { useRouter } from "next/navigation";

export function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  if (!isOpen) return null;

  const handleSelect = (path: string) => {
    setIsOpen(false);
    router.push(path);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-start justify-center pt-20 p-4">
      <div className="bg-[#0f172a] border border-slate-700/80 rounded-xl w-full max-w-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-150">
        <div className="p-3 border-b border-slate-800 flex items-center gap-3">
          <Search className="w-4 h-4 text-slate-400 shrink-0" />
          <input
            type="text"
            placeholder="Type a symbol, company, or command (e.g. AAPL, Forecast, Risk)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full bg-transparent text-sm text-slate-100 outline-none placeholder:text-slate-500"
          />
          <button onClick={() => setIsOpen(false)} className="text-slate-500 hover:text-slate-300">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-2 max-h-72 overflow-y-auto space-y-1 text-xs">
          <div className="px-2 py-1 text-[10px] uppercase font-bold text-slate-500 tracking-wider">Quick Navigation</div>
          <button onClick={() => handleSelect('/company/AAPL')} className="w-full text-left px-3 py-2 rounded hover:bg-slate-800/80 text-slate-200 flex justify-between">
            <span>Analyze Company — AAPL</span>
            <span className="text-slate-500">Company Workspace</span>
          </button>
          <button onClick={() => handleSelect('/forecast')} className="w-full text-left px-3 py-2 rounded hover:bg-slate-800/80 text-slate-200 flex justify-between">
            <span>Probabilistic Forecast Engine</span>
            <span className="text-slate-500">Prediction</span>
          </button>
          <button onClick={() => handleSelect('/portfolio')} className="w-full text-left px-3 py-2 rounded hover:bg-slate-800/80 text-slate-200 flex justify-between">
            <span>Portfolio Risk & Exposure Analytics</span>
            <span className="text-slate-500">Portfolio</span>
          </button>
          <button onClick={() => handleSelect('/knowledge-graph')} className="w-full text-left px-3 py-2 rounded hover:bg-slate-800/80 text-slate-200 flex justify-between">
            <span>Knowledge Graph Viewer</span>
            <span className="text-slate-500">Graph</span>
          </button>
        </div>
      </div>
    </div>
  );
}
