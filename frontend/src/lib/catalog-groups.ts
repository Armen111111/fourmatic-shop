// Ported 1:1 from the vanilla app's CATALOG_GROUPS — groups real product
// categories under the vehicle-system tree the client asked for.
export const CATALOG_GROUPS: { name: string; categories: string[] }[] = [
  { name: "Детали для ТО", categories: ["Масла и жидкости", "Фильтры"] },
  { name: "Двигатель", categories: ["Двигатель", "Сцепление"] },
  { name: "Система охлаждения", categories: ["Охлаждение", "Радиаторы", "Насосы системы охлаждения"] },
  {
    name: "Ходовая часть",
    categories: ["Подвеска", "Пневмоподвеска", "Амортизаторы", "Пружины подвески", "Ролики и натяжители"],
  },
  { name: "Рулевое управление", categories: ["Рулевое управление"] },
  { name: "Тормозная система", categories: ["Тормозная система", "Тормозные диски", "Тормозные колодки"] },
  { name: "Электрооборудование", categories: ["Электрика", "Датчики"] },
  { name: "Кузов и оптика", categories: ["Оптика", "Щётки стеклоочистителя"] },
];
