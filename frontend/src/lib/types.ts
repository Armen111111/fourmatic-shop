export interface Product {
  id: string;
  name: string;
  brand: string;
  category: string;
  oem?: string;
  compatible_models?: string[];
  price: number | null;
  description?: string;
  image: string;
  in_stock: boolean;
  is_hit?: boolean;
  is_new?: boolean;
  delivery_days?: string | null;
  supplier?: string;
  price_on_request?: boolean;
}

export interface Config {
  payments_enabled: boolean;
  currency: string;
}

export interface GarageCar {
  model: string;
  year?: string;
  engine?: string;
}

export type DeliveryMethod = "russian_post" | "cdek" | "yandex" | "pickup";
export type PaymentMethod = "transfer" | "cash";

export interface ContactDetails {
  name: string;
  phone: string;
  address: string;
  car_model: string;
  delivery_method: DeliveryMethod;
  payment_method: PaymentMethod;
}

/** Matches bot/webserver.py handle_checkout exactly — server looks up
 * price/name/stock server-side from {id, qty}, it does not trust the client. */
export interface CheckoutPayload {
  initData: string;
  items: { id: string; qty: number }[];
  contact: ContactDetails;
}

export type CheckoutResponse =
  | { mode: "payment"; order_id: string; invoice_link: string }
  | { mode: "manual"; order_id: string; total: number; currency: string }
  | { error: string };
