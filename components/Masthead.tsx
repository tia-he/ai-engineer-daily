"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Brief" },
  { href: "/search", label: "Search" },
];

export default function Masthead() {
  const pathname = usePathname();

  return (
    <header className="chrome-grid sticky top-0 z-50 border-b border-white/10 bg-chrome/95 text-chrome-ink backdrop-blur-md">
      <div className="mx-auto flex w-full max-w-3xl items-center justify-between gap-6 px-6 py-4">
        <Link
          href="/"
          className="text-sm font-semibold tracking-tight text-chrome-ink transition-colors hover:text-chrome-ink/70"
        >
          AI Engineer Daily
        </Link>

        <nav className="flex items-center gap-1">
          {NAV.map((item) => {
            const isActive =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={isActive ? "page" : undefined}
                className={`rounded-full px-3 py-1.5 font-mono text-xs uppercase tracking-[0.14em] transition-colors ${
                  isActive
                    ? "bg-white/15 text-chrome-ink"
                    : "text-chrome-ink/60 hover:text-chrome-ink"
                }`}
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
