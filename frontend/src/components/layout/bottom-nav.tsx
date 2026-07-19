"use client";

import { motion } from "framer-motion";
import { Home, LayoutGrid, Heart, ShoppingBag } from "lucide-react";
import { useUIStore } from "@/store/ui";
import { useFavoritesStore } from "@/store/favorites";
import { useCartStore } from "@/store/cart";
import { cn } from "@/lib/utils";

interface NavItem {
  key: string;
  label: string;
  icon: typeof Home;
  count?: number;
}

const items: NavItem[] = [
  { key: "home", label: "Главная", icon: Home },
  { key: "catalog", label: "Каталог", icon: LayoutGrid },
];

export function BottomNav() {
  const { tab, setTab, sheet, openSheet } = useUIStore();
  const favCount = useFavoritesStore((s) => s.ids.length);
  const cartCount = useCartStore((s) => Object.values(s.items).reduce((a, b) => a + b, 0));

  const active: string = sheet === "favorites" ? "favorites" : sheet === "cart" ? "cart" : tab;

  const go = (key: string) => {
    if (key === "favorites") return openSheet("favorites");
    if (key === "cart") return openSheet("cart");
    setTab(key as "home" | "catalog");
    if (sheet === "favorites" || sheet === "cart") openSheet(null);
  };

  const all: NavItem[] = [
    ...items,
    { key: "favorites", label: "Избранное", icon: Heart, count: favCount },
    { key: "cart", label: "Корзина", icon: ShoppingBag, count: cartCount },
  ];

  return (
    <nav className="fixed inset-x-0 bottom-0 z-30 flex gap-1 border-t border-border bg-background/85 px-1.5 pb-[calc(8px+env(safe-area-inset-bottom))] pt-2 backdrop-blur-2xl">
      {all.map(({ key, label, icon: Icon, count }) => {
        const isActive = active === key;
        return (
          <button
            key={key}
            onClick={() => go(key)}
            className="relative flex flex-1 flex-col items-center gap-1 rounded-2xl py-1.5 text-[10px] font-medium"
          >
            {isActive && (
              <motion.span
                layoutId="nav-active"
                className="absolute inset-0 rounded-2xl bg-card-alt"
                transition={{ type: "spring", stiffness: 420, damping: 34 }}
              />
            )}
            <span className="relative">
              <Icon
                className={cn(
                  "h-[21px] w-[21px] transition-colors",
                  isActive ? "text-foreground" : "text-faint"
                )}
                strokeWidth={1.7}
              />
              {!!count && (
                <span className="absolute -right-2 -top-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-primary px-1 text-[9px] font-bold text-primary-foreground">
                  {count}
                </span>
              )}
            </span>
            <span className={cn("relative", isActive ? "text-foreground" : "text-faint")}>{label}</span>
          </button>
        );
      })}
    </nav>
  );
}
