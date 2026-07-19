"use client";

import { useState } from "react";
import { X, Car } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { useGarageStore } from "@/store/garage";
import { useUIStore } from "@/store/ui";

export function GarageSheet() {
  const { sheet, closeSheet } = useUIStore();
  const cars = useGarageStore((s) => s.cars);
  const add = useGarageStore((s) => s.add);
  const remove = useGarageStore((s) => s.remove);

  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [engine, setEngine] = useState("");

  const open = sheet === "garage";

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!model.trim()) return;
    add({ model: model.trim(), year: year.trim(), engine: engine.trim() });
    setModel("");
    setYear("");
    setEngine("");
  };

  return (
    <Sheet open={open} onOpenChange={(v) => !v && closeSheet()}>
      <SheetContent side="bottom" className="max-h-[85vh] overflow-y-auto rounded-t-3xl border-t border-border-strong bg-card-elevated p-0">
        <div className="p-5">
          <SheetHeader className="mb-3 p-0">
            <SheetTitle className="text-[15px] font-bold">Мой гараж</SheetTitle>
          </SheetHeader>

          <form onSubmit={submit} className="flex flex-col gap-3">
            <label className="flex flex-col gap-1.5 text-[13px] font-medium text-muted-foreground">
              Модель автомобиля
              <input
                value={model}
                onChange={(e) => setModel(e.target.value)}
                maxLength={60}
                required
                placeholder="Например, W213 E-Class"
                className="rounded-xl border border-border-strong bg-white/[0.04] px-3.5 py-3 text-[14px] text-foreground placeholder:text-faint focus:outline-none"
              />
            </label>
            <label className="flex flex-col gap-1.5 text-[13px] font-medium text-muted-foreground">
              Год выпуска
              <input
                value={year}
                onChange={(e) => setYear(e.target.value)}
                maxLength={4}
                placeholder="Например, 2019"
                className="rounded-xl border border-border-strong bg-white/[0.04] px-3.5 py-3 text-[14px] text-foreground placeholder:text-faint focus:outline-none"
              />
            </label>
            <label className="flex flex-col gap-1.5 text-[13px] font-medium text-muted-foreground">
              Двигатель
              <input
                value={engine}
                onChange={(e) => setEngine(e.target.value)}
                maxLength={40}
                placeholder="Например, 2.0 бензин"
                className="rounded-xl border border-border-strong bg-white/[0.04] px-3.5 py-3 text-[14px] text-foreground placeholder:text-faint focus:outline-none"
              />
            </label>
            <button type="submit" className="rounded-2xl bg-primary py-3.5 text-[14px] font-semibold text-primary-foreground">
              Добавить в гараж
            </button>
          </form>

          <div className="mt-5 flex flex-col gap-2">
            {cars.length === 0 && (
              <p className="py-6 text-center text-[13px] text-faint">Автомобилей пока нет</p>
            )}
            {cars.map((car, i) => (
              <div key={i} className="flex items-center gap-3 rounded-xl border border-border bg-card p-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-border-strong bg-card-alt text-primary">
                  <Car className="h-4 w-4" />
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-[13px] font-semibold text-foreground">{car.model}</p>
                  {(car.year || car.engine) && (
                    <p className="text-[11.5px] text-faint">
                      {[car.year, car.engine].filter(Boolean).join(" · ")}
                    </p>
                  )}
                </div>
                <button onClick={() => remove(i)} className="text-faint transition-colors hover:text-destructive">
                  <X className="h-[15px] w-[15px]" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
