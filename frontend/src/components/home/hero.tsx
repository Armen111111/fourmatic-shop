"use client";

import { motion } from "framer-motion";

const ease = [0.16, 1, 0.3, 1] as const;

export function Hero() {
  return (
    <section className="relative overflow-hidden px-5 pb-2 pt-8">
      <div
        aria-hidden
        className="pointer-events-none absolute right-5 top-1 h-20 w-20 opacity-60"
        style={{
          backgroundImage:
            "radial-gradient(rgba(255,255,255,0.14) 1.4px, transparent 1.4px)",
          backgroundSize: "13px 13px",
        }}
      />
      <motion.span
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease, delay: 0.05 }}
        className="relative z-10 inline-block rounded-full border border-border-strong bg-card px-3.5 py-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-primary"
      >
        Mercedes&#8209;Benz · Официальный подбор запчастей
      </motion.span>

      <motion.h1
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease, delay: 0.14 }}
        className="relative z-10 mt-4 max-w-[92%] text-[26px] font-bold leading-[1.22] tracking-tight text-foreground"
      >
        Подбор оригинальных деталей и качественных аналогов
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease, delay: 0.24 }}
        className="relative z-10 mt-3 max-w-[88%] text-[13.5px] leading-relaxed text-muted-foreground"
      >
        По VIN и OEM-номеру, с проверкой совместимости с вашим автомобилем.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, scaleX: 0 }}
        animate={{ opacity: 1, scaleX: 1 }}
        transition={{ duration: 0.6, ease, delay: 0.36 }}
        className="relative z-10 mt-6 h-px origin-left bg-gradient-to-r from-border-strong to-transparent"
      />
    </section>
  );
}
