"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams, useRouter } from "next/navigation";

const TOTAL_QUESTIONS = 20;
const BATCH_SIZE = 2;

const TOTAL_TIME_BY_DIFFICULTY = {
  easy: 5 * 60,
  medium: 8 * 60,
  hard: 10 * 60,
};

export default function QuizPlayPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const pdfTitle = decodeURIComponent(params.title);
  const difficulty = searchParams.get("difficulty") || "easy";

  const TOTAL_TIME =
    TOTAL_TIME_BY_DIFFICULTY[difficulty] || 5 * 60;

  const [name, setName] = useState("");
  const [roll, setRoll] = useState("");
  const [semester, setSemester] = useState("");
  const [year, setYear] = useState("");


  const [started, setStarted] = useState(false);

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const [batch, setBatch] = useState(1);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(TOTAL_TIME);
  const [loading, setLoading] = useState(false);

  /* ================= TIMER ================= */

  useEffect(() => {
    if (!started) return;

    if (timeLeft <= 0) {
      submitQuiz();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((t) => t - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [started, timeLeft]);

  const formatTime = (sec) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  /* ================= DATA ================= */

  const loadBatch = async (batchNo) => {
    if (loading) return;
    setLoading(true);

    const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/quizzes/quiz` +
      `?pdf_title=${encodeURIComponent(pdfTitle)}` +
      `&difficulty=${difficulty}` +
      `&batch=${batchNo}` +
      `&batch_size=${BATCH_SIZE}`
  );

    const data = await res.json();
    setQuestions((prev) => [...prev, ...(data.questions || [])]);
    setLoading(false);
  };

  const startQuiz = async () => {
    setStarted(true);
    await loadBatch(1);
    await loadBatch(2);
    setBatch(2);
  };

  /* ================= QUIZ LOGIC ================= */

  const selectAnswer = (option) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [currentIndex]: option,
    }));
  };

  const nextQuestion = () => {
    const nextIndex = currentIndex + 1;
    setCurrentIndex(nextIndex);

    if (
      nextIndex % BATCH_SIZE === 1 &&
      questions.length < TOTAL_QUESTIONS
    ) {
      const nextBatch = batch + 1;
      setBatch(nextBatch);
      loadBatch(nextBatch);
    }
  };

  const prevQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1);
    }
  };

  const submitQuiz = () => {
    let score = 0;

    const reviewQuestions = questions.map((q, i) => {
      const selected = selectedAnswers[i] || null;
      const correct = q.answer;
      if (selected === correct) score++;

      return {
        question: q.question,
        options: q.options,
        correctAnswer: correct,
        selectedAnswer: selected,
      };
    });

    sessionStorage.setItem(
      "quizReview",
      JSON.stringify({
        pdfTitle,
        name,
        semester,
        year,
        roll,
        score,
        total: questions.length,
        questions: reviewQuestions,
      })
    );

    router.push(
      `/quizzes/${encodeURIComponent(
        pdfTitle
      )}/result?score=${score}&name=${name}&semester=${semester}&year=${year}&roll=${roll}`
    );
  };

  /* ================= UI ================= */

  if (!started) {
    return (
      <div className="max-w-md mx-auto mt-20 text-center space-y-4">
        <h1 className="text-xl font-semibold">Start Quiz</h1>
        <p className="text-sm text-slate-500">{pdfTitle}</p>

        <input
          className="w-full border rounded-lg px-3 py-2 text-sm"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="w-full border rounded-lg px-3 py-2 text-sm"
          placeholder="Enter roll number"
          value={roll}
          onChange={(e) => setRoll(e.target.value)}
        />
        <input
          className="w-full border rounded-lg px-3 py-2 text-sm"
          placeholder="Enter semester"
          value={semester}
          onChange={(e) => setSemester(e.target.value)}
        />

        <input
          className="w-full border rounded-lg px-3 py-2 text-sm"
          placeholder="Enter year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />

        

        <button
          disabled={!name || !semester || !year || !roll}
          onClick={startQuiz}
          className="w-full bg-emerald-600 text-white rounded-lg py-2 text-sm font-semibold"
        >
          Start Quiz
        </button>
      </div>
    );
  }

  const q = questions[currentIndex];
  if (!q) {
    return <p className="text-center mt-20">Loading questions…</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-16 space-y-6">
      <div className="flex justify-between text-sm text-slate-600">
        <span>
          Question {currentIndex + 1} / {TOTAL_QUESTIONS}
        </span>
        <span className="font-semibold text-emerald-600">
          ⏱ {formatTime(timeLeft)}
        </span>
      </div>

      <h2 className="text-lg font-semibold">{q.question}</h2>

      <div className="grid gap-3">
        {q.options.map((opt) => (
          <button
            key={opt}
            onClick={() => selectAnswer(opt)}
            className={`border rounded-lg px-4 py-2 text-left ${
              selectedAnswers[currentIndex] === opt
                ? "bg-emerald-100 border-emerald-500"
                : "hover:bg-emerald-50"
            }`}
          >
            {opt}
          </button>
        ))}
      </div>

      <div className="flex justify-between pt-4">
        <button
          onClick={prevQuestion}
          disabled={currentIndex === 0}
          className="px-4 py-2 text-sm rounded-lg border disabled:opacity-50"
        >
          Previous
        </button>

        {currentIndex === TOTAL_QUESTIONS - 1 ? (
          <button
            onClick={submitQuiz}
            className="px-6 py-2 text-sm rounded-lg bg-emerald-600 text-white"
          >
            Final Submit
          </button>
        ) : (
          <button
            onClick={nextQuestion}
            className="px-6 py-2 text-sm rounded-lg bg-emerald-600 text-white"
          >
            Next
          </button>
        )}
      </div>
    </div>
  );
}
