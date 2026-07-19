"use client";

import Image from "next/image";
import { Heart } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import type { Product } from "@/lib/types";
import { formatPrice } from "@/lib/format";
import { useUIStore } from "@/store/ui";
import { useFavoritesStore } from "@/store/favorites";
import { useCartStore } from "@/store/cart";
import { cn } from "@/lib/utils";

export function ProductSheet({ products }: { products: Product[] }) {
  const { sheet, activeProductId, closeSheet, openSheet } = useUIStore();
  const isFav = useFavoritesStore((s) => (activeProductId ? s.ids.includes(activeProductId) : false));
  const toggleFav = useFavoritesStore((s) => s.toggle);
  const qty = useCartStore((s) => (activeProductId ? s.items[activeProductId] ?? 0 : 0));
  const setQty = useCartStore((s) => s.setQty);

  const product = products.find((p) => p.id === activeProductId) ?? null;
  const open = sheet === "product" && !!product;
  const canBuy = !!product?.in_stock && !product?.price_on_request;

  return (
    <Sheet open={open} onOpenChange={(v) => !v && closeSheet()}>
      <SheetContent side="bottom" className="max-h-[88vh] overflow-y-auto rounded-t-3xl border-t border-border-strong bg-card-elevated p-0">
        {product && (
          <div className="p-5">
            <SheetHeader className="mb-3 p-0">
              <SheetTitle className="text-[15px] font-bold">О товаре</SheetTitle>
            </SheetHeader>

            <div className="relative aspect-square w-full overflow-hidden rounded-2xl bg-card">
              <Image src={product.image} alt={product.name} fill className="object-cover" unoptimized />
            </div>

            <h2 className="mt-4 text-[19px] font-bold leading-snug tracking-tight text-foreground">
              {product.name}
            </h2>
            <div className="mt-1.5 flex flex-col gap-0.5 text-[12px] text-muted-foreground">
              <span>Бренд: {product.brand}</span>
              <span>OEM-номер: {product.oem || "—"}</span>
            </div>
            {product.description && (
              <p className="mt-3 text-[13px] leading-relaxed text-muted-foreground">{product.description}</p>
            )}

            {!!product.compatible_models?.length && (
              <div className="mt-3 rounded-xl border border-border bg-card p-3.5">
                <p className="mb-2 text-[10.5px] font-semibold uppercase tracking-wide text-faint">
                  Совместимость
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {product.compatible_models.map((m) => (
                    <span key={m} className="rounded-lg border border-border-strong bg-white/[0.05] px-2.5 py-1 text-[11px] text-muted-foreground">
                      {m}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-4 flex items-center justify-between rounded-2xl border border-border bg-card p-4">
              <div>
                <div className="text-[20px] font-bold tabular-nums tracking-tight text-foreground">
                  {formatPrice(product.price)}
                </div>
                <div className="mt-0.5 text-[11px] text-muted-foreground">
                  {product.price_on_request
                    ? "Цена уточняется у поставщика"
                    : product.in_stock
                      ? "В наличии"
                      : "Под заказ"}{" "}
                  · доставка {product.delivery_days || "—"} дн.
                </div>
              </div>
            </div>

            <div className="mt-3 flex gap-2">
              <button
                onClick={() => toggleFav(product.id)}
                className={cn(
                  "flex h-[46px] w-[46px] shrink-0 items-center justify-center rounded-xl border border-border-strong bg-card transition-colors",
                  isFav && "border-destructive text-destructive"
                )}
              >
                <Heart className="h-[18px] w-[18px]" fill={isFav ? "currentColor" : "none"} />
              </button>
              <button
                disabled={!canBuy}
                onClick={() => {
                  setQty(product.id, qty + 1);
                  closeSheet();
                  openSheet("checkout");
                }}
                className="flex-1 rounded-xl border border-border-strong text-[14px] font-semibold text-foreground transition-colors disabled:border-border disabled:text-faint"
              >
                Купить в 1 клик
              </button>
              <button
                disabled={!canBuy}
                onClick={() => setQty(product.id, qty + 1)}
                className="flex-1 rounded-xl bg-primary text-[14px] font-semibold text-primary-foreground transition-opacity disabled:bg-card disabled:text-faint"
              >
                {qty > 0 ? `В корзине: ${qty}` : "В корзину"}
              </button>
            </div>
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
