"use client";

import { Logo } from "@/components/brand/logo";

export function Header() {
  return (
    <header className="sticky top-2 z-30 mx-3 mt-2 flex items-center justify-between rounded-full border border-border-strong bg-card-elevated/70 px-4 py-3 shadow-[0_12px_32px_-16px_rgba(0,0,0,0.6),inset_0_1px_0_rgba(255,255,255,0.06)] backdrop-blur-2xl">
      <Logo />
    </header>
  );
}
