/**
 * AlphaMind AI — useAgentStream Hook
 * Consumes Server-Sent Events (SSE) from the backend agent execution stream.
 * Full implementation pending Milestone 6.
 */

"use client";

import { useState, useCallback } from "react";
import type { AgentExecutionStep } from "@/lib/types";

interface UseAgentStreamReturn {
  steps: AgentExecutionStep[];
  isStreaming: boolean;
  startStream: (sessionId: string) => void;
  stopStream: () => void;
}

export function useAgentStream(): UseAgentStreamReturn {
  const [steps] = useState<AgentExecutionStep[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const startStream = useCallback((sessionId: string) => {
    // Full SSE implementation pending Milestone 6
    setIsStreaming(true);
    console.info(`[AlphaMind] Starting SSE stream for session: ${sessionId}`);
  }, []);

  const stopStream = useCallback(() => {
    setIsStreaming(false);
  }, []);

  return { steps, isStreaming, startStream, stopStream };
}
