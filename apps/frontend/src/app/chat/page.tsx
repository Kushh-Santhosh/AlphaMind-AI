import { AnalystChat } from "@/components/chat/AnalystChat";

export default function ChatPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Conversational AI Analyst Workspace</h1>
        <p className="text-xs text-slate-400">Interactive dialogue interface orchestrating research workflows, forecasting scenarios, and risk analysis.</p>
      </div>

      <AnalystChat />
    </div>
  );
}
