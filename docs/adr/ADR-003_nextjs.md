# ADR-003: Next.js 14 App Router for Frontend Presentation

## Context
The platform requires a modern, responsive, high-performance web interface supporting 13 interactive dashboards, dynamic dark-mode styling, real-time TradingView financial charts, and Server-Sent Events (SSE) log streaming.

## Decision
We decide to adopt **Next.js 14+ (App Router)** with React 18, TypeScript, TailwindCSS, and `shadcn/ui`.

## Alternatives Considered
1. **Single Page App (Vite + React)**: Rejected due to lack of built-in server-side rendering (SSR), SEO capabilities, and static page generation.
2. **Vue / Nuxt.js**: Rejected due to developer team familiarity with React/TypeScript and `shadcn/ui` ecosystem availability.

## Pros
- **App Router Architecture**: Flexible nested layouts, Server Components for high performance, and Client Components for interactive financial charts.
- **TypeScript First**: Strict type safety preventing runtime UI null errors.
- **TailwindCSS & `shadcn/ui`**: High-aesthetic dark-mode financial UI design with pre-built accessible primitives.

## Cons
- Next.js App Router learning curve for complex streaming state management.

## Consequences
All frontend code MUST be structured in `apps/frontend` using Next.js 14 App Router standards and TypeScript strict mode.
