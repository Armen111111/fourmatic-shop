"use client";

import { motion } from "framer-motion";
import type { Product } from "@/lib/types";
import { CATEGORY_ICONS, DEFAULT_CATEGORY_ICON } from "@/lib/category-icons";
import { useUIStore } from "@/store/ui";

export function CategoryGrid({ products }: { products: Product[] }) {
  const setCategory = useUIStore((s) => s.setCategory);
  const setTab = useUIStore((s) => s.setTab);

  const categories = Array.from(new Set(products.map((p) => p.category))).sort();

  return (
    <section className="mt-9 px-5">
      <h3 className="mb-4 text-[17px] font-bold tracking-tight text-foreground">
        Популярные категории
      </h3>
      <div className="grid grid-cols-3 gap-2.5">
        {categories.map((cat, i) => {
          const Icon = CATEGORY_ICONS[cat] ?? DEFAULT_CATEGORY_ICON;
          return (
            <motion.button
              key={cat}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: (i % 9) * 0.03, ease: [0.16, 1, 0.3, 1] }}
              whileTap={{ scale: 0.96 }}
              onClick={() => {
                setCategory(cat);
                setTab("catalog");
              }}
              className="flex flex-col items-center gap-2.5 rounded-2xl border border-border bg-card px-2.5 py-4.5 text-center shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_12px_26px_-18px_rgba(0,0,0,0.85)] transition-colors hover:bg-card-elevated"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-xl border border-border-strong bg-card-alt">
                <Icon className="h-[22px] w-[22px] text-muted-foreground" strokeWidth={1.6} />
              </span>
              <span className="text-[11.5px] font-medium leading-tight text-foreground">{cat}</span>
            </motion.button>
          );
        })}
      </div>
    </section>
  );
}
