"use client";

import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I am your electronics tutor. Ask me anything about the PDFs in your study material.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🔹 Auto-scroll reference
  const bottomRef = useRef(null);

  // 🔹 Scroll whenever messages or loading state changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const url = new URL("/rag/answer", API_BASE);
      url.searchParams.set("query", userMessage.content);

      const res = await fetch(url.toString());
      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer || "(No answer returned)",
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      console.error(err);
      setError(
        "Something went wrong talking to the tutor. Check that the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] max-h-[760px]">
      <h2 className="text-2xl font-semibold mb-4">AI Tutor</h2>

      {/* CHAT WINDOW */}
      <div className="flex-1 overflow-y-auto rounded-xl border border-slate-300 bg-slate-200/70 p-4 space-y-3">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={
              "rounded-lg px-4 py-3 text-sm max-w-[85%] " +
              (m.role === "user"
                ? "ml-auto bg-cyan-500 text-slate-950"
                : "mr-auto bg-slate-800 text-slate-50")
            }
          >
            {/* MESSAGE CONTENT */}
            {m.role === "assistant" ? (
              <div className="prose prose-invert prose-sm max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {m.content}
                </ReactMarkdown>
              </div>
            ) : (
              <div>{m.content}</div>
            )}

            {/* SOURCES */}
            {m.sources && m.sources.length > 0 && (
              <div className="mt-3 text-[10px] text-slate-400 border-t border-slate-600 pt-1">
                Sources:{" "}
                {m.sources
                  .map((s, i) => s.title || s.pdf || `source-${i}`)
                  .join(", ")}
              </div>
            )}
          </div>
        ))}

        {/* LOADING MESSAGE */}
        {loading && (
          <div className="mr-auto rounded-lg px-4 py-2 text-sm bg-slate-800 text-slate-300">
            Thinking based on knowledge given 
          </div>
        )}

        {/* ERROR */}
        {error && (
          <div className="mt-2 text-xs text-red-500">{error}</div>
        )}

        {/* 🔹 Auto-scroll anchor */}
        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <form onSubmit={sendMessage} className="mt-4 flex gap-2">
        <input
          className="flex-1 rounded-lg border border-slate-400 bg-slate-100 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500"
          placeholder="Ask about logic gates, flip-flops, counters..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-cyan-500 px-5 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-60"
        >
          {loading ? "Sending…" : "Send"}
        </button>
      </form>
    </div>
  );
}
