"use client";

import { useEffect, useState, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import 'katex/dist/katex.min.css';
const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function StudyPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const pdfIdFromUrl = Number(searchParams.get("pdf"));

  const [pdfs, setPdfs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");
  const [chatHistories, setChatHistories] = useState({});

  // 🔥 Mobile controls
  const [showPdfNav, setShowPdfNav] = useState(false);
  const [showChat, setShowChat] = useState(false);

  const chatRef = useRef(null);

  /* ================= LOAD PDFs ================= */

  useEffect(() => {
    async function loadPdfs() {
      const res = await fetch(`${API_BASE}/pdfs`);
      const data = await res.json();
      const list = Array.isArray(data) ? data : [];
      setPdfs(list);

      if (list.length > 0) {
        setSelected(list.find(p => p.id === pdfIdFromUrl) || list[0]);
      }
    }
    loadPdfs();
  }, [pdfIdFromUrl]);

  const handlePdfSelect = (pdf) => {
    setSelected(pdf);
    setShowPdfNav(false); // close mobile drawer
    router.push(`/study?pdf=${pdf.id}`, { scroll: false });
  };

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [chatHistories, loading, selected]);

  const currentMessages = selected ? chatHistories[selected.id] || [] : [];
  useEffect(() => {
  if (!selected) return;

  setChatHistories((prev) => {
    if (prev[selected.id]?.length) return prev;

    return {
      ...prev,
      [selected.id]: [
        {
          role: "assistant",
          content: `👋 Hi! I’m your AI Tutor.\n\nAsk me anything from **${selected.title}**.\n\nHow can I help you? 😊`,
        },
      ],
    };
  });
}, [selected]);


  /* ================= SEND MESSAGE ================= */
async function sendMessage(e) {
  e.preventDefault();
  if (!input.trim() || !selected || loading) return;

  const userContent = input.trim();
  const pdfId = selected.id;

  // 1️⃣ Add user message
  setChatHistories(prev => ({
    ...prev,
    [pdfId]: [...(prev[pdfId] || []), { role: "user", content: userContent }],
  }));

  setInput("");
  setLoading(true);

  // 2️⃣ Add "Thinking…" placeholder
  setChatHistories(prev => ({
    ...prev,
    [pdfId]: [
      ...(prev[pdfId] || []),
      { role: "assistant", content: "🤖 Thinking…" },
    ],
  }));

  try {
    const queryParams = new URLSearchParams({
      query: userContent,
      pdf_id: pdfId.toString(),
      pdf_title: selected.title,
    });

    const res = await fetch(`${API_BASE}/rag/pdf-answer?${queryParams}`);
    const data = await res.json();

    // 3️⃣ Replace "Thinking…" with real answer
    setChatHistories(prev => ({
      ...prev,
      [pdfId]: [
        ...(prev[pdfId] || []).slice(0, -1),
        { role: "assistant", content: data.answer || "No relevant info found." },
      ],
    }));
  } catch {
    setChatHistories(prev => ({
      ...prev,
      [pdfId]: [
        ...(prev[pdfId] || []).slice(0, -1),
        { role: "assistant", content: "⚠️ Unable to connect to AI Tutor." },
      ],
    }));
  } finally {
    setLoading(false);
  }
}

 

  /* ================= UI ================= */

  return (
    <div className="bg-slate-50 p-2 md:p-4 relative">

      {/* 🔥 MOBILE TOP BAR */}
      <div className="md:hidden flex items-center justify-between bg-white p-3 rounded-xl shadow mb-2">
        <button onClick={() => setShowPdfNav(true)} className="text-xl">☰</button>
        <span className="font-semibold truncate">{selected?.title}</span>
        <button onClick={() => setShowChat(true)}>🤖</button>
      </div>

      <div className="md:grid md:grid-cols-[280px_1fr_380px] gap-4 min-h-[100dvh] md:h-[calc(100vh-140px)]">

        {/* LEFT PDF LIST (DESKTOP) */}
        <aside className="hidden md:flex bg-white rounded-2xl border shadow-sm flex-col overflow-hidden">
          <div className="p-4 border-b font-bold">📚 Study Materials</div>
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {pdfs.map(pdf => (
              <button
                key={pdf.id}
                onClick={() => handlePdfSelect(pdf)}
                className={`w-full text-left rounded-xl px-4 py-3 border ${
                  selected?.id === pdf.id
                    ? "bg-emerald-50 border-emerald-500"
                    : "hover:bg-slate-50"
                }`}
              >
                <p className="text-xs font-semibold truncate">{pdf.title}</p>
                <span className="text-[10px] text-slate-400 uppercase">
                  {pdf.category}
                </span>
              </button>
            ))}
          </div>
        </aside>

        {/* CENTER PDF */}
        <section className="bg-white rounded-2xl border shadow-sm flex flex-col overflow-hidden min-h-[70vh]">
          <header className="hidden md:block px-4 py-2 border-b font-bold truncate">
            {selected?.title}
          </header>

          <div className="flex-1 bg-slate-200 overflow-y-auto md:overflow-hidden">
            {selected && (
              <iframe
  src={`${selected.url}#toolbar=0`}
  className="w-full h-[calc(100dvh-120px)] md:h-full border-none"
  title={selected.title}
/>

            )}
          </div>
        </section>

        {/* CHAT (DESKTOP) */}
        <aside className="hidden md:flex bg-white rounded-2xl border shadow-sm flex-col overflow-hidden">
          <div className="p-4 border-b bg-emerald-600 text-white font-bold">
            🤖 AI Study Tutor
          </div>

          <div ref={chatRef} className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
            {currentMessages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
  className={`max-w-[95%] px-4 py-3 rounded-xl text-sm leading-7 break-all overflow-x-hidden ${
    m.role === "user"
      ? "bg-emerald-600 text-white"
      : "bg-white border max-h-[65vh] overflow-y-auto"
  }`}
>



                  <ReactMarkdown
  remarkPlugins={[remarkGfm]}
  components={{
    p: ({ node, ...props }) => (
      <p className="mb-3 text-sm break-all" {...props} />
    ),
    li: ({ node, ...props }) => (
      <li className="ml-4 mb-2 list-disc break-all" {...props} />
    ),
    strong: ({ node, ...props }) => (
      <strong className="font-semibold" {...props} />
    ),
    code: ({ node, ...props }) => (
      <code className="bg-slate-100 px-1 rounded break-all" {...props} />
    ),
  }}
>
  {m.content}
</ReactMarkdown>


                </div>
              </div>
            ))}
            {loading && <div className="text-xs text-slate-500">AI Tutor is reading…</div>}
          </div>

          <form onSubmit={sendMessage} className="p-3 border-t">
            <div className="flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 border rounded-lg px-3 py-2 text-sm"
                placeholder="Ask a question…"
              />
              <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm">
                SEND
              </button>
            </div>
          </form>
        </aside>
      </div>

      {/* 🔥 MOBILE PDF DRAWER */}
      {showPdfNav && (
        <div className="fixed inset-0 bg-black/40 z-40 md:hidden">
          <div className="absolute left-0 top-0 h-full w-4/5 bg-white p-4 overflow-y-auto">
            <button onClick={() => setShowPdfNav(false)} className="mb-4">❌</button>
            {pdfs.map(pdf => (
              <button
                key={pdf.id}
                onClick={() => handlePdfSelect(pdf)}
                className="block w-full text-left py-3 border-b"
              >
                {pdf.title}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 🔥 MOBILE CHAT DRAWER */}
      {/* 🔥 MOBILE CHAT DRAWER */}
{showChat && (
  <div className="fixed inset-0 bg-black/60 z-50 md:hidden flex justify-end">
    {/* Overlay Click to Close */}
    <div className="absolute inset-0" onClick={() => setShowChat(false)} />
    
    <div className="relative h-full w-[85%] bg-slate-50 shadow-2xl flex flex-col animate-in slide-in-from-right duration-300">
      {/* Mobile Header */}
      <div className="p-4 bg-emerald-700 text-white flex items-center justify-between shadow-md">
        <div className="flex items-center gap-2">
          <span className="text-lg">🤖</span>
          <div>
            <h3 className="font-bold text-sm leading-none">AI Study Tutor</h3>
            <p className="text-[10px] text-emerald-100 mt-1">Online & ready to help</p>
          </div>
        </div>
        <button 
          onClick={() => setShowChat(false)}
          className="p-2 hover:bg-emerald-600 rounded-full transition-colors"
        >
          <span className="text-xl">✕</span>
        </button>
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {currentMessages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[90%] px-4 py-3 rounded-2xl text-sm shadow-sm ${
                m.role === "user"
                  ? "bg-emerald-600 text-white rounded-tr-none"
                  : "bg-white border border-slate-200 text-slate-800 rounded-tl-none"
              }`}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
                components={{
                  p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                  ul: ({ node, ...props }) => <ul className="ml-4 list-disc space-y-1 my-2" {...props} />,
                  li: ({ node, ...props }) => <li className="break-words" {...props} />,
                  strong: ({ node, ...props }) => <strong className="font-bold text-emerald-900" {...props} />,
                  code: ({ node, ...props }) => <code className="bg-slate-100 px-1 rounded text-xs font-mono" {...props} />,
                }}
              >
                {m.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 px-4 py-2 rounded-2xl rounded-tl-none shadow-sm text-xs text-slate-400 italic flex items-center gap-2">
              <span className="animate-bounce">●</span>
              <span>AI is thinking...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <form
        onSubmit={sendMessage}
        className="p-4 bg-white border-t border-slate-200 pb-safe-offset-4"
      >
        <div className="flex gap-2 items-center bg-slate-100 p-1 rounded-xl border border-slate-200 focus-within:border-emerald-500 focus-within:ring-1 focus-within:ring-emerald-500 transition-all">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your tutor..."
            className="flex-1 bg-transparent border-none focus:ring-0 px-3 py-2 text-sm"
            disabled={!selected || loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 text-white p-2 rounded-lg transition-colors"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
              <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
            </svg>
          </button>
        </div>
      </form>
    </div>
  </div>
)}
    </div>
  );
}
