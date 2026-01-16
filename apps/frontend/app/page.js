import Link from "next/link";

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto">
      {/* HERO */}
      <section className="rounded-3xl bg-white border border-emerald-100 p-10 text-center shadow-sm">
        <h1 className="text-4xl font-bold text-slate-900 mb-4">
          Welcome to <span className="text-emerald-600">ElectroMentor</span>
        </h1>

        <p className="text-slate-600 max-w-2xl mx-auto mb-10">
          Learn digital electronics interactively using AI-powered tutoring,
          PDF-based study materials, and practice quizzes — all in one place.
        </p>

        {/* ACTION BUTTONS */}
        <div className="grid gap-6 sm:grid-cols-3">
          <Link
            href="/chat"
            className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6 hover:bg-emerald-100 transition"
          >
            <div className="text-2xl mb-2">🤖</div>
            <h3 className="font-semibold text-lg">AI Tutor</h3>
            <p className="text-sm text-slate-600">
              Ask questions and get instant explanations.
            </p>
          </Link>

          <Link
            href="/quizzes"
            className="rounded-2xl border border-blue-200 bg-blue-50 p-6 hover:bg-blue-100 transition"
          >
            <div className="text-2xl mb-2">📝</div>
            <h3 className="font-semibold text-lg">Practice Quizzes</h3>
            <p className="text-sm text-slate-600">
              Test your understanding with quizzes.
            </p>
          </Link>

          <Link
            href="/resources"
            className="rounded-2xl border border-purple-200 bg-purple-50 p-6 hover:bg-purple-100 transition"
          >
            <div className="text-2xl mb-2">📘</div>
            <h3 className="font-semibold text-lg">Learning Resources</h3>
            <p className="text-sm text-slate-600">
              Read PDFs and chat alongside them.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}
