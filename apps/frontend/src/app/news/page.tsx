import type { Metadata } from "next";

export const metadata: Metadata = { title: "News | AlphaMind AI" };

export default function NewsPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">News</h1>
      <p className="text-muted-foreground mt-2">Implementation pending Milestone 6.</p>
    </main>
  );
}
