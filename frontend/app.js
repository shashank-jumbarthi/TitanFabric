const fabrics = [
  {
    id: "tf-linen-01",
    name: "Harbor Washed Linen",
    category: "linen",
    composition: "100% European flax linen",
    finish: "enzyme washed",
    weightGsm: 185,
    widthIn: 56,
    minYards: 25,
    price: 14.8,
    leadTime: 12,
    sustainable: true,
    colorways: ["oat", "indigo", "sage", "charcoal"],
  },
  {
    id: "tf-cotton-02",
    name: "Studio Organic Poplin",
    category: "cotton",
    composition: "100% GOTS organic cotton",
    finish: "soft mercerized",
    weightGsm: 118,
    widthIn: 58,
    minYards: 40,
    price: 9.6,
    leadTime: 9,
    sustainable: true,
    colorways: ["white", "ink", "coral", "moss"],
  },
  {
    id: "tf-denim-03",
    name: "Foundry Stretch Denim",
    category: "denim",
    composition: "97% cotton, 3% elastane",
    finish: "rinse ready",
    weightGsm: 340,
    widthIn: 61,
    minYards: 60,
    price: 12.4,
    leadTime: 16,
    sustainable: false,
    colorways: ["raw", "mid blue", "washed black"],
  },
  {
    id: "tf-silk-04",
    name: "Atelier Silk Twill",
    category: "silk",
    composition: "100% mulberry silk",
    finish: "print ready",
    weightGsm: 92,
    widthIn: 45,
    minYards: 15,
    price: 28,
    leadTime: 18,
    sustainable: false,
    colorways: ["ivory", "navy", "ruby"],
  },
  {
    id: "tf-recycled-05",
    name: "Loop Recycled Fleece",
    category: "knit",
    composition: "72% recycled cotton, 28% recycled polyester",
    finish: "brushed back",
    weightGsm: 280,
    widthIn: 63,
    minYards: 50,
    price: 11.2,
    leadTime: 14,
    sustainable: true,
    colorways: ["heather gray", "forest", "clay", "black"],
  },
];

const state = {
  category: "all",
  sustainableOnly: false,
  maxPrice: 30,
  quote: new Map(),
  destination: "domestic",
};

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

const catalogGrid = document.querySelector("#catalogGrid");
const categoryFilter = document.querySelector("#categoryFilter");
const sustainableFilter = document.querySelector("#sustainableFilter");
const priceFilter = document.querySelector("#priceFilter");
const priceLabel = document.querySelector("#priceLabel");
const quoteItems = document.querySelector("#quoteItems");
const subtotalEl = document.querySelector("#subtotal");
const shippingEl = document.querySelector("#shipping");
const serviceEl = document.querySelector("#service");
const totalEl = document.querySelector("#total");
const quoteForm = document.querySelector("#quoteForm");
const formStatus = document.querySelector("#formStatus");

function filteredFabrics() {
  return fabrics.filter((fabric) => {
    const matchesCategory = state.category === "all" || fabric.category === state.category;
    const matchesSustainable = !state.sustainableOnly || fabric.sustainable;
    const matchesPrice = fabric.price <= state.maxPrice;
    return matchesCategory && matchesSustainable && matchesPrice;
  });
}

function renderCatalog() {
  const visible = filteredFabrics();
  catalogGrid.innerHTML = visible.map((fabric) => {
    const existing = state.quote.get(fabric.id);
    const yards = existing?.yards || fabric.minYards;
    return `
      <article class="fabric-card">
        <div class="fabric-top">
          <div>
            <h3>${fabric.name}</h3>
            <p>${fabric.composition}</p>
          </div>
          <span class="tag">${fabric.sustainable ? "Sustainable" : fabric.category}</span>
        </div>
        <dl class="specs">
          <div><dt>Finish</dt><dd>${fabric.finish}</dd></div>
          <div><dt>Weight</dt><dd>${fabric.weightGsm} GSM</dd></div>
          <div><dt>Width</dt><dd>${fabric.widthIn} in</dd></div>
          <div><dt>Minimum</dt><dd>${fabric.minYards} yd</dd></div>
          <div><dt>Lead time</dt><dd>${fabric.leadTime} days</dd></div>
          <div><dt>Price</dt><dd>${currency.format(fabric.price)}/yd</dd></div>
        </dl>
        <div class="colorways" aria-label="Colorways">
          ${fabric.colorways.map((color) => `<span>${color}</span>`).join("")}
        </div>
        <div class="card-actions">
          <input type="number" min="${fabric.minYards}" value="${yards}" data-yards="${fabric.id}" aria-label="Yards for ${fabric.name}">
          <button class="button primary" type="button" data-add="${fabric.id}">Add</button>
        </div>
      </article>
    `;
  }).join("");
}

function calculateQuote() {
  const items = Array.from(state.quote.values());
  const subtotal = items.reduce((sum, item) => sum + item.yards * item.fabric.price, 0);
  const shipping = subtotal * (state.destination === "international" ? 0.08 : 0.035);
  const service = subtotal > 0 ? 35 : 0;
  return {
    items,
    subtotal,
    shipping,
    service,
    total: subtotal + shipping + service,
  };
}

function renderQuote() {
  const quote = calculateQuote();
  if (!quote.items.length) {
    quoteItems.innerHTML = "<p>No fabrics selected yet.</p>";
  } else {
    quoteItems.innerHTML = quote.items.map((item) => `
      <div class="quote-item">
        <div>
          <strong>${item.fabric.name}</strong>
          <span>${item.yards} yd at ${currency.format(item.fabric.price)}/yd</span>
        </div>
        <strong>${currency.format(item.yards * item.fabric.price)}</strong>
        <button class="icon-button" type="button" title="Remove ${item.fabric.name}" data-remove="${item.fabric.id}">x</button>
      </div>
    `).join("");
  }

  subtotalEl.textContent = currency.format(quote.subtotal);
  shippingEl.textContent = currency.format(quote.shipping);
  serviceEl.textContent = currency.format(quote.service);
  totalEl.textContent = currency.format(quote.total);
}

function addFabric(fabricId) {
  const fabric = fabrics.find((item) => item.id === fabricId);
  const yardsInput = document.querySelector(`[data-yards="${fabricId}"]`);
  const requestedYards = Number(yardsInput?.value || fabric.minYards);
  const yards = Math.max(requestedYards, fabric.minYards);
  state.quote.set(fabricId, { fabric, yards });
  renderCatalog();
  renderQuote();
}

catalogGrid.addEventListener("click", (event) => {
  const addButton = event.target.closest("[data-add]");
  if (addButton) {
    addFabric(addButton.dataset.add);
  }
});

quoteItems.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove]");
  if (removeButton) {
    state.quote.delete(removeButton.dataset.remove);
    renderCatalog();
    renderQuote();
  }
});

categoryFilter.addEventListener("change", (event) => {
  state.category = event.target.value;
  renderCatalog();
});

sustainableFilter.addEventListener("change", (event) => {
  state.sustainableOnly = event.target.checked;
  renderCatalog();
});

priceFilter.addEventListener("input", (event) => {
  state.maxPrice = Number(event.target.value);
  priceLabel.textContent = `$${state.maxPrice}/yd`;
  renderCatalog();
});

quoteForm.destination.addEventListener("change", (event) => {
  state.destination = event.target.value;
  renderQuote();
});

quoteForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const quote = calculateQuote();
  if (!quote.items.length) {
    formStatus.textContent = "Add at least one fabric before sending a quote request.";
    return;
  }

  const formData = new FormData(quoteForm);
  const payload = {
    customer_name: formData.get("name"),
    email: formData.get("email"),
    destination: formData.get("destination"),
    notes: formData.get("notes"),
    items: quote.items.map((item) => ({
      fabric_id: item.fabric.id,
      yards: item.yards,
    })),
    estimate_total: Number(quote.total.toFixed(2)),
  };

  console.info("TitanFabric quote request", payload);
  formStatus.textContent = `Quote request ready for ${payload.customer_name}: ${currency.format(quote.total)} estimated.`;
  quoteForm.reset();
  state.destination = "domestic";
});

renderCatalog();
renderQuote();
