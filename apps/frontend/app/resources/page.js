"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function ResourcesPage() {
  const router = useRouter();
  const [pdfs, setPdfs] = useState([]);
  const [loading, setLoading] = useState(true);

  /* ---------------- LOAD PDFs ---------------- */
  useEffect(() => {
    async function loadPdfs() {
      try {
        const res = await fetch(`${API_BASE}/pdfs`);
        const data = await res.json();
        setPdfs(data);
      } catch (err) {
        console.error("Failed to load PDFs", err);
      } finally {
        setLoading(false);
      }
    }

    loadPdfs();
  }, []);

  /* ---------------- UI ---------------- */
  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <h1 className="text-2xl font-bold mb-2">📚 Learning Resources</h1>
      <p className="text-sm text-slate-500 mb-6">
        Select a PDF to read and chat with the AI tutor.
      </p>

      {loading && (
        <div className="text-slate-500 text-sm">Loading PDFs…</div>
      )}

      {!loading && pdfs.length === 0 && (
        <div className="text-slate-500 text-sm">
          No PDFs found in the knowledge base.
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {pdfs.map((pdf) => (
          <button
            key={pdf.id}
            onClick={() => router.push(`/study?pdf=${pdf.id}`)}
            className="group rounded-xl border bg-white p-4 text-left shadow-sm
                       hover:shadow-md hover:border-emerald-400 transition"
          >
            <h3 className="font-semibold text-slate-900 group-hover:text-emerald-700">
              {pdf.title}
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              {pdf.category}
            </p>
            <div className="mt-3 text-xs text-emerald-600 font-semibold">
              Open & Study →
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
