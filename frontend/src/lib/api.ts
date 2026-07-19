import { useQuery, useMutation } from "@tanstack/react-query";
import type { CheckoutPayload, CheckoutResponse, Config, Product } from "./types";

async function getJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

export function useConfig() {
  return useQuery({ queryKey: ["config"], queryFn: () => getJSON<Config>("/api/config") });
}

export function useProducts() {
  return useQuery({ queryKey: ["products"], queryFn: () => getJSON<Product[]>("/api/products") });
}

export function useCheckout() {
  return useMutation({
    mutationFn: async (payload: CheckoutPayload): Promise<CheckoutResponse> => {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = (await res.json()) as CheckoutResponse;
      if (!res.ok) throw new Error("error" in data ? data.error : "checkout_failed");
      return data;
    },
  });
}

export function getTelegramInitData(): string {
  if (typeof window === "undefined") return "";
  const tg = (window as unknown as { Telegram?: { WebApp?: { initData?: string } } }).Telegram?.WebApp;
  return tg?.initData ?? "";
}
