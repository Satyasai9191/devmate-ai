"use client";

import { useEffect, useState } from "react";

type HealthResponse = {
  status: string;
  service?: string;
  version?: string;
};

export default function Home() {
  const [backendStatus, setBackendStatus] =
    useState<"checking" | "online" | "offline">("checking");

  const [health, setHealth] =
    useState<HealthResponse | null>(null);

  useEffect(() => {
    async function checkBackend() {
      try {
        const response = await fetch(
          "http://localhost:8000/api/health"
        );

        if (!response.ok) {
          throw new Error("Backend unavailable");
        }

        const data = await response.json();

        setHealth(data);
        setBackendStatus("online");
      } catch {
        setBackendStatus("offline");
      }
    }

    checkBackend();
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-12">
          <div className="mb-4 inline-flex rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-300">
            DevMate AI · Stage 0
          </div>

          <h1 className="text-5xl font-bold tracking-tight">
            Your local AI agent platform.
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-slate-400">
            Production-oriented foundation for an AI agent
            running locally on your Windows machine.
          </p>
        </header>

        <section className="grid gap-6 md:grid-cols-3">
          <StatusCard
            title="Frontend"
            status="Online"
            description="Next.js + TypeScript"
          />

          <StatusCard
            title="Backend"
            status={
              backendStatus === "online"
                ? "Online"
                : backendStatus === "offline"
                  ? "Offline"
                  : "Checking..."
            }
            description="FastAPI"
          />

          <StatusCard
            title="Database"
            status="Ready"
            description="PostgreSQL + pgvector"
          />
        </section>

        <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-8">
          <h2 className="text-2xl font-semibold">
            System status
          </h2>

          <div className="mt-6 rounded-xl bg-slate-950 p-5">
            <pre className="overflow-auto text-sm text-slate-300">
              {JSON.stringify(
                health ?? {
                  status: backendStatus,
                },
                null,
                2
              )}
            </pre>
          </div>
        </section>

        <section className="mt-8 grid gap-6 md:grid-cols-2">
          <Feature
            title="Local AI"
            description="Ollama will provide local model inference without a paid AI API."
          />

          <Feature
            title="Agent Runtime"
            description="LangGraph will manage agent state, tools and execution flow."
          />

          <Feature
            title="Knowledge"
            description="PostgreSQL and pgvector will provide local RAG infrastructure."
          />

          <Feature
            title="Production"
            description="Testing, Docker, CI/CD, monitoring and observability will be added incrementally."
          />
        </section>
      </div>
    </main>
  );
}


function StatusCard({
  title,
  status,
  description,
}: {
  title: string;
  status: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{title}</h3>

        <span className="rounded-full bg-emerald-950 px-3 py-1 text-xs text-emerald-400">
          {status}
        </span>
      </div>

      <p className="mt-3 text-sm text-slate-400">
        {description}
      </p>
    </div>
  );
}


function Feature({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-400">
        {description}
      </p>
    </div>
  );
}