"use client";

import { AuthProvider } from "../components/AuthProvider";
import { TopBar } from "../components/TopBar";

export default function ClientLayout({ children }) {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <TopBar />
        <main className="flex-1 px-8 py-6 max-w-6xl mx-auto">{children}</main>
      </div>
    </AuthProvider>
  );
}
