"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter, useParams } from "next/navigation";

export default function QuizResultPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const params = useParams();

  const pdfTitle = decodeURIComponent(params.title);

  const score = Number(searchParams.get("score"));
  const name = searchParams.get("name");
  const semester = searchParams.get("semester");
  const year = searchParams.get("year");
  const roll = searchParams.get("roll");

  const [review, setReview] = useState(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("quizReview");
    if (stored) {
      setReview(JSON.parse(stored));
    }
  }, []);

  if (!review) {
    return <p className="text-center mt-20">Loading review…</p>;
  }

  return (
    <div className="max-w-6xl mx-auto mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
      
      {/* ================= LEFT PANEL ================= */}
      <div className="space-y-4 border rounded-lg p-6 h-fit">
        <h1 className="text-xl font-semibold">Quiz Completed 🎉</h1>

        <p className="text-sm text-slate-500">
          PDF: <strong>{pdfTitle}</strong>
        </p>

        <div className="pt-2 space-y-1 text-sm">
          <p>Name: <strong>{name}</strong></p>
          <p>Roll Number: <strong>{roll}</strong></p>
          <p>Year: <strong>{year}</strong></p>
          <p>Semester: <strong>{semester}</strong></p>
        </div>

        <div className="pt-4 space-y-1">
          <p className="font-semibold">
            Score: {score} / {review.total}
          </p>
          <p>
            Accuracy:{" "}
            {Math.round((score / review.total) * 100)}%
          </p>
        </div>

        <div className="flex gap-3 pt-4">
          <button
            onClick={() => router.push("/quizzes")}
            className="px-4 py-2 rounded-lg border"
          >
            Back to Quizzes
          </button>

          <button
            onClick={() => router.back()}
            className="px-4 py-2 rounded-lg bg-emerald-600 text-white"
          >
            Retry Quiz
          </button>
        </div>
      </div>

      {/* ================= RIGHT PANEL (SCROLLABLE REVIEW) ================= */}
      <div className="border rounded-lg p-4 max-h-[70vh] overflow-y-auto space-y-4">
        <h2 className="text-lg font-semibold sticky top-0 bg-white pb-2">
          Answer Review
        </h2>

        {review.questions.map((q, index) => {
          const isCorrect =
            q.selectedAnswer === q.correctAnswer;

          return (
            <div
              key={index}
              className={`border rounded-lg p-4 space-y-2 ${
                isCorrect
                  ? "border-emerald-500 bg-emerald-50"
                  : "border-red-500 bg-red-50"
              }`}
            >
              <p className="font-semibold">
                Q{index + 1}. {q.question}
              </p>

              <p className="text-sm">
                Your Answer:{" "}
                <strong>
                  {q.selectedAnswer || "Not Answered"}
                </strong>
              </p>

              {!isCorrect && (
                <p className="text-sm">
                  Correct Answer:{" "}
                  <strong>{q.correctAnswer}</strong>
                </p>
              )}

              <p className="text-sm font-semibold">
                {isCorrect ? "✅ Correct" : "❌ Wrong"}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
