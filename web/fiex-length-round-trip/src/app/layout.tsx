import type { Metadata } from "next";

import { SiteNav } from "@/client/components/SiteNav";

import "./globals.css";

export const metadata: Metadata = {
  title: "Running Planner",
  description:
    "目標距離の周回路生成 + レースまでのトレーニング計画（OpenStreetMap / Lewis & Corcoran 2024）。",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>): React.JSX.Element {
  return (
    <html lang="ja">
      <body>
        <SiteNav />
        <main>{children}</main>
      </body>
    </html>
  );
}
