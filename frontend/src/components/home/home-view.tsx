"use client";

import type { Product } from "@/lib/types";
import { Hero } from "./hero";
import { SlideCarousel } from "./slide-carousel";
import { SearchBar } from "./search-bar";
import { GarageStrip } from "./garage-strip";
import { CategoryGrid } from "./category-grid";
import { BrandGrid } from "./brand-grid";

export function HomeView({ products }: { products: Product[] }) {
  return (
    <div>
      <Hero />
      <SlideCarousel />
      <SearchBar />
      <GarageStrip />
      <CategoryGrid products={products} />
      <BrandGrid products={products} />

      <footer className="mx-5 mb-6 mt-9 rounded-3xl border border-border bg-white/[0.03] p-5 text-center">
        <p className="text-[15px] font-bold text-foreground">Помогаем найти нужную деталь</p>
        <p className="mt-1.5 text-[12px] leading-relaxed text-muted-foreground">
          Если не нашли деталь в каталоге — напишите нам, поможем подобрать вручную.
        </p>
      </footer>
    </div>
  );
}
