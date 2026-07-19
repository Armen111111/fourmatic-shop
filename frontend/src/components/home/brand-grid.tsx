"use client";

import { motion } from "framer-motion";
import type { Product } from "@/lib/types";
import { useUIStore } from "@/store/ui";

export function BrandGrid({ products }: { products: Product[] }) {
  const setBrand = useUIStore((s) => s.setBrand);
  const setTab = useUIStore((s) => s.setTab);

  const brands = Array.from(new Set(products.map((p) => p.brand))).sort();

  return (
    <section className="mt-9 px-5 pb-2">
      <h3 className="mb-4 text-[17px] font-bold tracking-tight text-foreground">Каталог брендов</h3>
      <div className="grid grid-cols-3 gap-2.5">
        {brands.map((brand, i) => (
          <motion.button
            key={brand}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ duration: 0.4, delay: (i % 9) * 0.03, ease: [0.16, 1, 0.3, 1] }}
            whileTap={{ scale: 0.96 }}
            onClick={() => {
              setBrand(brand);
              setTab("catalog");
            }}
            className="flex flex-col items-center gap-2.5 rounded-2xl border border-border bg-card px-2.5 py-4 text-center shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_12px_26px_-18px_rgba(0,0,0,0.85)] transition-colors hover:bg-card-elevated"
          >
            <span className="flex h-[38px] w-[38px] items-center justify-center rounded-[10px] border border-border-strong bg-card-alt text-[14px] font-extrabold text-primary">
              {brand.trim().charAt(0).toUpperCase()}
            </span>
            <span className="text-[11.5px] font-semibold text-foreground">{brand}</span>
          </motion.button>
        ))}
      </div>
    </section>
  );
}
