import { create } from "zustand";

// Not persisted — matches the previous vanilla app, where the cart lived
// only in memory for the session (favorites/garage are the ones saved).
interface CartState {
  items: Record<string, number>; // productId -> qty
  setQty: (id: string, qty: number) => void;
  clear: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  items: {},
  setQty: (id, qty) =>
    set((s) => {
      const items = { ...s.items };
      if (qty <= 0) delete items[id];
      else items[id] = qty;
      return { items };
    }),
  clear: () => set({ items: {} }),
}));
