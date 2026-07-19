import { create } from "zustand";
import { persist, type PersistStorage, type StorageValue } from "zustand/middleware";

interface FavoritesState {
  ids: string[];
  toggle: (id: string) => void;
}

type Wrapped = { ids: string[] };

// Bare-array localStorage format — matches the vanilla app's
// `fourmatic_favorites` key so existing users keep their saved list.
const favoritesStorage: PersistStorage<Wrapped> = {
  getItem: (name) => {
    const raw = localStorage.getItem(name);
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw);
      const ids: string[] = Array.isArray(parsed) ? parsed : parsed?.state?.ids ?? [];
      return { state: { ids }, version: 0 } as StorageValue<Wrapped>;
    } catch {
      return null;
    }
  },
  setItem: (name, value) => {
    localStorage.setItem(name, JSON.stringify(value.state.ids ?? []));
  },
  removeItem: (name) => localStorage.removeItem(name),
};

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set) => ({
      ids: [],
      toggle: (id) =>
        set((s) => ({
          ids: s.ids.includes(id) ? s.ids.filter((x) => x !== id) : [...s.ids, id],
        })),
    }),
    { name: "fourmatic_favorites", storage: favoritesStorage }
  )
);
