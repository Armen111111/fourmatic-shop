"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence, type PanInfo } from "framer-motion";
import { ShieldCheck, ScanSearch, Truck, Award, LucideIcon } from "lucide-react";

interface Slide {
  icon: LucideIcon;
  title: string;
  text: string;
}

const slides: Slide[] = [
  {
    icon: ShieldCheck,
    title: "Оригинальные детали и качественные аналоги",
    text: "Подбор по VIN и OEM с проверкой совместимости.",
  },
  {
    icon: ScanSearch,
    title: "Подбор по VIN",
    text: "Точный подбор деталей именно под ваш автомобиль.",
  },
  {
    icon: Truck,
    title: "Доставка",
    text: "Отправляем по всей России проверенными транспортными компаниями.",
  },
  {
    icon: Award,
    title: "Проверенные бренды",
    text: "Bosch, ATE, MANN, Mahle, Bilstein, Lemförder, Sachs, Febi, INA, LuK.",
  },
];

export function SlideCarousel() {
  const [index, setIndex] = useState(0);
  const [direction, setDirection] = useState(0);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    timer.current = setInterval(() => {
      setDirection(1);
      setIndex((i) => (i + 1) % slides.length);
    }, 5000);
    return () => {
      if (timer.current) clearInterval(timer.current);
    };
  }, []);

  const goTo = (next: number) => {
    setDirection(next > index ? 1 : -1);
    setIndex((next + slides.length) % slides.length);
    if (timer.current) clearInterval(timer.current);
  };

  const onDragEnd = (_: unknown, info: PanInfo) => {
    if (info.offset.x < -60) goTo(index + 1);
    else if (info.offset.x > 60) goTo(index - 1);
  };

  const slide = slides[index];
  const Icon = slide.icon;

  return (
    <section className="mx-5 mt-7 overflow-hidden rounded-3xl border border-border bg-gradient-to-br from-card-alt to-card shadow-[inset_0_1px_0_rgba(255,255,255,0.05),0_18px_40px_-26px_rgba(0,0,0,0.85)]">
      <div className="relative h-[190px]">
        <AnimatePresence initial={false} custom={direction} mode="popLayout">
          <motion.div
            key={index}
            custom={direction}
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.6}
            onDragEnd={onDragEnd}
            initial={{ x: direction >= 0 ? 60 : -60, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: direction >= 0 ? -60 : 60, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 32 }}
            className="absolute inset-0 flex cursor-grab flex-col justify-center px-7 py-7 active:cursor-grabbing"
          >
            <span className="mb-2 flex h-11 w-11 items-center justify-center rounded-xl border border-border-strong bg-card text-primary">
              <Icon className="h-5 w-5" strokeWidth={1.7} />
            </span>
            <h3 className="max-w-[92%] text-[18px] font-bold leading-snug tracking-tight text-foreground">
              {slide.title}
            </h3>
            <p className="mt-2 max-w-[90%] text-[12.5px] leading-relaxed text-muted-foreground">
              {slide.text}
            </p>
          </motion.div>
        </AnimatePresence>
      </div>
      <div className="flex justify-center gap-1.5 pb-4">
        {slides.map((_, i) => (
          <button
            key={i}
            aria-label={`Слайд ${i + 1}`}
            onClick={() => goTo(i)}
            className="h-1.5 rounded-full bg-white/25 transition-all"
            style={{ width: i === index ? 16 : 6, backgroundColor: i === index ? "var(--primary)" : undefined }}
          />
        ))}
      </div>
    </section>
  );
}
