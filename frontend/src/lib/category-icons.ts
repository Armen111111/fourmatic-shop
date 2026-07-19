import {
  Filter,
  Disc,
  Waves,
  Cog,
  Lightbulb,
  Snowflake,
  CircleDot,
  Zap,
  Droplet,
  SprayCan,
  LucideIcon,
} from "lucide-react";

export const CATEGORY_ICONS: Record<string, LucideIcon> = {
  Фильтры: Filter,
  "Тормозная система": Disc,
  "Тормозные диски": Disc,
  "Тормозные колодки": Disc,
  Подвеска: Waves,
  Пневмоподвеска: Waves,
  Амортизаторы: Waves,
  "Пружины подвески": Waves,
  "Ролики и натяжители": Waves,
  Двигатель: Cog,
  Сцепление: Cog,
  Оптика: Lightbulb,
  Охлаждение: Snowflake,
  Радиаторы: Snowflake,
  "Насосы системы охлаждения": Snowflake,
  "Рулевое управление": CircleDot,
  Электрика: Zap,
  Датчики: Zap,
  "Масла и жидкости": Droplet,
  "Щётки стеклоочистителя": SprayCan,
};

export const DEFAULT_CATEGORY_ICON: LucideIcon = CircleDot;
