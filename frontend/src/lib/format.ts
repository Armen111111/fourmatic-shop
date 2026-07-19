export function formatPrice(value: number | null | undefined): string {
  if (value === null || value === undefined) return "Узнать цену";
  return `${value.toLocaleString("ru-RU")} ₽`;
}
