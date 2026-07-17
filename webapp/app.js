const tg = window.Telegram?.WebApp;

if (tg) {
  tg.ready();
  tg.expand();
}

const state = {
  products: [],
  tab: "all", // all | hit | new
  category: "all",
  cart: {}, // { productId: qty }
  paymentsEnabled: false,
  search: "",
};

const grid = document.getElementById("product-grid");
const searchInput = document.getElementById("search-input");
const categoryRailEl = document.getElementById("category-rail");
const cartBtn = document.getElementById("cart-btn");
const cartCount = document.getElementById("cart-count");
const cartOverlay = document.getElementById("cart-overlay");
const cartItemsEl = document.getElementById("cart-items");
const cartTotalEl = document.getElementById("cart-total");
const closeCartBtn = document.getElementById("close-cart");
const checkoutBtn = document.getElementById("checkout-btn");
const filtersEl = document.getElementById("filters");
const toastEl = document.getElementById("toast");
const contactOverlay = document.getElementById("contact-overlay");
const closeContactBtn = document.getElementById("close-contact");
const contactForm = document.getElementById("contact-form");
const productOverlay = document.getElementById("product-overlay");
const productDetailBody = document.getElementById("product-detail-body");
const closeProductBtn = document.getElementById("close-product");

function formatPrice(value) {
  return `${value.toLocaleString("ru-RU")} ₽`;
}

function showToast(message) {
  toastEl.textContent = message;
  toastEl.classList.remove("hidden");
  setTimeout(() => toastEl.classList.add("hidden"), 2500);
}

function getProduct(id) {
  return state.products.find((p) => p.id === id);
}

function cartQty(productId) {
  return state.cart[productId] || 0;
}

function cartEntries() {
  return Object.entries(state.cart)
    .filter(([, qty]) => qty > 0)
    .map(([productId, qty]) => ({ productId, qty, product: getProduct(productId) }))
    .filter((entry) => entry.product);
}

function cartTotal() {
  return cartEntries().reduce((sum, entry) => sum + entry.product.price * entry.qty, 0);
}

function cartItemsCount() {
  return cartEntries().reduce((sum, entry) => sum + entry.qty, 0);
}

function setQty(productId, qty) {
  state.cart[productId] = Math.max(0, qty);
  renderCartBadge();
  renderCart();
  if (!productOverlay.classList.contains("hidden") && productOverlay.dataset.productId === productId) {
    renderProductDetail(productId);
  }
}

function renderCartBadge() {
  cartCount.textContent = cartItemsCount();
}

function renderFilters() {
  filtersEl.querySelectorAll(".filter-chip").forEach((chip) => {
    chip.classList.toggle("active", chip.dataset.tab === state.tab);
  });
}

function matchesSearch(product) {
  const q = state.search.trim().toLowerCase();
  if (!q) return true;
  const models = (product.compatible_models || []).join(" ").toLowerCase();
  return (
    product.name.toLowerCase().includes(q) ||
    product.brand.toLowerCase().includes(q) ||
    models.includes(q)
  );
}

function matchesCategory(product) {
  return state.category === "all" || product.category === state.category;
}

function visibleProducts() {
  let list = state.products;
  if (state.tab === "hit") list = list.filter((p) => p.is_hit);
  else if (state.tab === "new") list = list.filter((p) => p.is_new);
  return list.filter(matchesCategory).filter(matchesSearch);
}

function categoryCounts() {
  const counts = new Map();
  state.products.forEach((p) => counts.set(p.category, (counts.get(p.category) || 0) + 1));
  return [...counts.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

function renderCategoryRail() {
  const categories = categoryCounts();
  const allChip = `<button class="category-chip${state.category === "all" ? " active" : ""}" data-category="all">
      <span>Все категории</span><span class="category-chip-count">${state.products.length}</span>
    </button>`;
  const chips = categories
    .map(
      ([category, count]) => `
    <button class="category-chip${state.category === category ? " active" : ""}" data-category="${category}">
      <span>${category}</span><span class="category-chip-count">${count}</span>
    </button>`
    )
    .join("");
  categoryRailEl.innerHTML = allChip + chips;
}

function addControlHtml(product) {
  const qty = cartQty(product.id);
  if (!product.in_stock) {
    return `<button class="add-btn" disabled>Нет в наличии</button>`;
  }
  if (qty > 0) {
    return `<div class="qty-control" data-product="${product.id}">
         <button class="qty-minus" type="button">−</button>
         <span>${qty}</span>
         <button class="qty-plus" type="button">+</button>
       </div>`;
  }
  return `<button class="add-btn" data-product="${product.id}" type="button">Добавить</button>`;
}

function productCardHtml(product) {
  const badge = product.is_hit ? "🏆 Хит" : product.is_new ? "🆕 Новинка" : "";
  return `
    <div class="product-card" data-product-id="${product.id}">
      ${badge ? `<span class="product-badge">${badge}</span>` : ""}
      <img src="${product.image}" alt="${product.name}" loading="lazy" />
      <div class="product-info">
        <span class="product-brand">${product.brand}</span>
        <span class="product-name">${product.name}</span>
        ${product.description ? `<p class="product-description">${product.description}</p>` : ""}
        <div class="product-price-row">
          <span class="product-price">${formatPrice(product.price)}</span>
        </div>
      </div>
    </div>
  `;
}

function renderGrid() {
  const products = visibleProducts();
  grid.innerHTML = products.length
    ? products.map(productCardHtml).join("")
    : '<p class="cart-empty">Ничего не найдено</p>';
}

function renderProductDetail(productId) {
  const product = getProduct(productId);
  if (!product) return;

  const models = product.compatible_models && product.compatible_models.length
    ? `<p class="product-detail-models">Подходит: ${product.compatible_models.join(", ")}</p>`
    : "";

  productDetailBody.innerHTML = `
    <img src="${product.image}" alt="${product.name}" class="product-detail-image" />
    <span class="product-brand">${product.brand}</span>
    <h3 class="product-detail-name">${product.name}</h3>
    ${models}
    ${product.description ? `<p class="product-detail-description">${product.description}</p>` : ""}
    <div class="detail-price-row">
      <span class="detail-price">${formatPrice(product.price)}</span>
      ${addControlHtml(product)}
    </div>
  `;
}

function openProductDetail(productId) {
  renderProductDetail(productId);
  productOverlay.dataset.productId = productId;
  productOverlay.classList.remove("hidden");
}

function cartItemHtml(entry) {
  const { product, qty } = entry;
  return `
    <div class="cart-item">
      <img src="${product.image}" alt="${product.name}" />
      <div class="cart-item-info">
        <div class="cart-item-name">${product.brand} ${product.name}</div>
        <div class="cart-item-price">${formatPrice(product.price)} × ${qty}</div>
      </div>
      <div class="qty-control" data-product="${product.id}">
        <button class="qty-minus" type="button">−</button>
        <span>${qty}</span>
        <button class="qty-plus" type="button">+</button>
      </div>
    </div>
  `;
}

function renderCart() {
  const entries = cartEntries();
  cartItemsEl.innerHTML = entries.length
    ? entries.map(cartItemHtml).join("")
    : '<div class="cart-empty">Корзина пуста</div>';
  cartTotalEl.textContent = formatPrice(cartTotal());
  checkoutBtn.disabled = entries.length === 0;
}

grid.addEventListener("click", (event) => {
  const card = event.target.closest(".product-card[data-product-id]");
  if (!card) return;
  openProductDetail(card.dataset.productId);
});

productDetailBody.addEventListener("click", (event) => {
  const addBtn = event.target.closest(".add-btn[data-product]");
  if (addBtn) {
    setQty(addBtn.dataset.product, cartQty(addBtn.dataset.product) + 1);
    return;
  }
  const qtyControl = event.target.closest(".qty-control");
  if (qtyControl) {
    const { product } = qtyControl.dataset;
    if (event.target.closest(".qty-plus")) setQty(product, cartQty(product) + 1);
    if (event.target.closest(".qty-minus")) setQty(product, cartQty(product) - 1);
  }
});

closeProductBtn.addEventListener("click", () => {
  productOverlay.classList.add("hidden");
});

cartItemsEl.addEventListener("click", (event) => {
  const qtyControl = event.target.closest(".qty-control");
  if (!qtyControl) return;
  const { product } = qtyControl.dataset;
  if (event.target.closest(".qty-plus")) setQty(product, cartQty(product) + 1);
  if (event.target.closest(".qty-minus")) setQty(product, cartQty(product) - 1);
});

function renderGridAnimated() {
  grid.classList.add("grid-leaving");
  window.setTimeout(() => {
    renderGrid();
    grid.classList.remove("grid-leaving");
  }, 150);
}

filtersEl.addEventListener("click", (event) => {
  const chip = event.target.closest(".filter-chip");
  if (!chip) return;
  if (chip.dataset.tab === state.tab) return;
  state.tab = chip.dataset.tab;
  renderFilters();
  renderGridAnimated();
});

categoryRailEl.addEventListener("click", (event) => {
  const chip = event.target.closest(".category-chip");
  if (!chip) return;
  if (chip.dataset.category === state.category) return;
  state.category = chip.dataset.category;
  renderCategoryRail();
  renderGridAnimated();
});

searchInput.addEventListener("input", () => {
  state.search = searchInput.value;
  renderGrid();
});

cartBtn.addEventListener("click", () => {
  renderCart();
  cartOverlay.classList.remove("hidden");
});

closeCartBtn.addEventListener("click", () => {
  cartOverlay.classList.add("hidden");
});

function clearCartAndClose() {
  state.cart = {};
  renderCartBadge();
  renderCart();
  cartOverlay.classList.add("hidden");
  contactOverlay.classList.add("hidden");
}

async function submitOrder(extraPayload) {
  const items = cartEntries().map((entry) => ({ id: entry.productId, qty: entry.qty }));
  const response = await fetch("/api/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initData: tg?.initData || "", items, ...extraPayload }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "checkout_failed");
  }
  return data;
}

checkoutBtn.addEventListener("click", async () => {
  if (cartEntries().length === 0) return;

  if (!state.paymentsEnabled) {
    cartOverlay.classList.add("hidden");
    contactOverlay.classList.remove("hidden");
    return;
  }

  checkoutBtn.disabled = true;
  checkoutBtn.textContent = "Оформляем...";

  try {
    const data = await submitOrder({});
    if (tg?.openInvoice) {
      tg.openInvoice(data.invoice_link, (status) => {
        if (status === "paid") {
          clearCartAndClose();
          showToast("Оплата прошла успешно!");
        } else if (status === "failed") {
          showToast("Оплата не прошла.");
        }
      });
    } else {
      window.open(data.invoice_link, "_blank");
    }
  } catch (err) {
    showToast("Не удалось оформить заказ. Попробуйте ещё раз.");
  } finally {
    checkoutBtn.disabled = cartEntries().length === 0;
    checkoutBtn.textContent = "Оформить заказ";
  }
});

contactForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (cartEntries().length === 0) return;

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
  submitBtn.textContent = "Отправляем...";

  try {
    const data = await submitOrder({ contact });
    clearCartAndClose();
    contactForm.reset();
    showToast(`Заказ №${data.order_id} отправлен! Мы свяжемся с вами в этом чате.`);
  } catch (err) {
    showToast("Не удалось отправить заказ. Попробуйте ещё раз.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Отправить заказ";
  }
});

closeContactBtn.addEventListener("click", () => {
  contactOverlay.classList.add("hidden");
});

async function loadConfig() {
  const response = await fetch("/api/config");
  const data = await response.json();
  state.paymentsEnabled = Boolean(data.payments_enabled);
}

async function loadProducts() {
  const response = await fetch("/api/products");
  state.products = await response.json();
  renderCategoryRail();
  renderGrid();
}

Promise.all([loadConfig(), loadProducts()]);
