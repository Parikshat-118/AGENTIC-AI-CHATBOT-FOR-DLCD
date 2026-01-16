import "./globals.css";
import { TopBar } from "../components/TopBar";

export const metadata = {
  title: "ElectroMentor",
  description: "Digital Electronics Assistant",
  icons: {
    icon: "/icons/favicon.png",
    shortcut: "/icons/favicon.png",
    apple: "/icons/favicon.png",
  },
};


export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-[#f7fbf9] text-slate-900">
        <TopBar />
        <main className="px-6 py-6">{children}</main>
      </body>
    </html>
  );
}
