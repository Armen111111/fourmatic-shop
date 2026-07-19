"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronRight } from "lucide-react";
import type { Product } from "@/lib/types";
import { CATALOG_GROUPS } from "@/lib/catalog-groups";
import { useUIStore } from "@/store/ui";
import { cn } from "@/lib/utils";

export function CatalogTree({ products }: { products: Product[] }) {
  const [openGroup, setOpenGroup] = useState<string | null>(CATALOG_GROUPS[0]?.name ?? null);
  const category = useUIStore((s) => s.category);
  const setCategory = useUIStore((s) => s.setCategory);

  const counts: Record<string, number> = {};
  for (const p of products) counts[p.category] = (counts[p.category] ?? 0) + 1;

  const groups = CATALOG_GROUPS.map((g) => ({
    name: g.name,
    categories: g.categories.filter((c) => counts[c]),
  })).filter((g) => g.categories.length);

  const known = new Set(CATALOG_GROUPS.flatMap((g) => g.categories));
  const other = Object.keys(counts).filter((c) => !known.has(c)).sort();
  if (other.length) groups.push({ name: "Дополнительное оборудование", categories: other });

  return (
    <section className="px-5 pt-6">
      <h3 className="mb-3 text-[17px] font-bold tracking-tight text-foreground">Каталог по системам</h3>
      <div className="flex flex-col gap-2">
        {groups.map((group) => {
          const total = group.categories.reduce((s, c) => s + (counts[c] ?? 0), 0);
          const isOpen = openGroup === group.name;
          return (
            <div
              key={group.name}
              className="overflow-hidden rounded-2xl border border-border bg-card shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_10px_22px_-18px_rgba(0,0,0,0.8)]"
            >
              <button
                onClick={() => setOpenGroup(isOpen ? null : group.name)}
                className="flex w-full items-center gap-2.5 px-4 py-3.5 text-left text-[13.5px] font-semibold text-foreground"
              >
                <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.25 }}>
                  <ChevronDown className={cn("h-4 w-4", isOpen ? "text-primary" : "text-faint")} />
                </motion.span>
                <span className="flex-1">{group.name}</span>
                <span className="rounded-full bg-card-alt px-2 py-0.5 text-[11px] font-semibold text-faint">
                  {total}
                </span>
              </button>
              <AnimatePresence initial={false}>
                {isOpen && (
                  <motion.div
                    initial={{ height: 0 }}
                    animate={{ height: "auto" }}
                    exit={{ height: 0 }}
                    transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                    className="overflow-hidden"
                  >
                    {group.categories.map((cat) => (
                      <button
                        key={cat}
                        onClick={() => setCategory(cat)}
                        className={cn(
                          "flex w-full items-center justify-between border-t border-border px-4 py-3 pl-7 text-left text-[13px] transition-colors",
                          category === cat ? "bg-white/[0.06] text-primary" : "text-muted-foreground hover:bg-white/[0.03] hover:text-foreground"
                        )}
                      >
                        <span>{cat}</span>
                        <span className="flex items-center gap-1.5 text-faint">
                          <span className="text-[11px]">{counts[cat]}</span>
                          <ChevronRight className="h-[15px] w-[15px]" />
                        </span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </section>
  );
}
