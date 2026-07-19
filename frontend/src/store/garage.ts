import { create } from "zustand";
import { persist, type PersistStorage, type StorageValue } from "zustand/middleware";
import type { GarageCar } from "@/lib/types";

interface GarageState {
  cars: GarageCar[];
  add: (car: GarageCar) => void;
  remove: (index: number) => void;
}

type Wrapped = { cars: GarageCar[] };

// Bare-array localStorage format (same key/shape as the vanilla app), plus
// migration of pre-existing string-only entries to {model, year, engine}.
const garageStorage: PersistStorage<Wrapped> = {
  getItem: (name) => {
    const raw = localStorage.getItem(name);
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw);
      const list: unknown[] = Array.isArray(parsed) ? parsed : parsed?.state?.cars ?? [];
      const cars: GarageCar[] = list.map((c) =>
        typeof c === "string" ? { model: c, year: "", engine: "" } : (c as GarageCar)
      );
      return { state: { cars }, version: 0 } as StorageValue<Wrapped>;
    } catch {
      return null;
    }
  },
  setItem: (name, value) => {
    localStorage.setItem(name, JSON.stringify(value.state.cars ?? []));
  },
  removeItem: (name) => localStorage.removeItem(name),
};

export const useGarageStore = create<GarageState>()(
  persist(
    (set) => ({
      cars: [],
      add: (car) => set((s) => ({ cars: [...s.cars, car] })),
      remove: (index) => set((s) => ({ cars: s.cars.filter((_, i) => i !== index) })),
    }),
    { name: "fourmatic_garage", storage: garageStorage }
  )
);
