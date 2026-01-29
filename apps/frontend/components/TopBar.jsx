"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/chat", label: "AI Tutor" },
  { href: "/quizzes", label: "Practice Quizzes" },
  { href: "/resources", label: "Learning Resources" },
];

export function TopBar() {
  const pathname = usePathname();

  return (
    <header className="border-b border-emerald-100 bg-[#f7fbf9] px-4 py-3">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">

        {/* ✅ CLICKABLE LOGO WITH ICON */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="h-9 w-9 flex items-center justify-center rounded-xl border bg-white overflow-hidden">
            <Image
              src="/icons/electromentor.png"
              alt="ElectroMentor Logo"
              width={36}
              height={36}
              className="object-contain"
              priority
            />
          </div>
          <div>
            <div className="text-sm font-semibold group-hover:text-emerald-700 transition">
              ElectroMentor
            </div>
            <div className="text-[11px] text-slate-500">
              Digital Electronics Assistant
            </div>
          </div>
        </Link>

        {/* Nav */}
        <nav className="flex flex-wrap gap-4 text-sm">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={
                  active
                    ? "text-emerald-700 font-semibold border-b-2 border-emerald-500"
                    : "text-slate-600 hover:text-emerald-600 transition"
                }
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
