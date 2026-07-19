"use client";

import { motion } from "framer-motion";
import { useProducts } from "@/lib/api";
import { useUIStore } from "@/store/ui";
import { Header } from "@/components/layout/header";
import { BottomNav } from "@/components/layout/bottom-nav";
import { HomeView } from "@/components/home/home-view";
import { CatalogView } from "@/components/catalog/catalog-view";
import { ProductSheet } from "@/components/sheets/product-sheet";
import { CartSheet } from "@/components/sheets/cart-sheet";
import { FavoritesSheet } from "@/components/sheets/favorites-sheet";
import { GarageSheet } from "@/components/sheets/garage-sheet";
import { CheckoutSheet } from "@/components/sheets/checkout-sheet";
import { Skeleton } from "@/components/ui/skeleton";

export default function HomePage() {
  const { data: products, isLoading } = useProducts();
  const tab = useUIStore((s) => s.tab);

  return (
    <>
      <Header />
      <main className="flex-1 pb-24">
        {isLoading || !products ? (
          <LoadingState />
        ) : (
          <motion.div
            key={tab}
            initial={{ opacity: 0, y: 8, filter: "blur(4px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.32, ease: [0.16, 1, 0.3, 1] }}
          >
            {tab === "home" ? <HomeView products={products} /> : <CatalogView products={products} />}
          </motion.div>
        )}
      </main>
      <BottomNav />

      {products && (
        <>
          <ProductSheet products={products} />
          <CartSheet products={products} />
          <FavoritesSheet products={products} />
          <GarageSheet />
          <CheckoutSheet />
        </>
      )}
    </>
  );
}

function LoadingState() {
  return (
    <div className="px-5 pt-8">
      <Skeleton className="h-6 w-40 rounded-full" />
      <Skeleton className="mt-4 h-16 w-[92%] rounded-2xl" />
      <Skeleton className="mt-6 h-[190px] w-full rounded-3xl" />
      <div className="mt-7 grid grid-cols-3 gap-2.5">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-24 rounded-2xl" />
        ))}
      </div>
    </div>
  );
}
