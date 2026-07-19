"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2 } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { useUIStore } from "@/store/ui";
import { useCartStore } from "@/store/cart";
import { useCheckout, getTelegramInitData } from "@/lib/api";
import type { DeliveryMethod, PaymentMethod } from "@/lib/types";

const schema = z.object({
  name: z.string().min(1, "Укажите имя"),
  phone: z.string().min(1, "Укажите телефон"),
  car_model: z.string().optional(),
  address: z.string().optional(),
  delivery_method: z.enum(["russian_post", "cdek", "yandex", "pickup"]),
  payment_method: z.enum(["transfer", "cash"]),
});
type FormValues = z.infer<typeof schema>;

const deliveryOptions: { value: DeliveryMethod; label: string }[] = [
  { value: "russian_post", label: "Почта России (до отделения)" },
  { value: "cdek", label: "СДЭК до ПВЗ" },
  { value: "yandex", label: "Яндекс Доставка" },
  { value: "pickup", label: "Самовывоз" },
];
const paymentOptions: { value: PaymentMethod; label: string }[] = [
  { value: "transfer", label: "Перевод на карту" },
  { value: "cash", label: "Наличными при получении" },
];

export function CheckoutSheet() {
  const { sheet, closeSheet } = useUIStore();
  const items = useCartStore((s) => s.items);
  const clearCart = useCartStore((s) => s.clear);
  const checkout = useCheckout();
  const [done, setDone] = useState(false);

  const open = sheet === "checkout";

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { delivery_method: "russian_post", payment_method: "transfer" },
  });

  const onSubmit = (values: FormValues) => {
    const cartItems = Object.entries(items).map(([id, qty]) => ({ id, qty }));
    checkout.mutate(
      {
        initData: getTelegramInitData(),
        items: cartItems,
        contact: {
          name: values.name,
          phone: values.phone,
          address: values.address ?? "",
          car_model: values.car_model ?? "",
          delivery_method: values.delivery_method,
          payment_method: values.payment_method,
        },
      },
      {
        onSuccess: (res) => {
          if ("error" in res) return;
          clearCart();
          setDone(true);
        },
      }
    );
  };

  return (
    <Sheet
      open={open}
      onOpenChange={(v) => {
        if (!v) {
          closeSheet();
          setTimeout(() => setDone(false), 300);
        }
      }}
    >
      <SheetContent side="bottom" className="max-h-[90vh] overflow-y-auto rounded-t-3xl border-t border-border-strong bg-card-elevated p-0">
        <div className="p-5">
          <SheetHeader className="mb-3 p-0">
            <SheetTitle className="text-[15px] font-bold">Оформление заказа</SheetTitle>
          </SheetHeader>

          <AnimatePresence mode="wait">
            {done ? (
              <motion.div
                key="done"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", stiffness: 260, damping: 20 }}
                className="flex flex-col items-center gap-3 py-10 text-center"
              >
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 15, delay: 0.1 }}
                  className="flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/15 text-emerald-400"
                >
                  <CheckCircle2 className="h-9 w-9" strokeWidth={1.6} />
                </motion.span>
                <p className="text-[16px] font-bold text-foreground">Заказ принят!</p>
                <p className="max-w-[80%] text-[13px] text-muted-foreground">
                  Менеджер свяжется с вами в этом чате, чтобы подтвердить заказ и способ оплаты.
                </p>
              </motion.div>
            ) : (
              <motion.form
                key="form"
                onSubmit={handleSubmit(onSubmit)}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col gap-3"
              >
                <Field label="Имя" error={errors.name?.message}>
                  <input {...register("name")} placeholder="Как к вам обращаться" className="fm-input" />
                </Field>
                <Field label="Телефон" error={errors.phone?.message}>
                  <input {...register("phone")} type="tel" placeholder="+7 900 000-00-00" className="fm-input" />
                </Field>
                <Field label="Модель автомобиля">
                  <input {...register("car_model")} placeholder="Например, W212 E200, 2013" className="fm-input" />
                </Field>
                <Field label="Адрес доставки">
                  <input {...register("address")} placeholder="Город, улица, дом, квартира" className="fm-input" />
                </Field>

                <fieldset className="flex flex-col gap-2">
                  <legend className="mb-1 text-[13px] font-medium text-muted-foreground">Способ доставки</legend>
                  {deliveryOptions.map((o) => (
                    <label key={o.value} className="flex items-center gap-2.5 text-[14px] text-foreground">
                      <input type="radio" value={o.value} {...register("delivery_method")} className="accent-primary" />
                      {o.label}
                    </label>
                  ))}
                </fieldset>

                <fieldset className="flex flex-col gap-2">
                  <legend className="mb-1 text-[13px] font-medium text-muted-foreground">Способ оплаты</legend>
                  {paymentOptions.map((o) => (
                    <label key={o.value} className="flex items-center gap-2.5 text-[14px] text-foreground">
                      <input type="radio" value={o.value} {...register("payment_method")} className="accent-primary" />
                      {o.label}
                    </label>
                  ))}
                </fieldset>

                <p className="text-[12px] text-faint">
                  После отправки с вами свяжутся в этом чате, чтобы подтвердить заказ и способ оплаты.
                </p>

                {checkout.isError && (
                  <p className="text-[12px] text-destructive">Не удалось отправить заказ. Попробуйте ещё раз.</p>
                )}

                <button
                  type="submit"
                  disabled={checkout.isPending}
                  className="mt-1 rounded-2xl bg-primary py-4 text-[15px] font-semibold text-primary-foreground disabled:opacity-60"
                >
                  {checkout.isPending ? "Отправляем…" : "Отправить заказ"}
                </button>
              </motion.form>
            )}
          </AnimatePresence>
        </div>
      </SheetContent>
    </Sheet>
  );
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="flex flex-col gap-1.5 text-[13px] font-medium text-muted-foreground">
      {label}
      {children}
      {error && <span className="text-[11px] font-normal text-destructive">{error}</span>}
    </label>
  );
}
