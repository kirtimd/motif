import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

type Health = { status: string; database: string };

function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: Health) => setHealth(data))
      .catch((err) => setError(err.message));
  }, []);

  const backendUp = health?.status === "ok";
  const dbUp = health?.database === "connected";

  return (
    <div className="min-h-screen w-full bg-neutral-950 text-neutral-100 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <h1 className="text-4xl font-bold tracking-tight mb-1">Motif</h1>
        <p className="text-neutral-400 mb-8">
          Capture anything interesting. Let AI connect the dots.
        </p>

        <div className="rounded-xl border border-neutral-800 bg-neutral-900 p-5 space-y-3">
          <p className="text-sm uppercase tracking-wide text-neutral-500">
            System status
          </p>

          {error ? (
            <StatusRow label="Backend" ok={false} detail={`unreachable (${error})`} />
          ) : !health ? (
            <p className="text-neutral-400 text-sm">Checking…</p>
          ) : (
            <>
              <StatusRow label="Backend API" ok={backendUp} detail={health.status} />
              <StatusRow label="Database" ok={dbUp} detail={health.database} />
            </>
          )}
        </div>

        <p className="text-xs text-neutral-600 mt-4">
          Phase 0 — end-to-end skeleton
        </p>
      </div>
    </div>
  );
}

function StatusRow({
  label,
  ok,
  detail,
}: {
  label: string;
  ok: boolean;
  detail: string;
}) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-neutral-200">{label}</span>
      <span className="flex items-center gap-2 text-sm">
        <span
          className={`h-2.5 w-2.5 rounded-full ${ok ? "bg-green-500" : "bg-red-500"}`}
        />
        <span className={ok ? "text-green-400" : "text-red-400"}>{detail}</span>
      </span>
    </div>
  );
}

export default App;
