"use client";

/**
 * AlphaMind AI v2 — Mission Control hooks.
 * All data-fetching hooks for the Mission Control Terminal.
 */

import { useCallback, useEffect, useReducer, useRef, useState } from "react";
import type {
  ActivityFeedItem,
  DashboardState,
  FundSnapshot,
  IntelligenceSnapshot,
  LiveTick,
  Notification,
  ReasoningRecord,
  ReplayStatus,
  SearchResponse,
  SystemHealth,
  TimelineStats,
} from "@/lib/missionControlTypes";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ── Generic data fetch hook ───────────────────────────────────────────────────

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

type FetchAction<T> =
  | { type: "LOADING" }
  | { type: "SUCCESS"; payload: T }
  | { type: "ERROR"; payload: string };

function fetchReducer<T>(state: FetchState<T>, action: FetchAction<T>): FetchState<T> {
  switch (action.type) {
    case "LOADING":
      return { ...state, loading: true, error: null };
    case "SUCCESS":
      return { data: action.payload, loading: false, error: null };
    case "ERROR":
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
}

function useFetch<T>(url: string, intervalMs?: number): FetchState<T> & { refetch: () => void } {
  const [state, dispatch] = useReducer(fetchReducer<T>, {
    data: null,
    loading: true,
    error: null,
  });

  const fetch_ = useCallback(async () => {
    dispatch({ type: "LOADING" });
    try {
      const resp = await fetch(url, { cache: "no-store" });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = (await resp.json()) as T;
      dispatch({ type: "SUCCESS", payload: data });
    } catch (e) {
      dispatch({ type: "ERROR", payload: e instanceof Error ? e.message : "Unknown error" });
    }
  }, [url]);

  useEffect(() => {
    void fetch_();
    if (intervalMs) {
      const id = setInterval(() => void fetch_(), intervalMs);
      return () => clearInterval(id);
    }
  }, [fetch_, intervalMs]);

  return { ...state, refetch: fetch_ };
}

// ── Dashboard (full aggregated state, refreshes every 15s) ───────────────────

export function useDashboard() {
  return useFetch<DashboardState>(`${API}/api/v1/mission-control/dashboard`, 15_000);
}

// ── System health (refreshes every 10s) ──────────────────────────────────────

export function useSystemHealth() {
  return useFetch<SystemHealth>(`${API}/api/v1/mission-control/health`, 10_000);
}

// ── Activity feed (refreshes every 8s) ───────────────────────────────────────

export function useActivityFeed(limit = 30) {
  return useFetch<{ items: ActivityFeedItem[]; total: number; generated_at_utc: string }>(
    `${API}/api/v1/mission-control/activity-feed?limit=${limit}`,
    8_000,
  );
}

// ── Funds (refreshes every 12s) ───────────────────────────────────────────────

export function useFunds() {
  return useFetch<{ funds: FundSnapshot[]; total_aum_usd: number; generated_at_utc: string }>(
    `${API}/api/v1/mission-control/funds`,
    12_000,
  );
}

// ── Intelligence dashboard (refreshes every 20s) ─────────────────────────────

export function useIntelligence() {
  return useFetch<IntelligenceSnapshot>(`${API}/api/v1/mission-control/intelligence`, 20_000);
}

// ── Notifications (refreshes every 15s) ──────────────────────────────────────

export function useNotifications(limit = 10) {
  return useFetch<{ notifications: Notification[]; unread_count: number }>(
    `${API}/api/v1/mission-control/notifications?limit=${limit}`,
    15_000,
  );
}

// ── Timeline statistics (refreshes every 20s) ────────────────────────────────

export function useTimelineStats() {
  return useFetch<TimelineStats & { generated_at_utc: string }>(
    `${API}/api/v1/mission-control/timeline-stats`,
    20_000,
  );
}

// ── Reasoning record for Decision Inspector ───────────────────────────────────

export function useReasoningRecord(reasoningId: string | null) {
  const [state, dispatch] = useReducer(fetchReducer<ReasoningRecord>, {
    data: null,
    loading: false,
    error: null,
  });

  useEffect(() => {
    if (!reasoningId) return;
    dispatch({ type: "LOADING" });
    void (async () => {
      try {
        const resp = await fetch(
          `${API}/api/v1/mission-control/reasoning/${encodeURIComponent(reasoningId)}`,
        );
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = (await resp.json()) as ReasoningRecord;
        dispatch({ type: "SUCCESS", payload: data });
      } catch (e) {
        dispatch({ type: "ERROR", payload: e instanceof Error ? e.message : "Unknown error" });
      }
    })();
  }, [reasoningId]);

  return state;
}

// ── Chess replay ──────────────────────────────────────────────────────────────

export function useReplayStatus() {
  return useFetch<ReplayStatus>(`${API}/api/v1/mission-control/replay/status`, 5_000);
}

export function useReplayControls() {
  const [position, setPosition] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [frame, setFrame] = useState<Record<string, unknown> | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const step = useCallback(async (direction: "forward" | "backward") => {
    try {
      const resp = await fetch(`${API}/api/v1/mission-control/replay/step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction }),
      });
      const data = (await resp.json()) as { frame: Record<string, unknown>; position: { current_step: number } };
      setFrame(data.frame as Record<string, unknown>);
      setPosition(data.position.current_step ?? 0);
    } catch {
      /* silent */
    }
  }, []);

  const jump = useCallback(async (targetStep: number) => {
    try {
      const resp = await fetch(`${API}/api/v1/mission-control/replay/jump`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ step: targetStep }),
      });
      const data = (await resp.json()) as { position: { current_step: number } };
      setPosition(data.position.current_step ?? targetStep);
      setFrame(null);
    } catch {
      /* silent */
    }
  }, []);

  const play = useCallback(() => {
    setIsPlaying(true);
    intervalRef.current = setInterval(() => void step("forward"), 1500);
  }, [step]);

  const pause = useCallback(() => {
    setIsPlaying(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  }, []);

  useEffect(() => () => { if (intervalRef.current) clearInterval(intervalRef.current); }, []);

  return { position, isPlaying, frame, step, jump, play, pause };
}

// ── Global search ─────────────────────────────────────────────────────────────

export function useGlobalSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const search = useCallback((q: string) => {
    setQuery(q);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!q.trim()) {
      setResults(null);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const resp = await fetch(
          `${API}/api/v1/mission-control/search?q=${encodeURIComponent(q)}&limit=10`,
        );
        const data = (await resp.json()) as SearchResponse;
        setResults(data);
      } catch {
        /* silent */
      } finally {
        setLoading(false);
      }
    }, 300);
  }, []);

  useEffect(() => () => { if (debounceRef.current) clearTimeout(debounceRef.current); }, []);

  return { query, results, loading, search };
}

// ── SSE Live stream ───────────────────────────────────────────────────────────

export function useLiveStream(): LiveTick | null {
  const [tick, setTick] = useState<LiveTick | null>(null);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const es = new EventSource(`${API}/api/v1/mission-control/stream?tick_interval=3.0`);
    esRef.current = es;

    es.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data as string) as LiveTick;
        setTick(data);
      } catch {
        /* ignore malformed ticks */
      }
    };

    return () => {
      es.close();
    };
  }, []);

  return tick;
}
