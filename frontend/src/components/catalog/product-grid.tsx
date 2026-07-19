"use client";

import { useMemo, useRef } from "react";
import { useWindowVirtualizer } from "@tanstack/react-virtual";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import type { Product } from "@/lib/types";
import { useUIStore } from "@/store/ui";
import { ProductCard } from "@/components/product/product-card";

const COLUMNS = 2;
const ROW_HEIGHT = 268;

export function ProductGrid({ products }: { products: Product[] }) {
  const { category, brand, search, filter, resetFilters } = useUIStore();
  const containerRef = useRef<HTMLDivElement>(null);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return products.filter((p) => {
      if (filter === "hit" && !p.is_hit) return false;
      if (filter === "new" && !p.is_new) return false;
      if (category && p.category !== category) return false;
      if (brand && p.brand !== brand) return false;
      if (q) {
        const hay = [p.name, p.brand, p.oem, p.category, ...(p.compatible_models ?? [])]
          .join(" ")
          .toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [products, category, brand, search, filter]);

  const rows = Math.ceil(filtered.length / COLUMNS);
  const virtualizer = useWindowVirtualizer({
    count: rows,
    estimateSize: () => ROW_HEIGHT,
    overscan: 6,
    scrollMargin: containerRef.current?.offsetTop ?? 0,
  });

  const activeLabel = category || brand || (search ? `«${search}»` : null);
  const title = activeLabel ? activeLabel : "Все товары";

  return (
    <section className="px-5 pb-4 pt-7">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-[17px] font-bold tracking-tight text-foreground">{title}</h3>
        <div className="flex gap-1.5">
          {(["all", "hit", "new"] as const).map((f) => (
            <button
              key={f}
              onClick={() => useUIStore.getState().setFilter(f)}
              className={`rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors ${
                filter === f
                  ? "border-transparent bg-primary text-primary-foreground"
                  : "border-border-strong text-muted-foreground"
              }`}
            >
              {f === "all" ? "Все" : f === "hit" ? "Хиты" : "Новинки"}
            </button>
          ))}
        </div>
      </div>

      {activeLabel && (
        <button
          onClick={resetFilters}
          className="mb-3 flex w-full items-center justify-between rounded-xl border border-border bg-white/[0.04] px-3.5 py-2.5 text-[12px] text-muted-foreground"
        >
          <span>Фильтр: {activeLabel}</span>
          <span className="flex items-center gap-1 font-semibold text-foreground">
            Сбросить <X className="h-3.5 w-3.5" />
          </span>
        </button>
      )}

      {filtered.length === 0 ? (
        <p className="py-10 text-center text-[13px] text-faint">
          Ничего не найдено. Попробуйте другой запрос.
        </p>
      ) : (
        <div ref={containerRef} style={{ height: virtualizer.getTotalSize(), position: "relative" }}>
          {virtualizer.getVirtualItems().map((row) => {
            const start = row.index * COLUMNS;
            const rowProducts = filtered.slice(start, start + COLUMNS);
            return (
              <motion.div
                key={row.key}
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  width: "100%",
                  height: row.size,
                  transform: `translateY(${row.start - virtualizer.options.scrollMargin}px)`,
                }}
                className="grid grid-cols-2 gap-3"
              >
                {rowProducts.map((p, i) => (
                  <ProductCard key={p.id} product={p} index={i} />
                ))}
              </motion.div>
            );
          })}
        </div>
      )}
    </section>
  );
}
