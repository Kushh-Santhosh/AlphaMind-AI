/**
 * AlphaMind AI — Frontend Component Types
 * Shared interface definitions for all UI components.
 */

export interface DashboardCardProps {
  title: string;
  value: string | number;
  description?: string;
  trend?: "up" | "down" | "neutral";
  className?: string;
}

export interface ProbabilityGaugeProps {
  bullPct: number;
  basePct: number;
  bearPct: number;
  label?: string;
}

export interface PriceChartProps {
  symbol: string;
  timeframe?: string;
  height?: number;
}
