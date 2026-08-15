"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  BarChart3,
  Calendar,
  ChevronDown,
  Eye,
  EyeOff,
  LineChart,
  Maximize2,
  RefreshCw,
  Sparkles,
  TrendingUp,
  Zap,
} from "lucide-react";

export interface CandleData {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface ForecastCandle {
  timestamp_utc: string;
  open: number;
  high: number;
  low: number;
  close: number;
  uncertainty_upper: number;
  uncertainty_lower: number;
}

interface Props {
  symbol: string;
  initialCandles?: CandleData[];
  forecastCandles?: ForecastCandle[];
  height?: number;
  onTimeframeChange?: (tf: string) => void;
}

export default function InteractiveCandlestickChart({
  symbol,
  initialCandles = [],
  forecastCandles = [],
  height = 420,
}: Props) {
  const [candles, setCandles] = useState<CandleData[]>(initialCandles);
  const [timeframe, setTimeframe] = useState<string>("1Y");
  const [loading, setLoading] = useState<boolean>(false);
  const [showSMA50, setShowSMA50] = useState<boolean>(true);
  const [showSMA200, setShowSMA200] = useState<boolean>(true);
  const [showBollinger, setShowBollinger] = useState<boolean>(true);
  const [showRSI, setShowRSI] = useState<boolean>(true);
  const [showForecast, setShowForecast] = useState<boolean>(true);
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  // Fetch real OHLCV historical bars from backend API
  const fetchBars = async (tf: string) => {
    setLoading(true);
    try {
      const periodMap: Record<string, string> = {
        "1D": "1d",
        "5D": "5d",
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "1Y": "1y",
        "5Y": "5y",
        MAX: "max",
      };
      const period = periodMap[tf] || "1y";
      const interval = tf === "1D" ? "15m" : tf === "5D" ? "1h" : "1d";
      const res = await fetch(
        `/api/v1/market/bars/${encodeURIComponent(symbol)}?period=${period}&interval=${interval}`
      );
      if (res.ok) {
        const data = await res.json();
        setCandles(data.bars || []);
      }
    } catch {
      // Keep initial if fetch fails
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBars(timeframe);
  }, [symbol, timeframe]);

  // Compute Technical Indicators
  const { sma50, sma200, bollingerUpper, bollingerLower, rsiValues, minPrice, maxPrice } =
    useMemo(() => {
      if (candles.length === 0) {
        return {
          sma50: [],
          sma200: [],
          bollingerUpper: [],
          bollingerLower: [],
          rsiValues: [],
          minPrice: 0,
          maxPrice: 100,
        };
      }

      const closes = candles.map((c) => c.close);
      let minP = Math.min(...candles.map((c) => c.low));
      let maxP = Math.max(...candles.map((c) => c.high));

      if (showForecast && forecastCandles.length > 0) {
        const fMax = Math.max(...forecastCandles.map((f) => f.uncertainty_upper));
        const fMin = Math.min(...forecastCandles.map((f) => f.uncertainty_lower));
        minP = Math.min(minP, fMin);
        maxP = Math.max(maxP, fMax);
      }

      // Add 5% padding
      const range = maxP - minP || 1.0;
      minP = Math.max(0, minP - range * 0.05);
      maxP = maxP + range * 0.05;

      // SMA 50 & 200
      const calcSMA = (period: number) => {
        return closes.map((_, i) => {
          if (i < period - 1) return null;
          const slice = closes.slice(i - period + 1, i + 1);
          return slice.reduce((a, b) => a + b, 0) / period;
        });
      };

      const s50 = calcSMA(Math.min(50, Math.floor(candles.length / 2)));
      const s200 = calcSMA(Math.min(200, Math.floor(candles.length * 0.8)));

      // Bollinger Bands (20 periods, 2 std dev)
      const bPeriod = Math.min(20, candles.length);
      const bUpper: (number | null)[] = [];
      const bLower: (number | null)[] = [];

      closes.forEach((_, i) => {
        if (i < bPeriod - 1) {
          bUpper.push(null);
          bLower.push(null);
        } else {
          const slice = closes.slice(i - bPeriod + 1, i + 1);
          const mean = slice.reduce((a, b) => a + b, 0) / bPeriod;
          const variance = slice.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / bPeriod;
          const std = Math.sqrt(variance);
          bUpper.push(mean + 2 * std);
          bLower.push(mean - 2 * std);
        }
      });

      // RSI 14
      const rsi: (number | null)[] = [];
      const rPeriod = 14;
      let gains = 0;
      let losses = 0;

      for (let i = 0; i < closes.length; i++) {
        if (i === 0) {
          rsi.push(50);
          continue;
        }
        const diff = closes[i] - closes[i - 1];
        if (i <= rPeriod) {
          if (diff >= 0) gains += diff;
          else losses += Math.abs(diff);
          rsi.push(50);
        } else {
          const gain = diff >= 0 ? diff : 0;
          const loss = diff < 0 ? Math.abs(diff) : 0;
          gains = (gains * (rPeriod - 1) + gain) / rPeriod;
          losses = (losses * (rPeriod - 1) + loss) / rPeriod;
          const rs = losses === 0 ? 100 : gains / losses;
          rsi.push(100 - 100 / (1 + rs));
        }
      }

      return {
        sma50: s50,
        sma200: s200,
        bollingerUpper: bUpper,
        bollingerLower: bLower,
        rsiValues: rsi,
        minPrice: minP,
        maxPrice: maxP,
      };
    }, [candles, forecastCandles, showForecast]);

  const maxVolume = useMemo(() => {
    if (candles.length === 0) return 1;
    return Math.max(...candles.map((c) => c.volume));
  }, [candles]);

  const totalPoints = candles.length + (showForecast ? forecastCandles.length : 0);
  const chartWidth = 900;
  const mainHeight = showRSI ? height * 0.7 : height * 0.85;
  const rsiHeight = showRSI ? height * 0.22 : 0;
  const volumeHeight = mainHeight * 0.2;

  const getY = (price: number) => {
    return mainHeight - ((price - minPrice) / (maxPrice - minPrice || 1)) * (mainHeight - 20) - 10;
  };

  const getX = (index: number) => {
    return (index / Math.max(1, totalPoints - 1)) * (chartWidth - 80) + 40;
  };

  const activeCandle = hoverIndex !== null && hoverIndex < candles.length ? candles[hoverIndex] : candles[candles.length - 1];

  return (
    <div className="w-full rounded-2xl bg-slate-950 border border-slate-800 p-5 space-y-4 shadow-2xl">
      {/* Chart Control Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800/80 pb-3">
        {/* Active Candle Hover Telemetry */}
        {activeCandle ? (
          <div className="flex items-center gap-4 text-xs">
            <span className="font-bold text-white tracking-wider">{symbol}</span>
            <span className="text-slate-400">
              O: <span className="font-semibold text-white">${activeCandle.open.toFixed(2)}</span>
            </span>
            <span className="text-slate-400">
              H: <span className="font-semibold text-emerald-400">${activeCandle.high.toFixed(2)}</span>
            </span>
            <span className="text-slate-400">
              L: <span className="font-semibold text-rose-400">${activeCandle.low.toFixed(2)}</span>
            </span>
            <span className="text-slate-400">
              C:{" "}
              <span
                className={`font-semibold ${
                  activeCandle.close >= activeCandle.open ? "text-emerald-400" : "text-rose-400"
                }`}
              >
                ${activeCandle.close.toFixed(2)}
              </span>
            </span>
            <span className="text-slate-400">
              Vol:{" "}
              <span className="font-semibold text-slate-200">
                {(activeCandle.volume / 1e6).toFixed(1)}M
              </span>
            </span>
          </div>
        ) : (
          <div className="text-xs text-slate-400">Interactive Institutional Chart</div>
        )}

        {/* Timeframe Selector */}
        <div className="flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800 text-xs">
          {["1D", "5D", "1M", "3M", "6M", "1Y", "5Y", "MAX"].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-2.5 py-1 rounded-lg font-semibold transition-all ${
                timeframe === tf
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>

        {/* Indicator Toggles */}
        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={() => setShowSMA50(!showSMA50)}
            className={`px-2.5 py-1 rounded-lg border font-medium transition-all ${
              showSMA50
                ? "bg-blue-500/20 text-blue-400 border-blue-500/40"
                : "bg-slate-900 text-slate-500 border-slate-800"
            }`}
          >
            SMA 50
          </button>
          <button
            onClick={() => setShowSMA200(!showSMA200)}
            className={`px-2.5 py-1 rounded-lg border font-medium transition-all ${
              showSMA200
                ? "bg-purple-500/20 text-purple-400 border-purple-500/40"
                : "bg-slate-900 text-slate-500 border-slate-800"
            }`}
          >
            SMA 200
          </button>
          <button
            onClick={() => setShowBollinger(!showBollinger)}
            className={`px-2.5 py-1 rounded-lg border font-medium transition-all ${
              showBollinger
                ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/40"
                : "bg-slate-900 text-slate-500 border-slate-800"
            }`}
          >
            Bollinger
          </button>
          <button
            onClick={() => setShowRSI(!showRSI)}
            className={`px-2.5 py-1 rounded-lg border font-medium transition-all ${
              showRSI
                ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
                : "bg-slate-900 text-slate-500 border-slate-800"
            }`}
          >
            RSI 14
          </button>
          {forecastCandles.length > 0 && (
            <button
              onClick={() => setShowForecast(!showForecast)}
              className={`px-2.5 py-1 rounded-lg border font-semibold flex items-center gap-1 transition-all ${
                showForecast
                  ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/40 shadow-sm"
                  : "bg-slate-900 text-slate-500 border-slate-800"
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              Kronos Forecast Cone
            </button>
          )}
        </div>
      </div>

      {/* Main SVG Candlestick Canvas */}
      <div className="relative w-full overflow-hidden">
        {loading && (
          <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-20 flex items-center justify-center text-xs text-blue-400">
            <RefreshCw className="w-5 h-5 animate-spin mr-2" /> Loading real historical price bars...
          </div>
        )}

        <svg
          viewBox={`0 0 ${chartWidth} ${height}`}
          className="w-full select-none cursor-crosshair"
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const idx = Math.floor((mouseX / rect.width) * totalPoints);
            if (idx >= 0 && idx < totalPoints) setHoverIndex(idx);
          }}
          onMouseLeave={() => setHoverIndex(null)}
        >
          <defs>
            <linearGradient id="forecastConeGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.05" />
            </linearGradient>
            <linearGradient id="volumeGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#1e293b" stopOpacity="0.05" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[0.2, 0.4, 0.6, 0.8].map((ratio) => {
            const y = mainHeight * ratio;
            const p = maxPrice - ratio * (maxPrice - minPrice);
            return (
              <g key={ratio}>
                <line x1="40" y1={y} x2={chartWidth - 40} y2={y} stroke="#1e293b" strokeDasharray="3 3" />
                <text x={chartWidth - 35} y={y + 4} fill="#64748b" fontSize="10">
                  ${p.toFixed(1)}
                </text>
              </g>
            );
          })}

          {/* Volume Bars */}
          {candles.map((c, i) => {
            const x = getX(i);
            const vHeight = (c.volume / (maxVolume || 1)) * volumeHeight;
            const y = mainHeight - vHeight;
            return (
              <rect
                key={`vol_${i}`}
                x={x - 2}
                y={y}
                width="4"
                height={vHeight}
                fill={c.close >= c.open ? "#10b981" : "#f43f5e"}
                opacity="0.3"
              />
            );
          })}

          {/* Bollinger Bands Shading & Lines */}
          {showBollinger && (
            <>
              <path
                d={candles
                  .map((_, i) => {
                    const up = bollingerUpper[i];
                    return up !== null ? `${i === 0 ? "M" : "L"} ${getX(i)} ${getY(up)}` : "";
                  })
                  .filter(Boolean)
                  .join(" ")}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="1"
                strokeDasharray="2 2"
                opacity="0.6"
              />
              <path
                d={candles
                  .map((_, i) => {
                    const low = bollingerLower[i];
                    return low !== null ? `${i === 0 ? "M" : "L"} ${getX(i)} ${getY(low)}` : "";
                  })
                  .filter(Boolean)
                  .join(" ")}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="1"
                strokeDasharray="2 2"
                opacity="0.6"
              />
            </>
          )}

          {/* SMA 50 Line */}
          {showSMA50 && (
            <path
              d={candles
                .map((_, i) => {
                  const s = sma50[i];
                  return s !== null ? `${i === 0 ? "M" : "L"} ${getX(i)} ${getY(s)}` : "";
                })
                .filter(Boolean)
                .join(" ")}
              fill="none"
              stroke="#3b82f6"
              strokeWidth="1.5"
              opacity="0.8"
            />
          )}

          {/* SMA 200 Line */}
          {showSMA200 && (
            <path
              d={candles
                .map((_, i) => {
                  const s = sma200[i];
                  return s !== null ? `${i === 0 ? "M" : "L"} ${getX(i)} ${getY(s)}` : "";
                })
                .filter(Boolean)
                .join(" ")}
              fill="none"
              stroke="#a855f7"
              strokeWidth="1.5"
              opacity="0.8"
            />
          )}

          {/* Candlesticks */}
          {candles.map((c, i) => {
            const x = getX(i);
            const isBullish = c.close >= c.open;
            const yOpen = getY(c.open);
            const yClose = getY(c.close);
            const yHigh = getY(c.high);
            const yLow = getY(c.low);
            const topY = Math.min(yOpen, yClose);
            const bodyHeight = Math.max(2, Math.abs(yOpen - yClose));
            const color = isBullish ? "#10b981" : "#f43f5e";

            return (
              <g key={`candle_${i}`}>
                {/* Wick */}
                <line x1={x} y1={yHigh} x2={x} y2={yLow} stroke={color} strokeWidth="1" />
                {/* Body */}
                <rect
                  x={x - 3}
                  y={topY}
                  width="6"
                  height={bodyHeight}
                  fill={color}
                  rx="1"
                  stroke={color}
                  strokeWidth="0.5"
                />
              </g>
            );
          })}

          {/* Kronos Forecast Uncertainty Cone Overlay */}
          {showForecast && forecastCandles.length > 0 && (
            <g>
              {/* Uncertainty cone polygon */}
              <polygon
                points={`
                  ${getX(candles.length - 1)},${getY(candles[candles.length - 1]?.close || minPrice)}
                  ${forecastCandles.map((f, i) => `${getX(candles.length + i)},${getY(f.uncertainty_upper)}`).join(" ")}
                  ${forecastCandles
                    .slice()
                    .reverse()
                    .map((f, i) => `${getX(candles.length + forecastCandles.length - 1 - i)},${getY(f.uncertainty_lower)}`)
                    .join(" ")}
                `}
                fill="url(#forecastConeGrad)"
              />
              {/* Forecast path line */}
              <path
                d={`M ${getX(candles.length - 1)} ${getY(candles[candles.length - 1]?.close || minPrice)} ${forecastCandles
                  .map((f, i) => `L ${getX(candles.length + i)} ${getY(f.close)}`)
                  .join(" ")}`}
                fill="none"
                stroke="#10b981"
                strokeWidth="2"
                strokeDasharray="4 4"
              />
            </g>
          )}

          {/* RSI Subpanel */}
          {showRSI && (
            <g transform={`translate(0, ${mainHeight + 10})`}>
              <rect x="40" y="0" width={chartWidth - 80} height={rsiHeight - 15} fill="#0b0f19" rx="6" />
              <line x1="40" y1={(rsiHeight - 15) * 0.3} x2={chartWidth - 40} y2={(rsiHeight - 15) * 0.3} stroke="#f43f5e" strokeDasharray="2 2" opacity="0.4" />
              <line x1="40" y1={(rsiHeight - 15) * 0.7} x2={chartWidth - 40} y2={(rsiHeight - 15) * 0.7} stroke="#10b981" strokeDasharray="2 2" opacity="0.4" />
              <text x="45" y="14" fill="#f59e0b" fontSize="10" fontWeight="bold">
                RSI 14
              </text>
              <path
                d={candles
                  .map((_, i) => {
                    const r = rsiValues[i];
                    if (r === null) return "";
                    const rx = getX(i);
                    const ry = (rsiHeight - 15) - (r / 100) * (rsiHeight - 20) - 5;
                    return `${i === 0 ? "M" : "L"} ${rx} ${ry}`;
                  })
                  .filter(Boolean)
                  .join(" ")}
                fill="none"
                stroke="#f59e0b"
                strokeWidth="1.5"
              />
            </g>
          )}

          {/* Crosshair Inspection Line */}
          {hoverIndex !== null && (
            <g>
              <line
                x1={getX(hoverIndex)}
                y1="10"
                x2={getX(hoverIndex)}
                y2={height - 20}
                stroke="#38bdf8"
                strokeWidth="1"
                strokeDasharray="2 2"
              />
            </g>
          )}
        </svg>
      </div>
    </div>
  );
}
