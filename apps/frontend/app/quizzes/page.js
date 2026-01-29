"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const DIFFICULTIES = ["easy", "medium", "hard"];

export default function QuizzesPage() {
  const router = useRouter();

  const [topics, setTopics] = useState([]);
  const [difficulty, setDifficulty] = useState("easy");

  // Fetch all PDFs as quiz topics
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/pdfs`)
      .then((res) => res.json())
      .then((data) => setTopics(data))
      .catch(console.error);
  }, []);

  // ✅ ONLY navigate — do NOT fetch quiz here
  const startQuiz = (title) => {
    router.push(
      `/quizzes/${encodeURIComponent(title)}?difficulty=${difficulty}`
    );
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="text-center">
        <h1 className="text-2xl font-semibold text-slate-900 mb-2">
          Practice Quizzes
        </h1>
        <p className="text-sm text-slate-500 max-w-2xl mx-auto">
          All quizzes are generated directly from your study PDFs using AI.
          Select a difficulty level and start practicing.
        </p>
      </section>

      {/* Difficulty Selector */}
      <section className="flex justify-center gap-3">
        {DIFFICULTIES.map((d) => (
          <button
            key={d}
            onClick={() => setDifficulty(d)}
            className={`rounded-full px-4 py-1.5 text-xs font-semibold capitalize border
              ${
                difficulty === d
                  ? "bg-emerald-600 text-white border-emerald-600"
                  : "bg-white text-slate-600 border-slate-200 hover:border-emerald-400"
              }`}
          >
            {d}
          </button>
        ))}
      </section>

      {/* Quiz Cards */}
      <section className="grid gap-4 md:grid-cols-3">
        {topics.map((t) => (
          <article
            key={t.id}
            className="rounded-2xl border border-emerald-50 bg-white px-5 py-5 shadow-sm flex flex-col justify-between"
          >
            <div className="space-y-2 text-xs">
              <span className="text-[11px] text-emerald-600 font-medium uppercase">
                {t.category}
              </span>

              <h2 className="text-sm font-semibold text-slate-900">
                {t.title}
              </h2>

              <p className="text-[11px] text-slate-500">
                AI-generated quiz based strictly on this PDF.
              </p>

              <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500">
                <span>Difficulty</span>
                <span className="capitalize font-semibold text-emerald-600">
                  {difficulty}
                </span>
              </div>
            </div>

            <button
              onClick={() => startQuiz(t.title)}
              className="mt-4 w-full rounded-full bg-emerald-600 px-4 py-2 text-xs font-semibold text-white hover:bg-emerald-700"
            >
              Start Quiz
            </button>
          </article>
        ))}
      </section>
    </div>
  );
}
