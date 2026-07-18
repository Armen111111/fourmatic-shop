const tg = window.Telegram?.WebApp;
tg?.ready();
tg?.expand();

const state = {
  products: [],
  tab: "all",
  category: null,
  brand: null,
  search: "",
  cart: {},
  favorites: [],
  garage: [],
  paymentsEnabled: false,
  visibleCount: 20,
  activeTab: "home",
};

function icon(paths) {
  return `<svg class="category-card-icon" viewBox="0 0 24 24">${paths}</svg>`;
}

const ICON_FILTER = icon('<path d="M4 4h16l-6 8v6l-4 2v-8L4 4z"/>');
const ICON_BRAKE = icon('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="6.5" r=".6" fill="currentColor" stroke="none"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/><circle cx="6.5" cy="12" r=".6" fill="currentColor" stroke="none"/><circle cx="17.5" cy="12" r=".6" fill="currentColor" stroke="none"/>');
const ICON_SUSPENSION = icon('<path d="M12 2v3M9 5l6 2-6 2 6 2-6 2 6 2M12 17v5"/>');
const ICON_ENGINE = icon('<path d="M4 10h4V7h4v3h4V7h2v3h1a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z"/>');
const ICON_LIGHT = icon('<path d="M12 3a6 6 0 0 0-3 11.2c.6.4 1 1 1 1.8h4c0-.8.4-1.4 1-1.8A6 6 0 0 0 12 3z"/><path d="M9.5 18.5h5M10.5 21h3"/>');
const ICON_COOLING = icon('<rect x="4" y="6" width="16" height="12" rx="1.5"/><path d="M9 6v12M13 6v12M17 6v12"/>');
const ICON_STEERING = icon('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M12 5v5M7.8 15.5l3.4-2M16.2 15.5l-3.4-2"/>');
const ICON_ELECTRIC = icon('<rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>');
const ICON_FLUID = icon('<path d="M12 3s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/>');
const ICON_WIPER = icon('<path d="M5 19L19 5"/><path d="M13 5h6v6"/>');
const ICON_DEFAULT = icon('<path d="M12 2l8 4.6v9.2L12 22l-8-4.6V6.6L12 2z"/><circle cx="12" cy="12" r="3"/>');
const HEART_ICON = '<svg class="icon" viewBox="0 0 24 24"><path d="M12 20.5c-.3 0-.6-.1-.8-.3C7.6 17.3 3 13.6 3 9.5 3 6.7 5.2 4.5 8 4.5c1.6 0 3 .8 4 2.1 1-1.3 2.4-2.1 4-2.1 2.8 0 5 2.2 5 5 0 4.1-4.6 7.8-8.2 10.7-.2.2-.5.3-.8.3z"/></svg>';

const CATEGORY_ICONS = {
  "Фильтры": ICON_FILTER,
  "Тормозная система": ICON_BRAKE,
  "Тормозные диски": ICON_BRAKE,
  "Тормозные колодки": ICON_BRAKE,
  "Подвеска": ICON_SUSPENSION,
  "Пневмоподвеска": ICON_SUSPENSION,
  "Амортизаторы": ICON_SUSPENSION,
  "Пружины подвески": ICON_SUSPENSION,
  "Ролики и натяжители": ICON_SUSPENSION,
  "Двигатель": ICON_ENGINE,
  "Сцепление": ICON_ENGINE,
  "Оптика": ICON_LIGHT,
  "Охлаждение": ICON_COOLING,
  "Радиаторы": ICON_COOLING,
  "Насосы системы охлаждения": ICON_COOLING,
  "Рулевое управление": ICON_STEERING,
  "Электрика": ICON_ELECTRIC,
  "Датчики": ICON_ELECTRIC,
  "Масла и жидкости": ICON_FLUID,
  "Щётки стеклоочистителя": ICON_WIPER,
};

const productGridEl = document.getElementById("product-grid");
const loadMoreBtn = document.getElementById("load-more-btn");
const tabHomeEl = document.getElementById("tab-home");
const tabCatalogEl = document.getElementById("tab-catalog");
const bottomNavItems = document.querySelectorAll(".bottom-nav-item");
const bottomNavCartCountEl = document.getElementById("bottom-nav-cart-count");
const categoryGridEl = document.getElementById("category-grid");
const brandGridEl = document.getElementById("brand-grid");
const filtersEl = document.getElementById("filters");
const activeFilterRowEl = document.getElementById("active-filter-row");
const activeFilterLabelEl = document.getElementById("active-filter-label");
const clearFilterBtn = document.getElementById("clear-filter-btn");
const vinInputEl = document.getElementById("vin-input");
const vinSearchBtn = document.getElementById("vin-search-btn");

const cartBtn = document.getElementById("cart-btn");
const cartOverlay = document.getElementById("cart-overlay");
const closeCartBtn = document.getElementById("close-cart");
const cartItemsEl = document.getElementById("cart-items");
const cartCountEl = document.getElementById("cart-count");
const cartTotalEl = document.getElementById("cart-total");
const checkoutBtn = document.getElementById("checkout-btn");

const favoritesBtn = document.getElementById("favorites-btn");
const favoritesOverlay = document.getElementById("favorites-overlay");
const closeFavoritesBtn = document.getElementById("close-favorites");
const favoritesItemsEl = document.getElementById("favorites-items");
const favoritesCountEl = document.getElementById("favorites-count");

const garageManageBtn = document.getElementById("garage-manage-btn");
const garageOverlay = document.getElementById("garage-overlay");
const closeGarageBtn = document.getElementById("close-garage");
const garageCarsEl = document.getElementById("garage-cars");
const garageListEl = document.getElementById("garage-list");
const garageForm = document.getElementById("garage-form");
const garageModelInput = document.getElementById("garage-model-input");

const contactOverlay = document.getElementById("contact-overlay");
const closeContactBtn = document.getElementById("close-contact");
const contactForm = document.getElementById("contact-form");

const productOverlay = document.getElementById("product-overlay");
const closeProductBtn = document.getElementById("close-product");
const productDetailBodyEl = document.getElementById("product-detail-body");

const toastEl = document.getElementById("toast");

function switchTab(tab) {
  if (tab === "favorites") {
    favoritesOverlay.classList.remove("hidden");
    return;
  }
  if (tab === "cart") {
    cartOverlay.classList.remove("hidden");
    return;
  }
  state.activeTab = tab;
  tabHomeEl.classList.toggle("hidden", tab !== "home");
  tabCatalogEl.classList.toggle("hidden", tab !== "catalog");
  bottomNavItems.forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === tab));
  window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
}

bottomNavItems.forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function saveJSON(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

state.favorites = loadJSON("fourmatic_favorites", []);
state.garage = loadJSON("fourmatic_garage", []);

let toastTimer = null;
function showToast(message) {
  toastEl.textContent = message;
  toastEl.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.add("hidden"), 2600);
}

function formatPrice(value) {
  if (value === null || value === undefined) return "Узнать цену";
  return `${value.toLocaleString("ru-RU")} ₽`;
}

async function loadInitial() {
  renderSkeleton();
  const [configRes, productsRes] = await Promise.all([
    fetch("/api/config"),
    fetch("/api/products"),
  ]);
  const config = await configRes.json();
  state.paymentsEnabled = Boolean(config.payments_enabled);
  state.products = await productsRes.json();

  renderCategoryGrid();
  renderBrandGrid();
  renderGarage();
  renderProducts();
  updateCartBadge();
  updateFavoritesBadge();
  initHeroSlider();
  initScrollReveal();
}

/* ---------- hero-слайдер ---------- */

function initHeroSlider() {
  const track = document.getElementById("slider-track");
  const dotsEl = document.getElementById("slider-dots");
  if (!track) return;
  const slides = track.querySelectorAll(".hero-slide");
  let index = 0;
  let timer = null;

  dotsEl.innerHTML = Array.from(slides)
    .map((_, i) => `<span class="slider-dot${i === 0 ? " active" : ""}" data-index="${i}"></span>`)
    .join("");
  const dots = dotsEl.querySelectorAll(".slider-dot");

  function goTo(i) {
    index = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
    dots.forEach((d, di) => d.classList.toggle("active", di === index));
  }

  function next() {
    goTo(index + 1);
  }

  function restartTimer() {
    clearInterval(timer);
    timer = setInterval(next, 4200);
  }

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      goTo(Number(dot.dataset.index));
      restartTimer();
    });
  });

  let startX = 0;
  let deltaX = 0;
  track.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
    deltaX = 0;
  }, { passive: true });
  track.addEventListener("touchmove", (e) => {
    deltaX = e.touches[0].clientX - startX;
  }, { passive: true });
  track.addEventListener("touchend", () => {
    if (deltaX > 40) goTo(index - 1);
    else if (deltaX < -40) goTo(index + 1);
    restartTimer();
  });

  goTo(0);
  restartTimer();
}

/* ---------- анимации появления при скролле ---------- */

function initScrollReveal() {
  const targets = document.querySelectorAll(".fade-in");
  if (!("IntersectionObserver" in window)) {
    targets.forEach((el) => el.classList.add("in-view"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  targets.forEach((el) => observer.observe(el));
}

function renderSkeleton() {
  productGridEl.innerHTML = Array.from({ length: 6 })
    .map(
      () => `
      <div class="skeleton-card">
        <div class="skeleton-block"></div>
        <div class="skeleton-lines">
          <div class="skeleton-block" style="width:60%"></div>
          <div class="skeleton-block" style="width:85%"></div>
          <div class="skeleton-block" style="width:40%"></div>
        </div>
      </div>`
    )
    .join("");
}

function categoryCounts() {
  const counts = {};
  state.products.forEach((p) => {
    counts[p.category] = (counts[p.category] || 0) + 1;
  });
  return counts;
}

function brandCounts() {
  const counts = {};
  state.products.forEach((p) => {
    counts[p.brand] = (counts[p.brand] || 0) + 1;
  });
  return counts;
}

function renderCategoryGrid() {
  const counts = categoryCounts();
  const categories = Object.keys(counts).sort();
  categoryGridEl.innerHTML = categories
    .map(
      (cat) => `
      <button class="category-card${state.category === cat ? " active" : ""}" data-category="${escapeAttr(cat)}" type="button">
        ${CATEGORY_ICONS[cat] || ICON_DEFAULT}
        <span class="category-card-label">${escapeHtml(cat)}</span>
      </button>`
    )
    .join("");

  categoryGridEl.querySelectorAll(".category-card").forEach((btn) => {
    btn.addEventListener("click", () => {
      const cat = btn.dataset.category;
      state.category = state.category === cat ? null : cat;
      state.brand = null;
      state.tab = "all";
      syncFilterChips();
      renderCategoryGrid();
      renderBrandGrid();
      renderProducts();
      switchTab("catalog");
    });
  });
}

function renderBrandGrid() {
  const counts = brandCounts();
  const brands = Object.keys(counts).sort();
  brandGridEl.innerHTML = brands
    .map(
      (brand) => `
      <button class="brand-card${state.brand === brand ? " active" : ""}" data-brand="${escapeAttr(brand)}" type="button">
        ${escapeHtml(brand)}
      </button>`
    )
    .join("");

  brandGridEl.querySelectorAll(".brand-card").forEach((btn) => {
    btn.addEventListener("click", () => {
      const brand = btn.dataset.brand;
      state.brand = state.brand === brand ? null : brand;
      state.category = null;
      state.tab = "all";
      syncFilterChips();
      renderCategoryGrid();
      renderBrandGrid();
      renderProducts();
      switchTab("catalog");
    });
  });
}

function syncFilterChips() {
  filtersEl.querySelectorAll(".filter-chip").forEach((chip) => {
    chip.classList.toggle("active", chip.dataset.tab === state.tab);
  });
}

function updateActiveFilterRow() {
  const label = state.category || state.brand;
  if (label) {
    activeFilterRowEl.classList.remove("hidden");
    activeFilterLabelEl.textContent = `Фильтр: ${label}`;
  } else {
    activeFilterRowEl.classList.add("hidden");
  }
}

clearFilterBtn.addEventListener("click", () => {
  state.category = null;
  state.brand = null;
  renderCategoryGrid();
  renderBrandGrid();
  renderProducts();
});

filtersEl.addEventListener("click", (event) => {
  const chip = event.target.closest(".filter-chip");
  if (!chip) return;
  state.tab = chip.dataset.tab;
  syncFilterChips();
  renderProducts();
});

function matchesSearch(product, query) {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  const haystack = [
    product.name,
    product.brand,
    product.oem,
    ...(product.compatible_models || []),
  ]
    .join(" ")
    .toLowerCase();
  return haystack.includes(q);
}

function filteredProducts() {
  return state.products.filter((p) => {
    if (state.tab === "hit" && !p.is_hit) return false;
    if (state.tab === "new" && !p.is_new) return false;
    if (state.category && p.category !== state.category) return false;
    if (state.brand && p.brand !== state.brand) return false;
    if (!matchesSearch(p, state.search)) return false;
    return true;
  });
}

function productCardHtml(product, index) {
  const isFav = state.favorites.includes(product.id);
  const stockClass = product.price_on_request ? "out" : product.in_stock ? "in" : "out";
  const stockLabel = product.price_on_request ? "Под запрос" : product.in_stock ? "В наличии" : "Под заказ";
  const badge = product.is_hit ? "Хит" : product.is_new ? "Новинка" : "";
  return `
    <article class="product-card" data-id="${escapeAttr(product.id)}" style="--card-index:${index % 12}">
      ${badge ? `<span class="product-badge">${badge}</span>` : ""}
      <button class="favorite-toggle${isFav ? " active" : ""}" data-fav="${escapeAttr(product.id)}" type="button">${HEART_ICON}</button>
      <img src="${escapeAttr(product.image)}" alt="${escapeAttr(product.name)}" loading="lazy" />
      <div class="product-info">
        <span class="product-brand">${escapeHtml(product.brand)}</span>
        <span class="product-oem">OEM ${escapeHtml(product.oem || "—")}</span>
        <span class="product-name">${escapeHtml(product.name)}</span>
        <div class="product-price-row">
          <span class="product-price">${formatPrice(product.price)}</span>
          <span class="stock-dot ${stockClass}">${stockLabel}</span>
        </div>
      </div>
    </article>`;
}

const PAGE_SIZE = 20;

function renderProducts(resetPage = true) {
  if (resetPage) state.visibleCount = PAGE_SIZE;
  updateActiveFilterRow();
  const all = filteredProducts();
  const items = all.slice(0, state.visibleCount || PAGE_SIZE);
  productGridEl.classList.add("grid-leaving");
  setTimeout(() => {
    if (!items.length) {
      productGridEl.innerHTML = `<div class="cart-empty">Ничего не найдено. Попробуйте другой запрос.</div>`;
    } else {
      productGridEl.innerHTML = items.map((p, i) => productCardHtml(p, i)).join("");
    }
    productGridEl.classList.remove("grid-leaving");
    loadMoreBtn.classList.toggle("hidden", items.length >= all.length);

    productGridEl.querySelectorAll(".product-card").forEach((card) => {
      card.addEventListener("click", (e) => {
        if (e.target.closest(".favorite-toggle")) return;
        openProductDetail(card.dataset.id);
      });
    });

    productGridEl.querySelectorAll(".favorite-toggle").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleFavorite(btn.dataset.fav);
      });
    });
  }, 120);
}

loadMoreBtn.addEventListener("click", () => {
  state.visibleCount = (state.visibleCount || PAGE_SIZE) + PAGE_SIZE;
  renderProducts(false);
});

vinSearchBtn.addEventListener("click", () => {
  state.search = vinInputEl.value;
  state.category = null;
  state.brand = null;
  state.tab = "all";
  syncFilterChips();
  renderCategoryGrid();
  renderBrandGrid();
  renderProducts();
  switchTab("catalog");
});

vinInputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") vinSearchBtn.click();
});

/* ---------- избранное ---------- */

function toggleFavorite(id) {
  const idx = state.favorites.indexOf(id);
  if (idx >= 0) {
    state.favorites.splice(idx, 1);
  } else {
    state.favorites.push(id);
    showToast("Добавлено в избранное");
  }
  saveJSON("fourmatic_favorites", state.favorites);
  updateFavoritesBadge();
  renderProducts();
  if (!productOverlay.classList.contains("hidden")) {
    const current = state.products.find((p) => p.id === productOverlay.dataset.productId);
    if (current) renderProductDetail(current);
  }
}

function updateFavoritesBadge() {
  if (state.favorites.length > 0) {
    favoritesCountEl.textContent = state.favorites.length;
    favoritesCountEl.classList.remove("hidden");
  } else {
    favoritesCountEl.classList.add("hidden");
  }
}

function renderFavorites() {
  const items = state.products.filter((p) => state.favorites.includes(p.id));
  if (!items.length) {
    favoritesItemsEl.innerHTML = `<div class="cart-empty">Пока пусто. Нажмите на сердечко на карточке товара.</div>`;
    return;
  }
  favoritesItemsEl.innerHTML = items
    .map(
      (p) => `
      <div class="cart-item" data-id="${escapeAttr(p.id)}">
        <img src="${escapeAttr(p.image)}" alt="" />
        <div class="cart-item-info">
          <div class="cart-item-name">${escapeHtml(p.name)}</div>
          <div class="cart-item-price">${formatPrice(p.price)}</div>
        </div>
        <button class="favorite-toggle active" data-fav="${escapeAttr(p.id)}" type="button">${HEART_ICON}</button>
      </div>`
    )
    .join("");

  favoritesItemsEl.querySelectorAll(".cart-item").forEach((row) => {
    row.addEventListener("click", (e) => {
      if (e.target.closest(".favorite-toggle")) return;
      favoritesOverlay.classList.add("hidden");
      openProductDetail(row.dataset.id);
    });
  });

  favoritesItemsEl.querySelectorAll(".favorite-toggle").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleFavorite(btn.dataset.fav);
      renderFavorites();
    });
  });
}

favoritesBtn.addEventListener("click", () => {
  renderFavorites();
  favoritesOverlay.classList.remove("hidden");
});
closeFavoritesBtn.addEventListener("click", () => favoritesOverlay.classList.add("hidden"));

/* ---------- гараж ---------- */

function renderGarage() {
  if (!state.garage.length) {
    garageCarsEl.innerHTML = "";
  } else {
    garageCarsEl.innerHTML = state.garage
      .map(
        (car, i) => `<button class="garage-chip" data-index="${i}" type="button">${escapeHtml(car)}</button>`
      )
      .join("");
    garageCarsEl.querySelectorAll(".garage-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const car = state.garage[Number(chip.dataset.index)];
        state.search = car;
        vinInputEl.value = car;
        state.category = null;
        state.brand = null;
        renderCategoryGrid();
        renderBrandGrid();
        renderProducts();
        productGridEl.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  if (!state.garage.length) {
    garageListEl.innerHTML = `<div class="cart-empty">Автомобилей пока нет</div>`;
  } else {
    garageListEl.innerHTML = state.garage
      .map(
        (car, i) => `
        <div class="garage-list-item">
          <span>${escapeHtml(car)}</span>
          <button class="garage-remove-btn" data-index="${i}" type="button"><svg class="icon" viewBox="0 0 24 24" style="width:15px;height:15px"><path d="M5 5l14 14M19 5L5 19"/></svg></button>
        </div>`
      )
      .join("");
    garageListEl.querySelectorAll(".garage-remove-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.garage.splice(Number(btn.dataset.index), 1);
        saveJSON("fourmatic_garage", state.garage);
        renderGarage();
      });
    });
  }
}

garageManageBtn.addEventListener("click", () => {
  renderGarage();
  garageOverlay.classList.remove("hidden");
});
closeGarageBtn.addEventListener("click", () => garageOverlay.classList.add("hidden"));

garageForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const value = garageModelInput.value.trim();
  if (!value) return;
  state.garage.push(value);
  saveJSON("fourmatic_garage", state.garage);
  garageModelInput.value = "";
  renderGarage();
  showToast("Автомобиль добавлен в гараж");
});

/* ---------- корзина ---------- */

function cartEntries() {
  return Object.entries(state.cart)
    .filter(([, qty]) => qty > 0)
    .map(([id, qty]) => {
      const product = state.products.find((p) => p.id === id);
      return product ? { product, qty } : null;
    })
    .filter(Boolean);
}

function cartCount() {
  return cartEntries().reduce((sum, { qty }) => sum + qty, 0);
}

function cartTotal() {
  return cartEntries().reduce((sum, { product, qty }) => sum + product.price * qty, 0);
}

function updateCartBadge() {
  const count = cartCount();
  cartCountEl.textContent = count;
  bottomNavCartCountEl.textContent = count;
  bottomNavCartCountEl.classList.toggle("hidden", count === 0);
}

function setQty(id, qty) {
  if (qty <= 0) {
    delete state.cart[id];
  } else {
    state.cart[id] = qty;
  }
  updateCartBadge();
  renderCart();
}

function renderCart() {
  const entries = cartEntries();
  if (!entries.length) {
    cartItemsEl.innerHTML = `<div class="cart-empty">Корзина пуста</div>`;
    checkoutBtn.disabled = true;
  } else {
    cartItemsEl.innerHTML = entries
      .map(
        ({ product, qty }) => `
        <div class="cart-item">
          <img src="${escapeAttr(product.image)}" alt="" />
          <div class="cart-item-info">
            <div class="cart-item-name">${escapeHtml(product.brand)} ${escapeHtml(product.name)}</div>
            <div class="cart-item-price">${formatPrice(product.price)} × ${qty}</div>
            <div class="qty-control" data-product="${escapeAttr(product.id)}">
              <button class="qty-minus" type="button">−</button>
              <span>${qty}</span>
              <button class="qty-plus" type="button">+</button>
            </div>
          </div>
        </div>`
      )
      .join("");
    checkoutBtn.disabled = false;
  }

  cartTotalEl.textContent = formatPrice(cartTotal());
}

cartItemsEl.addEventListener("click", (event) => {
  const qtyControl = event.target.closest(".qty-control");
  if (!qtyControl) return;
  const { product } = qtyControl.dataset;
  const current = state.cart[product] || 0;
  if (event.target.closest(".qty-plus")) setQty(product, current + 1);
  if (event.target.closest(".qty-minus")) setQty(product, current - 1);
});

cartBtn.addEventListener("click", () => {
  renderCart();
  cartOverlay.classList.remove("hidden");
});
closeCartBtn.addEventListener("click", () => cartOverlay.classList.add("hidden"));

checkoutBtn.addEventListener("click", () => {
  if (!cartEntries().length) return;
  cartOverlay.classList.add("hidden");
  contactOverlay.classList.remove("hidden");
});
closeContactBtn.addEventListener("click", () => contactOverlay.classList.add("hidden"));

contactForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!cartEntries().length) return;

  const submitBtn = document.getElementById("submit-order-btn");
  const formData = new FormData(contactForm);
  const contact = {
    name: formData.get("name")?.toString().trim() || "",
    phone: formData.get("phone")?.toString().trim() || "",
    car_model: formData.get("car_model")?.toString().trim() || "",
    address: formData.get("address")?.toString().trim() || "",
    delivery_method: formData.get("delivery_method")?.toString() || "russian_post",
    payment_method: formData.get("payment_method")?.toString() || "transfer",
  };

  if (!contact.name || !contact.phone) {
    showToast("Заполните имя и телефон.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Отправляем…";

  try {
    const items = cartEntries().map(({ product, qty }) => ({ id: product.id, qty }));
    const response = await fetch("/api/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData: tg?.initData || "", items, contact }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "checkout_failed");
    }
    state.cart = {};
    updateCartBadge();
    renderCart();
    contactForm.reset();
    contactOverlay.classList.add("hidden");
    showToast(`Заказ №${data.order_id} отправлен! Мы свяжемся с вами в этом чате.`);
  } catch (err) {
    showToast("Не удалось отправить заказ. Попробуйте ещё раз.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Отправить заказ";
  }
});

/* ---------- детальный просмотр товара ---------- */

function openProductDetail(id) {
  const product = state.products.find((p) => p.id === id);
  if (!product) return;
  renderProductDetail(product);
  productOverlay.classList.remove("hidden");
}

function renderProductDetail(product) {
  productOverlay.dataset.productId = product.id;
  const isFav = state.favorites.includes(product.id);
  const compatTags = (product.compatible_models || [])
    .map((m) => `<span class="compat-tag">${escapeHtml(m)}</span>`)
    .join("");
  const inCart = state.cart[product.id] || 0;

  productDetailBodyEl.innerHTML = `
    <img class="product-detail-image" src="${escapeAttr(product.image)}" alt="${escapeAttr(product.name)}" />
    <div class="product-detail-name">${escapeHtml(product.name)}</div>
    <div class="product-detail-meta">
      <span>Бренд: ${escapeHtml(product.brand)}</span>
      <span>OEM-номер: ${escapeHtml(product.oem || "—")}</span>
    </div>
    <p class="product-detail-description">${escapeHtml(product.description || "")}</p>
    ${
      compatTags
        ? `<div class="compat-block">
            <div class="compat-block-title">Совместимость</div>
            <div class="compat-tags">${compatTags}</div>
          </div>`
        : ""
    }
    <div class="detail-price-row">
      <div>
        <div class="detail-price">${formatPrice(product.price)}</div>
        <div class="detail-availability">${product.price_on_request ? "Цена уточняется у поставщика" : product.in_stock ? "В наличии" : "Под заказ"} · доставка ${escapeHtml(product.delivery_days || "—")} дн.</div>
      </div>
    </div>
    <div class="detail-actions">
      <button class="favorite-btn-detail${isFav ? " active" : ""}" id="detail-fav-btn" type="button">${HEART_ICON}</button>
      <button class="quick-order-btn" id="detail-quick-order-btn" type="button" ${product.in_stock && !product.price_on_request ? "" : "disabled"}>Купить в 1 клик</button>
      <button class="add-btn" id="detail-add-btn" type="button" ${product.in_stock && !product.price_on_request ? "" : "disabled"}>${inCart > 0 ? `В корзине: ${inCart}` : "В корзину"}</button>
    </div>
  `;

  document.getElementById("detail-fav-btn").addEventListener("click", () => toggleFavorite(product.id));

  document.getElementById("detail-add-btn").addEventListener("click", () => {
    setQty(product.id, (state.cart[product.id] || 0) + 1);
    renderProductDetail(product);
    showToast("Добавлено в корзину");
  });

  document.getElementById("detail-quick-order-btn").addEventListener("click", () => {
    setQty(product.id, (state.cart[product.id] || 0) + 1);
    productOverlay.classList.add("hidden");
    cartOverlay.classList.add("hidden");
    contactOverlay.classList.remove("hidden");
  });
}

closeProductBtn.addEventListener("click", () => productOverlay.classList.add("hidden"));

/* ---------- утилиты ---------- */

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[ch]);
}

function escapeAttr(value) {
  return escapeHtml(value);
}

loadInitial();
