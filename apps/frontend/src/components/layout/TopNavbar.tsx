"use client";

import { Bell, Search, ShieldCheck, User } from "lucide-react";
import Link from "next/link";

export function TopNavbar() {
  return (
    <header className="h-14 bg-[#0d1322]/90 backdrop-blur border-b border-slate-800/80 px-6 flex items-center justify-between sticky top-0 z-30 shrink-0">
      {/* Search Trigger */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => {
            const event = new KeyboardEvent("keydown", {
              key: "k",
              metaKey: true,
              bubbles: true,
            });
            window.dispatchEvent(event);
          }}
          className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 hover:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-400 w-64 transition-all"
        >
          <Search className="w-3.5 h-3.5 text-slate-500" />
          <span>Quick Search / Command...</span>
          <kbd className="ml-auto bg-slate-800 px-1.5 py-0.5 rounded text-[10px] text-slate-400 font-mono">
            ⌘K
          </kbd>
        </button>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4 text-xs">
        {/* Compliance Badge */}
        <div className="flex items-center gap-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full text-[11px] font-medium">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Probabilistic Gate Verified</span>
        </div>

        {/* Notifications */}
        <Link
          href="/alerts"
          className="relative text-slate-400 hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-800/60"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-blue-500 ring-2 ring-[#0d1322]" />
        </Link>

        {/* User Avatar */}
        <div className="flex items-center gap-2 border-l border-slate-800/80 pl-4">
          <div className="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300">
            <User className="w-4 h-4" />
          </div>
          <span className="font-medium text-slate-200 text-xs">Quant Analyst</span>
        </div>
      </div>
    </header>
  );
}
