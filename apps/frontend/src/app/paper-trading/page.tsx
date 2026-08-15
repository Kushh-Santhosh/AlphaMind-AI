import type { Metadata } from "next";
export const metadata: Metadata = { title: "Paper Trading | AlphaMind AI" };
export default function PaperTradingPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">Paper Trading</h1>
      <p className="text-muted-foreground mt-2">Simulated execution engine — Implementation pending Milestone 6.</p>
    </main>
  );
}
