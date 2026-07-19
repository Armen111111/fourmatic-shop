import { create } from "zustand";

export type Tab = "home" | "catalog";
export type Sheet = "product" | "cart" | "favorites" | "garage" | "checkout" | null;

interface UIState {
  tab: Tab;
  sheet: Sheet;
  activeProductId: string | null;
  category: string | null;
  brand: string | null;
  search: string;
  filter: "all" | "hit" | "new";
  setTab: (tab: Tab) => void;
  openSheet: (sheet: Sheet, productId?: string) => void;
  closeSheet: () => void;
  setCategory: (category: string | null) => void;
  setBrand: (brand: string | null) => void;
  setSearch: (search: string) => void;
  setFilter: (filter: "all" | "hit" | "new") => void;
  resetFilters: () => void;
}

export const useUIStore = create<UIState>((set, get) => {
  if (typeof window !== "undefined") {
    (window as unknown as { __uiStore?: unknown }).__uiStore = { getState: get, setState: set };
  }
  return {
  tab: "home",
  sheet: null,
  activeProductId: null,
  category: null,
  brand: null,
  search: "",
  filter: "all",
  setTab: (tab) => set({ tab }),
  openSheet: (sheet, productId) => set({ sheet, activeProductId: productId ?? null }),
  closeSheet: () => set({ sheet: null }),
  setCategory: (category) => set({ category, brand: null, filter: "all" }),
  setBrand: (brand) => set({ brand, category: null, filter: "all" }),
  setSearch: (search) => set({ search, category: null, brand: null, filter: "all" }),
  setFilter: (filter) => set({ filter }),
  resetFilters: () => set({ category: null, brand: null, search: "", filter: "all" }),
  };
});
