/**
 * AlphaMind AI — Shared TypeScript Type Definitions
 * Mirrors the PredictionSafetySchema and agent state interfaces from packages/shared.
 */

export interface ProbabilityDistribution {
  bullScenarioPct: number;
  baseScenarioPct: number;
  bearScenarioPct: number;
}

export interface ConfidenceInterval {
  lowerBoundPct: number;
  expectedReturnPct: number;
  upperBoundPct: number;
}

export interface PredictionSafetyPayload {
  asset: string;
  predictionHorizonDays: number;
  probabilityDistribution: ProbabilityDistribution;
  confidenceInterval95: ConfidenceInterval;
  modelConfidenceScore: number;
  dataQualityScore: number;
  predictionExpiryTimestamp: string;
  supportingEvidence: string[];
  contradictingEvidence: string[];
  knownUnknowns: string[];
  historicalModelAccuracyBrierScore: number;
  disclaimer: string;
}

export interface MarketBar {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface AgentExecutionStep {
  agent: string;
  status: string;
  message?: string;
  confidence?: number;
  timestamp: string;
}

export type UserRole = "guest" | "trader" | "quant_analyst" | "admin";

export interface UserProfile {
  id: string;
  email: string;
  role: UserRole;
  createdAt: string;
}
