"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertCircle,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Bot,
  CheckCircle2,
  ChevronRight,
  Clock,
  DollarSign,
  Flame,
  Layers,
  Percent,
  Play,
  Plus,
  RefreshCw,
  Scale,
  Shield,
  Sparkles,
  TrendingDown,
  TrendingUp,
  Wallet,
  Zap,
} from "lucide-react";

interface Position {
  symbol: string;
  quantity: number;
  average_entry_price: number;
  current_market_price: number;
  unrealized_pnl_usd: number;
  unrealized_return_pct: number;
  market_value_usd: number;
}

interface TradeLog {
  trade_id: string;
  order_id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  commission_usd: number;
  slippage_usd: number;
  timestamp_utc: string;
}

interface PortfolioState {
  total_portfolio_value_usd: number;
  cash_balance_usd: number;
  buying_power_usd: number;
  unrealized_pnl_usd: number;
  realized_pnl_usd: number;
  daily_pnl_usd: number;
  maintenance_margin_required_usd: number;
  is_margin_call: boolean;
  positions_count: number;
}

export default function PaperTradingTerminalPage() {
  const [portfolio, setPortfolio] = useState<PortfolioState | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [trades, setTrades] = useState<TradeLog[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [autonomousLoading, setAutonomousLoading] = useState<boolean>(false);
  const [autonomousMessage, setAutonomousMessage] = useState<string | null>(null);

  // Order Ticket Form State
  const [orderSymbol, setOrderSymbol] = useState<string>("NVDA");
  const [orderSide, setOrderSide] = useState<"BUY" | "SELL">("BUY");
  const [orderType, setOrderType] = useState<"MARKET" | "LIMIT" | "STOP">("MARKET");
  const [orderQuantity, setOrderQuantity] = useState<number>(10);
  const [orderLimitPrice, setOrderLimitPrice] = useState<string>("");
  const [submittingOrder, setSubmittingOrder] = useState<boolean>(false);
  const [orderFeedback, setOrderFeedback] = useState<{ type: "success" | "error"; msg: string } | null>(null);

  const fetchPaperData = async () => {
    setLoading(true);
    try {
      const [pRes, posRes, trdRes] = await Promise.all([
        fetch("/api/v1/trading/portfolio"),
        fetch("/api/v1/trading/positions"),
        fetch("/api/v1/trading/trades"),
      ]);

      if (pRes.ok) setPortfolio(await pRes.json());
      if (posRes.ok) {
        const d = await posRes.json();
        setPositions(d.positions || []);
      }
      if (trdRes.ok) {
        const d = await trdRes.json();
        setTrades(d.trades || []);
      }
    } catch {
      // Handled via state
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPaperData();
  }, []);

  const handleOrderSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittingOrder(true);
    setOrderFeedback(null);
    try {
      const res = await fetch("/api/v1/trading/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          symbol: orderSymbol.trim().toUpperCase(),
          side: orderSide,
          order_type: orderType,
          quantity: Number(orderQuantity),
          limit_price: orderLimitPrice ? parseFloat(orderLimitPrice) : null,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setOrderFeedback({
          type: "success",
          msg: `Filled ${orderSide} ${orderQuantity} ${orderSymbol.toUpperCase()} at $${data.live_quote_used?.toFixed(2)}`,
        });
        fetchPaperData();
      } else {
        setOrderFeedback({
          type: "error",
          msg: data.detail || "Order rejected by exchange risk controls",
        });
      }
    } catch (err: any) {
      setOrderFeedback({ type: "error", msg: "Network error submitting order" });
    } finally {
      setSubmittingOrder(false);
    }
  };

  const triggerAutonomousCycle = async () => {
    setAutonomousLoading(true);
    setAutonomousMessage(null);
    try {
      const res = await fetch("/api/v1/trading/autonomous/cycle", { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        setAutonomousMessage(data.action_taken || "Autonomous cycle completed.");
        fetchPaperData();
      }
    } catch {
      setAutonomousMessage("Error executing autonomous paper loop.");
    } finally {
      setAutonomousLoading(false);
    }
  };

  const totalValue = portfolio?.total_portfolio_value_usd || 100_000.0;
  const cash = portfolio?.cash_balance_usd || 100_000.0;
  const unrealizedPnL = portfolio?.unrealized_pnl_usd || 0.0;
  const realizedPnL = portfolio?.realized_pnl_usd || 0.0;

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 p-6 space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#0d1322] via-[#090e1c] to-[#0d1428] border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold tracking-tight text-white">Autonomous Paper Trader</h1>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  PAPER MODE
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Simulated execution matching with dynamic slippage, commissions, and live provider quotes.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={triggerAutonomousCycle}
            disabled={autonomousLoading}
            className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-lg shadow-emerald-600/20"
          >
            <Zap className={`w-4 h-4 ${autonomousLoading ? "animate-spin" : ""}`} />
            {autonomousLoading ? "Running Agent Scan & Execute..." : "Trigger Autonomous Cycle"}
          </button>
          <button
            onClick={fetchPaperData}
            disabled={loading}
            className="p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-all text-xs"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {autonomousMessage && (
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-blue-400 shrink-0" />
          <span>{autonomousMessage}</span>
        </div>
      )}

      {/* Portfolio KPI Summary Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1 shadow-lg">
          <span className="text-xs text-slate-400 font-medium">Total Portfolio Value</span>
          <p className="text-2xl font-extrabold text-white">
            ${totalValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <p className="text-xs text-slate-500">Live Marked-to-Market Equity</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1 shadow-lg">
          <span className="text-xs text-slate-400 font-medium">Available Cash</span>
          <p className="text-2xl font-extrabold text-slate-200">
            ${cash.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <p className="text-xs text-emerald-400 font-medium">
            Buying Power: ${portfolio?.buying_power_usd ? (portfolio.buying_power_usd / 1e3).toFixed(1) + "k" : "100.0k"}
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1 shadow-lg">
          <span className="text-xs text-slate-400 font-medium">Unrealized P&L</span>
          <p
            className={`text-2xl font-extrabold ${
              unrealizedPnL >= 0 ? "text-emerald-400" : "text-rose-400"
            }`}
          >
            {unrealizedPnL >= 0 ? "+" : ""}${unrealizedPnL.toFixed(2)}
          </p>
          <p className="text-xs text-slate-500">Open Position Floating Return</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1 shadow-lg">
          <span className="text-xs text-slate-400 font-medium">Realized P&L</span>
          <p
            className={`text-2xl font-extrabold ${
              realizedPnL >= 0 ? "text-emerald-400" : "text-rose-400"
            }`}
          >
            {realizedPnL >= 0 ? "+" : ""}${realizedPnL.toFixed(2)}
          </p>
          <p className="text-xs text-slate-500">Closed Position Cumulative Net</p>
        </div>
      </div>

      {/* Main Trading Terminal: Order Entry Ticket + Open Positions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Interactive Order Entry Ticket */}
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-5 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Zap className="w-4 h-4 text-blue-400" />
              Order Entry Ticket
            </h2>
            <span className="text-xs font-semibold text-slate-400">Virtual Fill Engine</span>
          </div>

          <form onSubmit={handleOrderSubmit} className="space-y-4 text-xs">
            {/* Side Selector */}
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setOrderSide("BUY")}
                className={`py-2.5 rounded-xl font-bold transition-all ${
                  orderSide === "BUY"
                    ? "bg-emerald-600 text-white shadow-lg shadow-emerald-600/20"
                    : "bg-slate-950 text-slate-400 border border-slate-800"
                }`}
              >
                BUY (LONG)
              </button>
              <button
                type="button"
                onClick={() => setOrderSide("SELL")}
                className={`py-2.5 rounded-xl font-bold transition-all ${
                  orderSide === "SELL"
                    ? "bg-rose-600 text-white shadow-lg shadow-rose-600/20"
                    : "bg-slate-950 text-slate-400 border border-slate-800"
                }`}
              >
                SELL (SHORT)
              </button>
            </div>

            {/* Symbol Input */}
            <div className="space-y-1.5">
              <label className="text-slate-400 font-medium">Asset Symbol</label>
              <input
                type="text"
                value={orderSymbol}
                onChange={(e) => setOrderSymbol(e.target.value)}
                placeholder="e.g. NVDA, AAPL, RELIANCE.NS, BTC-USD, WTI"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white font-semibold placeholder-slate-600 focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            {/* Order Type */}
            <div className="space-y-1.5">
              <label className="text-slate-400 font-medium">Order Type</label>
              <div className="grid grid-cols-3 gap-1.5">
                {(["MARKET", "LIMIT", "STOP"] as const).map((t) => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setOrderType(t)}
                    className={`py-2 rounded-xl font-semibold transition-all ${
                      orderType === t
                        ? "bg-blue-600/20 text-blue-400 border border-blue-500/40"
                        : "bg-slate-950 text-slate-500 border border-slate-800"
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>

            {/* Quantity */}
            <div className="space-y-1.5">
              <label className="text-slate-400 font-medium">Quantity (Units)</label>
              <input
                type="number"
                min="0.01"
                step="any"
                value={orderQuantity}
                onChange={(e) => setOrderQuantity(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white font-semibold focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            {/* Limit Price (if LIMIT) */}
            {orderType === "LIMIT" && (
              <div className="space-y-1.5">
                <label className="text-slate-400 font-medium">Limit Price ($)</label>
                <input
                  type="number"
                  step="any"
                  value={orderLimitPrice}
                  onChange={(e) => setOrderLimitPrice(e.target.value)}
                  placeholder="Target price..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white font-semibold focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            )}

            {orderFeedback && (
              <div
                className={`p-3 rounded-xl border text-xs ${
                  orderFeedback.type === "success"
                    ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/30"
                    : "bg-rose-500/10 text-rose-300 border-rose-500/30"
                }`}
              >
                {orderFeedback.msg}
              </div>
            )}

            <button
              type="submit"
              disabled={submittingOrder}
              className={`w-full py-3 rounded-xl font-bold text-white transition-all shadow-xl flex items-center justify-center gap-2 ${
                orderSide === "BUY"
                  ? "bg-emerald-600 hover:bg-emerald-500 shadow-emerald-600/20"
                  : "bg-rose-600 hover:bg-rose-500 shadow-rose-600/20"
              }`}
            >
              {submittingOrder ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                `Execute Paper ${orderSide} Order`
              )}
            </button>
          </form>
        </div>

        {/* Right Column: Open Positions Table */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-blue-400" />
                Active Multi-Asset Positions ({positions.length})
              </h2>
              <span className="text-xs text-slate-400">Live Marked-to-Market</span>
            </div>

            <div className="overflow-x-auto mt-4">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800">
                  <tr>
                    <th className="p-3">Asset</th>
                    <th className="p-3">Quantity</th>
                    <th className="p-3">Avg Entry</th>
                    <th className="p-3">Live Price</th>
                    <th className="p-3">Market Value</th>
                    <th className="p-3">Unrealized P&L</th>
                    <th className="p-3 text-right">Return %</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {positions.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="p-8 text-center text-slate-500">
                        No active paper trading positions. Place an order or trigger the autonomous trader.
                      </td>
                    </tr>
                  ) : (
                    positions.map((pos) => (
                      <tr key={pos.symbol} className="hover:bg-slate-800/30 transition-all">
                        <td className="p-3 font-bold text-white flex items-center gap-2">
                          <div className="w-5 h-5 rounded bg-blue-600/20 text-[10px] text-blue-400 flex items-center justify-center">
                            {pos.symbol.slice(0, 2)}
                          </div>
                          {pos.symbol}
                        </td>
                        <td className="p-3 text-slate-300">{pos.quantity.toFixed(2)}</td>
                        <td className="p-3 text-slate-300">${pos.average_entry_price.toFixed(2)}</td>
                        <td className="p-3 text-white font-semibold">${pos.current_market_price.toFixed(2)}</td>
                        <td className="p-3 text-slate-200">${pos.market_value_usd.toFixed(2)}</td>
                        <td
                          className={`p-3 font-semibold ${
                            pos.unrealized_pnl_usd >= 0 ? "text-emerald-400" : "text-rose-400"
                          }`}
                        >
                          {pos.unrealized_pnl_usd >= 0 ? "+" : ""}${pos.unrealized_pnl_usd.toFixed(2)}
                        </td>
                        <td
                          className={`p-3 text-right font-bold ${
                            pos.unrealized_return_pct >= 0 ? "text-emerald-400" : "text-rose-400"
                          }`}
                        >
                          {pos.unrealized_return_pct >= 0 ? "+" : ""}
                          {pos.unrealized_return_pct.toFixed(2)}%
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Commission per trade: $1.00 • Estimated slippage: 2.0 bps</span>
            <Link href="/risk" className="text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1">
              View Risk Center <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Trade Execution History Table */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-emerald-400" />
            Simulated Trade Execution Log ({trades.length})
          </h2>
          <span className="text-xs text-slate-400">Audit Trail with Slippage & Fees</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">Trade ID</th>
                <th className="p-3">Asset</th>
                <th className="p-3">Side</th>
                <th className="p-3">Filled Qty</th>
                <th className="p-3">Fill Price</th>
                <th className="p-3">Slippage</th>
                <th className="p-3">Commission</th>
                <th className="p-3 text-right">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {trades.length === 0 ? (
                <tr>
                  <td colSpan={8} className="p-8 text-center text-slate-500">
                    No simulated executions recorded yet.
                  </td>
                </tr>
              ) : (
                trades.slice(-10).reverse().map((t) => (
                  <tr key={t.trade_id} className="hover:bg-slate-800/30 transition-all">
                    <td className="p-3 font-mono text-slate-500 text-[11px]">{t.trade_id}</td>
                    <td className="p-3 font-bold text-white">{t.symbol}</td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          t.side === "BUY"
                            ? "bg-emerald-500/20 text-emerald-400"
                            : "bg-rose-500/20 text-rose-400"
                        }`}
                      >
                        {t.side}
                      </span>
                    </td>
                    <td className="p-3 text-slate-300">{t.quantity.toFixed(2)}</td>
                    <td className="p-3 text-white font-semibold">${t.price.toFixed(2)}</td>
                    <td className="p-3 text-slate-400">${t.slippage_usd.toFixed(3)}</td>
                    <td className="p-3 text-slate-400">${t.commission_usd.toFixed(2)}</td>
                    <td className="p-3 text-right text-slate-500">{t.timestamp_utc}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
