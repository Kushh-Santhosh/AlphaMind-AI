import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNavbar } from "@/components/layout/TopNavbar";
import { CommandPalette } from "@/components/layout/CommandPalette";

export const metadata: Metadata = {
  title: "AlphaMind AI — Autonomous Institutional Research Gateway",
  description: "Institutional AI investment research, probabilistic forecasting, and quantitative analytics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-[#090d16] text-slate-100 min-h-screen flex">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <TopNavbar />
          <main className="flex-1 p-6 overflow-y-auto">{children}</main>
        </div>
        <CommandPalette />
      </body>
    </html>
  );
}
