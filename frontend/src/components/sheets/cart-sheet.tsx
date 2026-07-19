"use client";

import Image from "next/image";
import { Minus, Plus } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import type { Product } from "@/lib/types";
import { formatPrice } from "@/lib/format";
import { useCartStore } from "@/store/cart";
import { useUIStore } from "@/store/ui";

export function CartSheet({ products }: { products: Product[] }) {
  const { sheet, closeSheet, openSheet } = useUIStore();
  const items = useCartStore((s) => s.items);
  const setQty = useCartStore((s) => s.setQty);

  const open = sheet === "cart";
  const entries = Object.entries(items)
    .map(([id, qty]) => ({ product: products.find((p) => p.id === id), qty }))
    .filter((e): e is { product: Product; qty: number } => !!e.product && e.qty > 0);

  const total = entries.reduce((sum, e) => sum + (e.product.price ?? 0) * e.qty, 0);

  return (
    <Sheet open={open} onOpenChange={(v) => !v && closeSheet()}>
      <SheetContent side="bottom" className="max-h-[85vh] overflow-y-auto rounded-t-3xl border-t border-border-strong bg-card-elevated p-0">
        <div className="p-5">
          <SheetHeader className="mb-3 p-0">
            <SheetTitle className="text-[15px] font-bold">Корзина</SheetTitle>
          </SheetHeader>

          {entries.length === 0 ? (
            <p className="py-10 text-center text-[13px] text-faint">Корзина пуста</p>
          ) : (
            <div className="flex flex-col gap-2.5">
              {entries.map(({ product, qty }) => (
                <div key={product.id} className="flex items-center gap-3 border-b border-border pb-2.5">
                  <div className="relative h-[50px] w-[50px] shrink-0 overflow-hidden rounded-xl bg-card">
                    <Image src={product.image} alt="" fill className="object-cover" unoptimized />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-[13px] font-medium text-foreground">{product.name}</p>
                    <p className="mt-0.5 text-[12px] tabular-nums text-muted-foreground">
                      {formatPrice(product.price)}
                    </p>
                    <div className="mt-2 flex w-fit items-center gap-1 rounded-lg border border-border bg-card p-1">
                      <button
                        onClick={() => setQty(product.id, qty - 1)}
                        className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground"
                      >
                        <Minus className="h-3.5 w-3.5" />
                      </button>
                      <span className="w-6 text-center text-[12px] font-semibold tabular-nums">{qty}</span>
                      <button
                        onClick={() => setQty(product.id, qty + 1)}
                        className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground"
                      >
                        <Plus className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 border-t border-border pt-4">
            <div className="mb-3 flex items-center justify-between text-[17px] font-bold">
              <span>Итого:</span>
              <span className="tabular-nums">{formatPrice(total)}</span>
            </div>
            <button
              disabled={entries.length === 0}
              onClick={() => openSheet("checkout")}
              className="w-full rounded-2xl bg-primary py-4 text-[15px] font-semibold text-primary-foreground disabled:bg-card disabled:text-faint"
            >
              Оформить заказ
            </button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
