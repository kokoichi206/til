"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "周回路（距離計算）" },
  { href: "/training", label: "トレーニング計画" },
];

/** 全ページ共通のヘッダーナビ。現在ページをハイライトする。 */
export function SiteNav(): React.JSX.Element {
  const pathname = usePathname();
  return (
    <nav className="sticky top-0 z-20 flex h-12 shrink-0 items-center gap-1 border-b border-slate-200 bg-white/95 px-4 backdrop-blur">
      <span className="mr-3 text-sm font-bold text-slate-900">Running Planner</span>
      {LINKS.map((l) => {
        const active = l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
        return (
          <Link
            key={l.href}
            href={l.href}
            aria-current={active ? "page" : undefined}
            className={`rounded px-3 py-1.5 text-sm ${
              active
                ? "bg-blue-600 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            {l.label}
          </Link>
        );
      })}
    </nav>
  );
}
