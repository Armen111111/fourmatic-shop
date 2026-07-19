"use client";

import type { Product } from "@/lib/types";
import { CatalogTree } from "./catalog-tree";
import { ProductGrid } from "./product-grid";

export function CatalogView({ products }: { products: Product[] }) {
  return (
    <div>
      <CatalogTree products={products} />
      <ProductGrid products={products} />
    </div>
  );
}
