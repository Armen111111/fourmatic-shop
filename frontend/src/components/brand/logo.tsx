"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

/**
 * Original FOURMATIC mark — an engineering "tolerance frame": a rotated
 * square with a centered crosshair, evoking precision measurement rather
 * than any specific manufacturer emblem. Deliberately not a 3-pointed
 * star or any other automotive brand's registered mark.
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 32 32"
      className={cn("h-full w-full", className)}
      aria-hidden="true"
    >
      <rect
        x="8.5"
        y="8.5"
        width="15"
        height="15"
        rx="2"
        transform="rotate(45 16 16)"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
      />
      <path d="M16 12v8M12 16h8" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  );
}

export function Logo({ animated = true }: { animated?: boolean }) {
  const Wrap = animated ? motion.div : "div";
  const wrapProps = animated
    ? {
        initial: { opacity: 0, y: 6 },
        animate: { opacity: 1, y: 0 },
        transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] as const },
      }
    : {};

  return (
    <Wrap {...wrapProps} className="flex items-center gap-2.5">
      <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border border-primary/70 text-primary">
        <LogoMark className="h-4 w-4" />
      </span>
      <span className="flex flex-col leading-none">
        <span className="text-[15px] font-extrabold tracking-tight text-foreground">
          FOUR<span className="font-normal text-muted-foreground">MATIC</span>
        </span>
        <span className="mt-1 border-t border-border pt-1 text-[9px] font-semibold uppercase tracking-[0.14em] text-faint">
          Mercedes&#8209;Benz Parts
        </span>
      </span>
    </Wrap>
  );
}
