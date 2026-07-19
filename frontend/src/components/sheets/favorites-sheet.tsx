"use client";

import Image from "next/image";
import { Heart } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import type { Product } from "@/lib/types";
import { formatPrice } from "@/lib/format";
import { useFavoritesStore } from "@/store/favorites";
import { useUIStore } from "@/store/ui";

export function FavoritesSheet({ products }: { products: Product[] }) {
  const { sheet, closeSheet, openSheet } = useUIStore();
  const ids = useFavoritesStore((s) => s.ids);
  const toggle = useFavoritesStore((s) => s.toggle);

  const open = sheet === "favorites";
  const items = products.filter((p) => ids.includes(p.id));

  return (
    <Sheet open={open} onOpenChange={(v) => !v && closeSheet()}>
      <SheetContent side="bottom" className="max-h-[85vh] overflow-y-auto rounded-t-3xl border-t border-border-strong bg-card-elevated p-0">
        <div className="p-5">
          <SheetHeader className="mb-3 p-0">
            <SheetTitle className="text-[15px] font-bold">Избранное</SheetTitle>
          </SheetHeader>

          {items.length === 0 ? (
            <p className="py-10 text-center text-[13px] text-faint">
              Пока пусто. Нажмите на сердечко на карточке товара.
            </p>
          ) : (
            <div className="flex flex-col gap-2.5">
              {items.map((product) => (
                <div
                  key={product.id}
                  onClick={() => {
                    closeSheet();
                    openSheet("product", product.id);
                  }}
                  className="flex cursor-pointer items-center gap-3 border-b border-border pb-2.5"
                >
                  <div className="relative h-[50px] w-[50px] shrink-0 overflow-hidden rounded-xl bg-card">
                    <Image src={product.image} alt="" fill className="object-cover" unoptimized />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-[13px] font-medium text-foreground">{product.name}</p>
                    <p className="mt-0.5 text-[12px] tabular-nums text-muted-foreground">
                      {formatPrice(product.price)}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggle(product.id);
                    }}
                    className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-destructive text-destructive"
                  >
                    <Heart className="h-4 w-4" fill="currentColor" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}
