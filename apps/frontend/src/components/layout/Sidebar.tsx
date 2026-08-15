"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  Award,
  BarChart3,
  Bell,
  Bot,
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

interface NavGroup {
  title: string;
  items: {
    name: string;
    href: string;
    icon: any;
    badge?: string;
  }[];
}

const navGroups: NavGroup[] = [
  {
    title: "RESEARCH",
    items: [
      { name: "Opportunity Scanner", href: "/scanner", icon: Radar, badge: "AI" },
      { name: "Company Terminal", href: "/company/NVDA", icon: Building2 },
      { name: "Multi-Asset Compare", href: "/compare", icon: BarChart3 },
      { name: "Research Engine", href: "/research", icon: Search },
    ],
  },
  {
    title: "INTELLIGENCE",
    items: [
      { name: "Mission Control 2.0", href: "/mission-control", icon: Brain, badge: "LIVE" },
      { name: "Forecasts (Kronos)", href: "/forecast", icon: TrendingUp },
      { name: "Knowledge Graph", href: "/knowledge-graph", icon: GitBranch },
      { name: "AI Analyst Chat", href: "/chat", icon: Sparkles },
    ],
  },
  {
    title: "TRADING & QUANT",
    items: [
      { name: "Paper Trading Terminal", href: "/paper-trading", icon: Bot, badge: "PAPER" },
      { name: "Portfolio & Funds", href: "/portfolio", icon: PieChart },
      { name: "Backtest Workbench", href: "/backtesting", icon: LineChart, badge: "v4" },
    ],
  },
  {
    title: "RISK & EVALUATION",
    items: [
      { name: "Risk Center & Stress", href: "/risk", icon: ShieldAlert },
      { name: "Model Scorecard & Lab", href: "/evaluation", icon: Award },
      { name: "Watchlists", href: "/watchlists", icon: Eye },
      { name: "Settings & Gateways", href: "/settings", icon: Sliders },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#0a0f1d] border-r border-slate-800/80 flex flex-col h-screen sticky top-0 z-40 shrink-0 select-none">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800/80 flex items-center gap-3 bg-[#0c1224]/80 backdrop-blur-md">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/25 ring-1 ring-white/20">
          <Brain className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-1.5">
            <h1 className="font-extrabold text-slate-100 tracking-tight text-base leading-none">
              AlphaMind <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">AI</span>
            </h1>
            <span className="text-[9px] bg-blue-500/20 text-blue-300 font-mono font-bold px-1.5 py-0.2 rounded border border-blue-500/30">
              v4.1
            </span>
          </div>
          <p className="text-[10px] text-slate-400 mt-1 uppercase tracking-wider font-semibold">
            Institutional Trading OS
          </p>
        </div>
      </div>

      {/* Navigation Groups */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-5 scrollbar-thin scrollbar-thumb-slate-800">
        {navGroups.map((group) => (
          <div key={group.title} className="space-y-1">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 pb-1">
              {group.title}
            </p>
            {group.items.map((item) => {
              const isActive =
                pathname === item.href ||
                (item.href !== "/" &&
                  pathname.startsWith(item.href.split("/")[1] ? `/${item.href.split("/")[1]}` : item.href));
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all group ${
                    isActive
                      ? "bg-blue-600/20 text-cyan-300 border border-blue-500/30 font-semibold shadow-sm"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon
                      className={`w-4 h-4 transition-colors ${
                        isActive ? "text-cyan-400" : "text-slate-500 group-hover:text-slate-300"
                      }`}
                    />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded uppercase ${
                        item.badge === "LIVE"
                          ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 animate-pulse"
                          : item.badge === "PAPER"
                          ? "bg-amber-500/15 text-amber-400 border border-amber-500/30"
                          : "bg-blue-500/15 text-blue-400 border border-blue-500/30"
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </div>
        ))}
      </nav>

      {/* Footer System Status Badge */}
      <div className="p-3 border-t border-slate-800/80 bg-[#080d1a] flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-semibold text-slate-300">Providers Online</span>
        </div>
        <span className="font-mono text-[10px] text-slate-500">FastAPI + SSE</span>
      </div>
    </aside>
  );
}
