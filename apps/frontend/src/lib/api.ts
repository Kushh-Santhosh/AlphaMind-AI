/**
 * AlphaMind AI — API Client Stub
 * Typed HTTP client for the FastAPI backend.
 * Full implementation pending Milestone 6.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  health: () => request<{ status: string; version: string }>("/health"),
  market: {
    search: (query: string) =>
      request<unknown>(`/api/v1/market/search?query=${encodeURIComponent(query)}`),
    bars: (symbol: string, timeframe = "1D") =>
      request<unknown>(`/api/v1/market/bars/${symbol}?timeframe=${timeframe}`),
    quote: (symbol: string) => request<unknown>(`/api/v1/market/quote/${symbol}`),
  },
  research: {
    analyze: (body: unknown) =>
      request<unknown>("/api/v1/research/analyze", {
        method: "POST",
        body: JSON.stringify(body),
      }),
  },
};
