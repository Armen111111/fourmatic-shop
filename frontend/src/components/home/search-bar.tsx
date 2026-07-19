"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Search, ArrowRight } from "lucide-react";
import { useUIStore } from "@/store/ui";

export function SearchBar() {
  const [value, setValue] = useState("");
  const [focused, setFocused] = useState(false);
  const setSearch = useUIStore((s) => s.setSearch);
  const setTab = useUIStore((s) => s.setTab);

  const submit = () => {
    if (!value.trim()) return;
    setSearch(value.trim());
    setTab("catalog");
  };

  return (
    <section className="mx-5 mt-6">
      <motion.div
        animate={{
          boxShadow: focused
            ? "0 0 0 3px rgba(216,214,210,0.14), inset 0 1px 0 rgba(255,255,255,0.05)"
            : "inset 0 1px 0 rgba(255,255,255,0.05), 0 16px 34px -26px rgba(0,0,0,0.9)",
          borderColor: focused ? "var(--border-strong)" : "var(--border)",
        }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
        className="flex items-center gap-2.5 rounded-full border bg-card py-1.5 pl-5 pr-1.5"
      >
        <Search className="h-[18px] w-[18px] shrink-0 text-faint" strokeWidth={1.8} />
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="Введите VIN, артикул или название детали"
          className="min-w-0 flex-1 bg-transparent py-3.5 text-sm text-foreground placeholder:text-faint focus:outline-none"
        />
        <button
          onClick={submit}
          aria-label="Найти"
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground transition-transform active:scale-90"
        >
          <ArrowRight className="h-[18px] w-[18px]" strokeWidth={2} />
        </button>
      </motion.div>
    </section>
  );
}
