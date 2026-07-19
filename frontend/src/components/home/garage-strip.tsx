"use client";

import { motion } from "framer-motion";
import { Car, Plus } from "lucide-react";
import { useGarageStore } from "@/store/garage";
import { useUIStore } from "@/store/ui";

export function GarageStrip() {
  const cars = useGarageStore((s) => s.cars);
  const openSheet = useUIStore((s) => s.openSheet);
  const setSearch = useUIStore((s) => s.setSearch);
  const setTab = useUIStore((s) => s.setTab);

  return (
    <section className="mt-7 px-5">
      <div className="mb-3.5 flex items-center justify-between">
        <span className="flex items-center gap-2 text-[15px] font-bold text-foreground">
          <Car className="h-[18px] w-[18px]" strokeWidth={1.8} />
          Мой гараж
        </span>
        <button
          onClick={() => openSheet("garage")}
          className="rounded-full border border-border-strong px-3.5 py-1.5 text-[11px] font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          Управлять
        </button>
      </div>

      <div className="-mx-5 flex gap-2.5 overflow-x-auto px-5 pb-1">
        {cars.map((car, i) => (
          <motion.button
            key={i}
            whileTap={{ scale: 0.96 }}
            onClick={() => {
              setSearch(car.model);
              setTab("catalog");
            }}
            className="flex w-[132px] shrink-0 flex-col items-start gap-2.5 rounded-2xl border border-border bg-card p-4 text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_12px_26px_-18px_rgba(0,0,0,0.85)] transition-colors hover:bg-card-elevated"
          >
            <span className="flex h-9 w-9 items-center justify-center rounded-[10px] border border-border-strong bg-card-alt text-primary">
              <Car className="h-[18px] w-[18px]" strokeWidth={1.7} />
            </span>
            <span className="text-[13px] font-bold leading-tight text-foreground">{car.model}</span>
            {(car.year || car.engine) && (
              <span className="text-[11px] text-faint">
                {[car.year, car.engine].filter(Boolean).join(" · ")}
              </span>
            )}
          </motion.button>
        ))}

        <motion.button
          whileTap={{ scale: 0.96 }}
          onClick={() => openSheet("garage")}
          className="flex w-[132px] shrink-0 flex-col items-center justify-center gap-2.5 rounded-2xl border border-dashed border-border-strong bg-card p-4 text-center text-[12px] font-semibold text-muted-foreground"
        >
          <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/5 text-primary">
            <Plus className="h-[18px] w-[18px]" strokeWidth={1.8} />
          </span>
          Добавить авто
        </motion.button>
      </div>
    </section>
  );
}
