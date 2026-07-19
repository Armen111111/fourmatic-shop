"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { Heart } from "lucide-react";
import type { Product } from "@/lib/types";
import { formatPrice } from "@/lib/format";
import { useFavoritesStore } from "@/store/favorites";
import { useUIStore } from "@/store/ui";
import { cn } from "@/lib/utils";

export function ProductCard({ product, index = 0 }: { product: Product; index?: number }) {
  const isFav = useFavoritesStore((s) => s.ids.includes(product.id));
  const toggleFav = useFavoritesStore((s) => s.toggle);
  const openSheet = useUIStore((s) => s.openSheet);

  const stockLabel = product.price_on_request
    ? "Под запрос"
    : product.in_stock
      ? "В наличии"
      : "Под заказ";
  const badge = product.is_hit ? "Хит" : product.is_new ? "Новинка" : null;

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 14, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, delay: Math.min(index, 11) * 0.035, ease: [0.16, 1, 0.3, 1] }}
      whileTap={{ scale: 0.97 }}
      onClick={() => openSheet("product", product.id)}
      className="group relative flex cursor-pointer flex-col overflow-hidden rounded-3xl border border-border bg-card shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_14px_30px_-22px_rgba(0,0,0,0.8)] transition-colors hover:border-border-strong hover:bg-card-elevated"
    >
      {badge && (
        <span className="absolute left-2.5 top-2.5 z-10 rounded-full border border-border-strong bg-background/80 px-2.5 py-1 text-[9px] font-semibold uppercase tracking-wide text-foreground backdrop-blur">
          {badge}
        </span>
      )}
      <button
        onClick={(e) => {
          e.stopPropagation();
          toggleFav(product.id);
        }}
        className={cn(
          "absolute right-2.5 top-2.5 z-10 flex h-8 w-8 items-center justify-center rounded-full border border-border-strong bg-background/80 backdrop-blur transition-transform active:scale-90",
          isFav && "border-destructive text-destructive"
        )}
      >
        <Heart className="h-[15px] w-[15px]" strokeWidth={1.8} fill={isFav ? "currentColor" : "none"} />
      </button>

      <div className="relative aspect-square w-full bg-card-elevated">
        <Image
          src={product.image}
          alt={product.name}
          fill
          sizes="(max-width: 640px) 50vw, 200px"
          className="object-cover"
          unoptimized
        />
      </div>

      <div className="flex flex-1 flex-col gap-1 p-3.5">
        <span className="text-[10px] font-semibold uppercase tracking-wide text-faint">
          {product.brand}
        </span>
        <span className="text-[10.5px] tabular-nums text-faint">OEM {product.oem || "—"}</span>
        <span className="text-[13px] font-medium leading-snug text-foreground">{product.name}</span>
        <div className="mt-auto flex items-center justify-between gap-2 pt-1.5">
          <span className="text-[15px] font-bold tabular-nums tracking-tight text-foreground">
            {formatPrice(product.price)}
          </span>
          <span
            className={cn(
              "flex items-center gap-1 text-[10px]",
              product.price_on_request ? "text-faint" : product.in_stock ? "text-emerald-400" : "text-faint"
            )}
          >
            <span className="h-1.5 w-1.5 rounded-full bg-current" />
            {stockLabel}
          </span>
        </div>
      </div>
    </motion.article>
  );
}
