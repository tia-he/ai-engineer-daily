import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import Masthead from "../components/Masthead";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "AI Engineer Daily",
    template: "%s · AI Engineer Daily",
  },
  description:
    "A daily brief on AI and software engineering, read in a few minutes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      // Next 16 no longer forces scroll-behavior to auto during navigation;
      // this opts back in so route changes still land at the top instantly.
      data-scroll-behavior="smooth"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col bg-surface text-ink">
        <Masthead />

        <div className="flex-1">{children}</div>

        <footer className="border-t border-rule">
          <div className="mx-auto w-full max-w-3xl px-6 py-8">
            <p className="font-mono text-xs uppercase tracking-[0.14em] text-ink-faint">
              Ingested from OpenAI, Google AI, Hugging Face, Mistral AI, and
              DeepMind
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
