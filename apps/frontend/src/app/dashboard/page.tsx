import type { Metadata } from "next";

export const metadata: Metadata = { title: "Dashboard | AlphaMind AI" };

export default function DashboardPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="text-muted-foreground mt-2">Implementation pending Milestone 6.</p>
    </main>
  );
}
