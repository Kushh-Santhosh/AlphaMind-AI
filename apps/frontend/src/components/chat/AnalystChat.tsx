"use client";

import { useState } from "react";
import { Send, Sparkles, User, FileText, CheckCircle2, ChevronRight } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: string[];
  suggestedFollowups?: string[];
}

export function AnalystChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "msg_1",
      role: "assistant",
      content:
        "Hello! I am your AI Analyst. I can orchestrate end-to-end research workflows across company filings, financial statement normalization, Knowledge Graph relationships, probabilistic return forecasting, and portfolio risk decomposition. What would you like to analyze?",
      suggestedFollowups: [
        "Analyze AAPL financial statements & 10-K",
        "Generate 30-day forecast scenarios for NVDA",
        "Decompose MSFT portfolio risk contribution",
        "Audit SEC disclosure data contradictions",
      ],
    },
  ]);
  const [input, setInput] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    const userMsgId = `user_${messages.length + 1}`;
    const userMsg: Message = { id: userMsgId, role: "user", content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsProcessing(true);

    setTimeout(() => {
      const assistantMsg: Message = {
        id: `asst_${userMsgId}`,
        role: "assistant",
        content: `Analyzed '${query}': Extracted factors from SEC filings, computed financial health trends (+0.75), generated 5-tier probabilistic return distributions, and verified 100% calculation lineage against EDGAR disclosures.`,
        citations: ["SEC EDGAR 10-K FY2025 Item 7", "FRED Fed Funds Rate Series", "AlphaMind Knowledge Graph"],
        suggestedFollowups: [
          "Explain forecast feature importance",
          "Run Monte Carlo 10,000 stochastic trajectories",
          "Generate executive summary report",
        ],
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsProcessing(false);
    }, 1200);
  };

  return (
    <div className="bg-[#0d1322] border border-slate-800 rounded-xl h-[700px] flex flex-col shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 bg-[#090d16]/70 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="font-semibold text-slate-100 text-sm">Conversational AI Analyst</h2>
            <p className="text-[11px] text-slate-400">Multi-Engine Autonomous Orchestrator</p>
          </div>
        </div>
        <span className="text-[11px] bg-slate-800 text-slate-300 px-2.5 py-1 rounded-full border border-slate-700">
          Session Active
        </span>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex gap-3 ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {m.role === "assistant" && (
              <div className="w-7 h-7 rounded-full bg-blue-600/20 text-blue-400 border border-blue-500/30 flex items-center justify-center shrink-0 mt-1">
                <Sparkles className="w-3.5 h-3.5" />
              </div>
            )}

            <div className={`max-w-2xl space-y-2`}>
              <div
                className={`p-3.5 rounded-2xl text-xs leading-relaxed ${
                  m.role === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none shadow-lg"
                }`}
              >
                {m.content}
              </div>

              {/* Citations */}
              {m.citations && (
                <div className="p-2.5 rounded-lg bg-[#090d16] border border-slate-800/80 text-[11px] space-y-1">
                  <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <FileText className="w-3 h-3 text-blue-400" /> Evidence References
                  </div>
                  <ul className="space-y-0.5 text-slate-300">
                    {m.citations.map((c, i) => (
                      <li key={i} className="flex items-center gap-1.5">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400 shrink-0" />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Suggested Followups */}
              {m.suggestedFollowups && (
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {m.suggestedFollowups.map((f, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(f)}
                      className="text-[11px] bg-slate-900 hover:bg-slate-800 text-blue-300 hover:text-blue-200 border border-slate-800 rounded-full px-3 py-1 flex items-center gap-1 transition-all"
                    >
                      <span>{f}</span>
                      <ChevronRight className="w-3 h-3 text-blue-400" />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {m.role === "user" && (
              <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 mt-1">
                <User className="w-3.5 h-3.5" />
              </div>
            )}
          </div>
        ))}

        {isProcessing && (
          <div className="flex items-center gap-2 text-xs text-blue-400 animate-pulse p-2">
            <Sparkles className="w-4 h-4" />
            <span>Orchestrating workflow across platforms engines...</span>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-slate-800 bg-[#090d16]/70">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            placeholder="Ask AI Analyst to research, forecast, or decompose risk..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-slate-900 border border-slate-800 focus:border-blue-500 rounded-xl px-4 py-2.5 text-xs text-slate-100 outline-none placeholder:text-slate-500"
          />
          <button
            type="submit"
            disabled={isProcessing || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-xl px-4 py-2.5 text-xs font-semibold flex items-center gap-2 transition-all shadow-lg shadow-blue-500/20"
          >
            <span>Send</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </div>
    </div>
  );
}
