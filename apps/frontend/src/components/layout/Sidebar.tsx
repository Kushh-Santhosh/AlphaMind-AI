"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  BarChart3,
  Bell,
  Brain,
  Building2,
  Compass,
  Cpu,
  Eye,
  FileText,
  GitBranch,
  LineChart,
  PieChart,
  Radar,
  Search,
  ShieldAlert,
  Sliders,
  Sparkles,
  TrendingUp,
  Zap,
} from "lucide-react";

const navItems = [
  { name: "Mission Control 2.0", href: "/mission-control", icon: Brain, badge: "LIVE" },
  { name: "Opportunity Scanner", href: "/scanner", icon: Radar, badge: "NEW" },
  { name: "Company Terminal", href: "/company/NVDA", icon: Building2 },
  { name: "Multi-Asset Compare", href: "/compare", icon: BarChart3 },
  { name: "Institutional Backtest", href: "/backtesting", icon: LineChart, badge: "v4" },
  { name: "Research Engine", href: "/research", icon: Search },
  { name: "Forecast Engine", href: "/forecast", icon: TrendingUp },
  { name: "Portfolio & Funds", href: "/portfolio", icon: PieChart },
  { name: "Risk & Stress Tests", href: "/risk", icon: ShieldAlert },
  { name: "Evaluation & Brier", href: "/evaluation", icon: Cpu },
  { name: "Knowledge Graph", href: "/knowledge-graph", icon: GitBranch },
  { name: "AI Analyst Chat", href: "/chat", icon: Sparkles },
  { name: "Watchlists", href: "/watchlists", icon: Eye },
  { name: "Alerts Center", href: "/alerts", icon: Bell },
  { name: "Settings & Gateways", href: "/settings", icon: Sliders },
  { name: "Beta Admin Panel", href: "/beta-admin", icon: Compass },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#0a0f1d] border-r border-slate-800/80 flex flex-col h-screen sticky top-0 z-40 shrink-0 select-none">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800/80 flex items-center gap-3 bg-[#0c1224]/80 backdrop-blur-md">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/25 ring-1 ring-white/20">
          <Brain className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-1.5">
            <h1 className="font-extrabold text-slate-100 tracking-tight text-base leading-none">
              AlphaMind <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">AI</span>
            </h1>
            <span className="text-[9px] bg-blue-500/20 text-blue-300 font-mono font-bold px-1.5 py-0.2 rounded border border-blue-500/30">
              v4
            </span>
          </div>
          <p className="text-[10px] text-slate-400 mt-1 uppercase tracking-wider font-semibold">
            Investment Research OS
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1 scrollbar-thin scrollbar-thumb-slate-800">
        {navItems.map((item) => {
          const isActive =
            pathname === item.href ||
            (item.href !== "/" && pathname.startsWith(item.href.split("/")[1] ? `/${item.href.split("/")[1]}` : item.href));
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-all group ${
                isActive
                  ? "bg-gradient-to-r from-blue-600/20 to-cyan-500/10 text-cyan-300 border-l-2 border-cyan-400 font-semibold shadow-sm shadow-blue-900/20"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon
                  className={`w-4 h-4 transition-colors ${
                    isActive ? "text-cyan-400" : "text-slate-500 group-hover:text-slate-300"
                  }`}
                />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[9px] font-mono font-bold px-1.5 py-0.2 rounded uppercase ${
                    item.badge === "LIVE"
                      ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 animate-pulse"
                      : "bg-cyan-500/15 text-cyan-300 border border-cyan-500/30"
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer & Disclaimer */}
      <div className="p-3 border-t border-slate-800/80 bg-[#070b14]/90 space-y-2">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-400 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block" />
            <span className="font-semibold text-slate-300">System Ready</span>
          </span>
          <Link href="/settings" className="text-cyan-400 hover:text-cyan-300 transition-colors font-medium text-[11px]">
            Model Gateways →
          </Link>
        </div>
        <div className="p-2 rounded bg-slate-900/80 border border-slate-800/80 text-[10px] text-slate-400 leading-snug">
          <span className="font-semibold text-slate-300 block mb-0.5">SEC / FINRA Disclaimer</span>
          All insights are probabilistic research. No automated live trading advice.
        </div>
      </div>
    </aside>
  );
}
