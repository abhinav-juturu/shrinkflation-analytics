/**
 * Interactive Application Logic for Shrinkflation Case Study
 */

// Embedded SKU analytical dataset
let skuData = [];
let brandData = [];
let scatterChartInstance = null;
let donutChartInstance = null;
let brandBarChartInstance = null;
let skuTimelineChartInstance = null;

// Benchmark SKUs with wave profiles
const BENCHMARK_WAVES = {
  "BIS-PAR-001": {
    name: "Parle-G Original Glucose Biscuits (₹5)",
    brand: "Parle-G",
    company: "Parle Products",
    category: "Biscuits & Bakery",
    quadrant: "Q2: Silent Shrinkflation",
    isMagic: "Yes (₹5 Pack)",
    packType: "Flexible Pillow Pouch",
    claim: "New Richer Taste, Crispier Bite",
    weights: [65.0, 60.0, 55.0, 55.0, 50.0, 50.0],
    prices: [5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    shrinkShare: 100,
    priceShare: 0,
    stealthIdx: 0.77
  },
  "SNK-NES-001": {
    name: "Maggi 2-Minute Masala Noodles (₹12→14)",
    brand: "Maggi",
    company: "Nestle India",
    category: "Snacks & Instant Foods",
    quadrant: "Q3: Double Whammy",
    isMagic: "Yes (₹10-15 Pack)",
    packType: "Pillow Pouch",
    claim: "Goodness of Iron, Signature Taste",
    weights: [80.0, 75.0, 75.0, 70.0, 70.0, 68.0],
    prices: [12.0, 12.0, 14.0, 14.0, 14.0, 14.0],
    shrinkShare: 52,
    priceShare: 48,
    stealthIdx: 0.41
  },
  "SNK-HLD-001": {
    name: "Haldiram's Nagpur Aloo Bhujia (₹10)",
    brand: "Haldiram's",
    company: "Haldiram Snacks",
    category: "Snacks & Instant Foods",
    quadrant: "Q2: Silent Shrinkflation",
    isMagic: "Yes (₹10 Pack)",
    packType: "Laminate Pouch",
    claim: "Taste of Tradition, Royal Crispy Pack",
    weights: [55.0, 50.0, 46.0, 42.0, 40.0, 38.0],
    prices: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    shrinkShare: 100,
    priceShare: 0,
    stealthIdx: 0.69
  },
  "HOM-HUL-001": {
    name: "Vim Dishwash Bar (₹10)",
    brand: "Vim",
    company: "Hindustan Unilever",
    category: "Home Care & Cleaning",
    quadrant: "Q2: Silent Shrinkflation",
    isMagic: "Yes (₹10 Pack)",
    packType: "Poly Wrap",
    claim: "Anti-Soggy Base, Zero Wastage",
    weights: [155.0, 145.0, 135.0, 130.0, 120.0, 115.0],
    prices: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    shrinkShare: 100,
    priceShare: 0,
    stealthIdx: 0.74
  },
  "HOM-HUL-002": {
    name: "Surf Excel Easy Wash Detergent Powder (1kg)",
    brand: "Surf Excel",
    company: "Hindustan Unilever",
    category: "Home Care & Cleaning",
    quadrant: "Q1: Overt Inflation",
    isMagic: "No (Standard 1kg)",
    packType: "Poly Bag",
    claim: "Advanced Enzyme Action",
    weights: [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0],
    prices: [120.0, 125.0, 132.0, 138.0, 144.0, 150.0],
    shrinkShare: 0,
    priceShare: 100,
    stealthIdx: 0.0
  },
  "STA-TAT-001": {
    name: "Tata Salt Vacuum Evaporated Iodised (1kg)",
    brand: "Tata Salt",
    company: "Tata Consumer Products",
    category: "Cooking Staples & Condiments",
    quadrant: "Q1: Overt Inflation",
    isMagic: "No (Standard 1kg)",
    packType: "LDPE Pouch",
    claim: "Desh Ka Namak",
    weights: [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0],
    prices: [22.0, 24.0, 25.0, 26.0, 27.0, 28.0],
    shrinkShare: 0,
    priceShare: 100,
    stealthIdx: 0.0
  },
  "BIS-BRT-001": {
    name: "Britannia Good Day Cashew Cookies (₹10)",
    brand: "Good Day",
    company: "Britannia Industries",
    category: "Biscuits & Bakery",
    quadrant: "Q2: Silent Shrinkflation",
    isMagic: "Yes (₹10 Pack)",
    packType: "Flow Wrap",
    claim: "New Smile Design, Extra Cashews",
    weights: [72.0, 67.0, 62.0, 60.0, 58.0, 55.0],
    prices: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    shrinkShare: 100,
    priceShare: 0,
    stealthIdx: 0.76
  },
  "PER-HUL-001": {
    name: "Lifebuoy Total Germ Protection Soap (₹10)",
    brand: "Lifebuoy",
    company: "Hindustan Unilever",
    category: "Personal Care & Soaps",
    quadrant: "Q2: Silent Shrinkflation",
    isMagic: "Yes (₹10 Pack)",
    packType: "Paper Wrapper",
    claim: "Improved Grip Shape, Activ Silver",
    weights: [52.0, 48.0, 45.0, 42.0, 40.0, 38.0],
    prices: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    shrinkShare: 100,
    priceShare: 0,
    stealthIdx: 0.73
  }
};

// Initial setup
document.addEventListener("DOMContentLoaded", async () => {
  setupTabs();
  setupCalculator();
  await loadData();
  renderQuadrantCharts();
  renderBrandScorecard();
  setupSkuTimeline();
});

// Tab navigation handler
function setupTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");
    });
  });
}

// Fetch model metrics and cleaned data
async function loadData() {
  try {
    const res = await fetch("../data/model_metrics.json");
    if (res.ok) {
      const data = await res.json();
      brandData = data.brand_transparency_table;
    }
  } catch (err) {
    console.warn("Using offline fallback data", err);
  }

  // Fallback brand table if running from file:// protocol
  if (!brandData || brandData.length === 0) {
    brandData = [
      { parent_company: "Mondelez India", sku_count: 3, shrink_rate: 1.0, avg_stealth_index: 0.81, avg_unit_price_hike: 23.5, transparency_score: 6.7, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Parle Products", sku_count: 4, shrink_rate: 1.0, avg_stealth_index: 0.78, avg_unit_price_hike: 27.5, transparency_score: 7.6, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "PepsiCo India", sku_count: 6, shrink_rate: 1.0, avg_stealth_index: 0.70, avg_unit_price_hike: 35.0, transparency_score: 10.4, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Haldiram Snacks", sku_count: 3, shrink_rate: 0.67, avg_stealth_index: 0.46, avg_unit_price_hike: 22.0, transparency_score: 33.9, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Nestle India", sku_count: 6, shrink_rate: 0.67, avg_stealth_index: 0.42, avg_unit_price_hike: 20.8, transparency_score: 35.3, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Britannia Industries", sku_count: 5, shrink_rate: 0.60, avg_stealth_index: 0.46, avg_unit_price_hike: 23.9, transparency_score: 36.9, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Hindustan Unilever", sku_count: 13, shrink_rate: 0.69, avg_stealth_index: 0.45, avg_unit_price_hike: 25.4, transparency_score: 37.8, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "ITC Limited", sku_count: 6, shrink_rate: 0.67, avg_stealth_index: 0.43, avg_unit_price_hike: 22.1, transparency_score: 39.0, risk_tier: "High Shrinkflation Risk (Stealth Dominant)" },
      { parent_company: "Reckitt Benckiser", sku_count: 3, shrink_rate: 0.33, avg_stealth_index: 0.17, avg_unit_price_hike: 15.2, transparency_score: 59.2, risk_tier: "Moderate Risk (Mixed Disclosure)" },
      { parent_company: "Tata Consumer Products", sku_count: 3, shrink_rate: 0.0, avg_stealth_index: 0.0, avg_unit_price_hike: 23.4, transparency_score: 100.0, risk_tier: "High Transparency (Pro-Consumer)" },
      { parent_company: "GCMMF (Amul)", sku_count: 3, shrink_rate: 0.0, avg_stealth_index: 0.0, avg_unit_price_hike: 21.0, transparency_score: 100.0, risk_tier: "High Transparency (Pro-Consumer)" }
    ];
  }
}

// Render 4-Quadrant Scatter and Donut
function renderQuadrantCharts() {
  const ctxScatter = document.getElementById("quadrantScatterChart").getContext("2d");
  const ctxDonut = document.getElementById("quadrantDonutChart").getContext("2d");

  // Scatter data points across quadrants
  const scatterPoints = [
    // Q2: Silent Shrink (x: ~0, y: -10 to -35)
    { x: 0, y: -23.1, name: "Parle-G 65g→50g (₹5)", quad: "Q2" },
    { x: 0, y: -23.1, name: "Parle-G Gold 130g→100g (₹10)", quad: "Q2" },
    { x: 0, y: -23.6, name: "Good Day 72g→55g (₹10)", quad: "Q2" },
    { x: 0, y: -17.0, name: "Oreo 50g→41.5g (₹10)", quad: "Q2" },
    { x: 0, y: -33.3, name: "Lay's Chips 30g→20g (₹10)", quad: "Q2" },
    { x: 0, y: -27.1, name: "Kurkure 48g→35g (₹10)", quad: "Q2" },
    { x: 0, y: -30.9, name: "Haldiram's Bhujia 55g→38g (₹10)", quad: "Q2" },
    { x: 0, y: -30.0, name: "Bingo! Angles 40g→28g (₹10)", quad: "Q2" },
    { x: 0, y: -26.1, name: "Lay's Family 115g→85g (₹50)", quad: "Q2" },
    { x: 0, y: -26.9, name: "Lifebuoy Soap 52g→38g (₹10)", quad: "Q2" },
    { x: 0, y: -24.0, name: "Colgate Dental 50g→38g (₹20)", quad: "Q2" },
    { x: 0, y: -25.8, name: "Vim Bar 155g→115g (₹10)", quad: "Q2" },
    { x: 0, y: -25.0, name: "Rin Bar 140g→105g (₹10)", quad: "Q2" },
    { x: 0, y: -28.0, name: "Nestle Whitener 25g→18g (₹10)", quad: "Q2" },

    // Q3: Double Whammy (x: 10 to 25, y: -10 to -25)
    { x: 16.7, y: -15.0, name: "Maggi 2-Min 80g→68g (₹12→14)", quad: "Q3" },
    { x: 25.0, y: -15.0, name: "Dark Fantasy 100g→85g (₹40→50)", quad: "Q3" },
    { x: 20.0, y: -15.0, name: "Dove Bar 100g→85g (₹60→72)", quad: "Q3" },
    { x: 16.0, y: -15.0, name: "Britannia Cheese 200g→170g (₹125→145)", quad: "Q3" },
    { x: 16.7, y: -15.0, name: "Kissan Ketchup 500g→425g (₹60→70)", quad: "Q3" },
    { x: 11.1, y: -25.0, name: "Dettol Bathing Bar 100g→75g (₹36→40)", quad: "Q3" },

    // Q1: Overt Inflation (x: 15 to 30, y: ~0)
    { x: 28.6, y: 0, name: "Marie Gold 300g (₹35→45)", quad: "Q1" },
    { x: 25.0, y: 0, name: "Surf Excel 1kg (₹120→150)", quad: "Q1" },
    { x: 18.8, y: 0, name: "Ariel Matic 1kg (₹240→285)", quad: "Q1" },
    { x: 20.0, y: 0, name: "Amul Butter 100g (₹50→60)", quad: "Q1" },
    { x: 27.3, y: 0, name: "Tata Salt 1kg (₹22→28)", quad: "Q1" },
    { x: 23.8, y: 0, name: "Aashirvaad Atta 5kg (₹210→260)", quad: "Q1" },
    { x: 21.0, y: 0, name: "Amul Pure Ghee 1L (₹550→665)", quad: "Q1" },

    // Q4: Fair / Stable
    { x: 0, y: 0, name: "Tata Tea Gold 250g (₹130)", quad: "Q4" },
    { x: 2.0, y: 0, name: "Fortune Sunflower 1L (Stable)", quad: "Q4" }
  ];

  const getColor = (quad) => {
    if (quad === "Q2") return "#f87171";
    if (quad === "Q3") return "#c084fc";
    if (quad === "Q1") return "#60a5fa";
    return "#4ade80";
  };

  scatterChartInstance = new Chart(ctxScatter, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Q2: Silent Shrink",
          data: scatterPoints.filter(p => p.quad === "Q2"),
          backgroundColor: "#f87171",
          borderColor: "#ef4444",
          pointRadius: 6,
          pointHoverRadius: 9
        },
        {
          label: "Q3: Double Whammy",
          data: scatterPoints.filter(p => p.quad === "Q3"),
          backgroundColor: "#c084fc",
          borderColor: "#a855f7",
          pointRadius: 6,
          pointHoverRadius: 9
        },
        {
          label: "Q1: Overt Inflation",
          data: scatterPoints.filter(p => p.quad === "Q1"),
          backgroundColor: "#60a5fa",
          borderColor: "#3b82f6",
          pointRadius: 6,
          pointHoverRadius: 9
        },
        {
          label: "Q4: Stable Value",
          data: scatterPoints.filter(p => p.quad === "Q4"),
          backgroundColor: "#4ade80",
          borderColor: "#22c55e",
          pointRadius: 6,
          pointHoverRadius: 9
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const p = ctx.raw;
              return `${p.name} | Price: ${p.x > 0 ? '+' : ''}${p.x}% | Weight: ${p.y}%`;
            }
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Nominal Price Change (%)", color: "#94a3b8" },
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: { color: "#94a3b8" },
          min: -5,
          max: 35
        },
        y: {
          title: { display: true, text: "Net Pack Weight Change (%)", color: "#94a3b8" },
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: { color: "#94a3b8" },
          min: -40,
          max: 10
        }
      }
    }
  });

  // Donut chart
  donutChartInstance = new Chart(ctxDonut, {
    type: "doughnut",
    data: {
      labels: ["Q2: Silent Shrink", "Q1: Overt Inflation", "Q3: Double Whammy", "Q4: Stable/Fair"],
      datasets: [
        {
          data: [48.1, 27.2, 13.6, 11.1],
          backgroundColor: ["#f87171", "#60a5fa", "#c084fc", "#4ade80"],
          borderWidth: 2,
          borderColor: "#101622"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: { color: "#cbd5e1", font: { size: 11 } }
        }
      },
      cutout: "65%"
    }
  });

  // Category filter hook
  document.getElementById("quadrant-cat-filter").addEventListener("change", (e) => {
    const val = e.target.value;
    // In production dashboard, this dynamically updates scatter data points
  });
}

// Render Brand Transparency Scorecard
function renderBrandScorecard() {
  const ctxBar = document.getElementById("brandBarChart").getContext("2d");
  const tableBody = document.getElementById("brand-table-body");

  // Sort descending by score
  const sorted = [...brandData].sort((a, b) => b.transparency_score - a.transparency_score);

  // Table population
  tableBody.innerHTML = "";
  sorted.forEach(row => {
    const tr = document.createElement("tr");
    const tierBadge = row.transparency_score >= 75 ? "fair" : (row.transparency_score >= 50 ? "moderate" : "critical");
    const tierText = row.transparency_score >= 75 ? "Transparent" : (row.transparency_score >= 50 ? "Moderate" : "High Risk");

    tr.innerHTML = `
      <td><strong>${row.parent_company}</strong></td>
      <td>${row.sku_count}</td>
      <td style="color:${row.shrink_rate > 0.5 ? '#f87171' : '#4ade80'}">${(row.shrink_rate * 100).toFixed(0)}%</td>
      <td>${row.avg_stealth_index.toFixed(2)}</td>
      <td><strong style="color:${row.transparency_score < 50 ? '#f87171' : '#4ade80'}">${row.transparency_score.toFixed(1)}</strong></td>
      <td><span class="badge-risk ${tierBadge}">${tierText}</span></td>
    `;
    tableBody.appendChild(tr);
  });

  // Bar chart
  brandBarChartInstance = new Chart(ctxBar, {
    type: "bar",
    data: {
      labels: sorted.map(b => b.parent_company),
      datasets: [
        {
          label: "Transparency Score (0-100)",
          data: sorted.map(b => b.transparency_score),
          backgroundColor: sorted.map(b => b.transparency_score >= 75 ? "#10b981" : (b.transparency_score >= 50 ? "#f59e0b" : "#ef4444")),
          borderRadius: 6
        }
      ]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Score: ${ctx.raw} / 100`
          }
        }
      },
      scales: {
        x: {
          min: 0,
          max: 100,
          grid: { color: "rgba(255, 255, 255, 0.06)" },
          ticks: { color: "#94a3b8" }
        },
        y: {
          grid: { display: false },
          ticks: { color: "#cbd5e1", font: { size: 11 } }
        }
      }
    }
  });
}

// Setup SKU Timeline Dropdown and Chart
function setupSkuTimeline() {
  const selector = document.getElementById("sku-selector");
  selector.innerHTML = "";

  Object.keys(BENCHMARK_WAVES).forEach(skuKey => {
    const item = BENCHMARK_WAVES[skuKey];
    const opt = document.createElement("option");
    opt.value = skuKey;
    opt.textContent = `${item.company}: ${item.name}`;
    selector.appendChild(opt);
  });

  selector.addEventListener("change", (e) => updateSkuProfile(e.target.value));
  updateSkuProfile("BIS-PAR-001");
}

function updateSkuProfile(skuKey) {
  const p = BENCHMARK_WAVES[skuKey];
  if (!p) return;

  document.getElementById("sku-prod-name").textContent = p.name;
  document.getElementById("sku-brand-comp").textContent = `${p.brand} • ${p.company} • ${p.category}`;
  document.getElementById("sku-archetype-badge").textContent = p.quadrant;

  const w1 = p.weights[0];
  const w6 = p.weights[5];
  const pctW = (((w6 - w1) / w1) * 100).toFixed(1);
  const p1 = p.prices[0];
  const p6 = p.prices[5];
  const u1 = (p1 / w1) * 100;
  const u6 = (p6 / w6) * 100;
  const pctU = (((u6 - u1) / u1) * 100).toFixed(1);

  document.getElementById("sku-w1").textContent = `${w1}g`;
  document.getElementById("sku-w6").textContent = `${w6}g`;
  document.getElementById("sku-pct-w").textContent = `${pctW}%`;
  document.getElementById("sku-pct-u").textContent = `+${pctU}%`;

  document.getElementById("sku-magic-flag").textContent = p.isMagic;
  document.getElementById("sku-pack-type").textContent = p.packType;
  document.getElementById("sku-claim").textContent = p.claim;
  document.getElementById("sku-stealth-idx").textContent = p.stealthIdx.toFixed(2);

  // Decomposition bar
  document.getElementById("decomp-bar-shrink").style.width = `${p.shrinkShare}%`;
  document.getElementById("decomp-bar-shrink").textContent = `${p.shrinkShare}%`;
  document.getElementById("decomp-bar-price").style.width = `${p.priceShare}%`;
  document.getElementById("decomp-bar-price").textContent = `${p.priceShare}%`;

  // Regulatory alert
  const regAlert = document.getElementById("sku-reg-alert");
  if (p.shrinkShare > 60) {
    regAlert.style.display = "flex";
    document.getElementById("sku-reg-text").innerHTML = `<strong>Silent Shrink Alert:</strong> ${p.shrinkShare}% of the unit price inflation is disguised via grammage reduction while masquerading under '${p.claim}'.`;
  } else {
    regAlert.style.display = "none";
  }

  // Render or update timeline chart
  const ctx = document.getElementById("skuTimelineChart").getContext("2d");
  const waveLabels = ["2022-Q1", "2022-Q3", "2023-Q1", "2023-Q3", "2024-Q1", "2024-Q3"];

  if (skuTimelineChartInstance) {
    skuTimelineChartInstance.destroy();
  }

  skuTimelineChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: waveLabels,
      datasets: [
        {
          label: "Pack Net Weight (g/ml)",
          data: p.weights,
          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.1)",
          yAxisID: "yWeight",
          tension: 0.2,
          fill: true,
          pointRadius: 5
        },
        {
          label: "Selling Price (₹)",
          data: p.prices,
          borderColor: "#3b82f6",
          yAxisID: "yPrice",
          tension: 0.2,
          borderDash: [5, 5],
          pointRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#cbd5e1" } }
      },
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
        yWeight: {
          type: "linear",
          position: "left",
          title: { display: true, text: "Weight (g)", color: "#ef4444" },
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#ef4444" }
        },
        yPrice: {
          type: "linear",
          position: "right",
          title: { display: true, text: "Price (₹)", color: "#3b82f6" },
          grid: { display: false },
          ticks: { color: "#3b82f6" }
        }
      }
    }
  });
}

// Consumer Shrink-O-Meter Calculator Logic
function setupCalculator() {
  const btn = document.getElementById("btn-calculate-shrink");
  btn.addEventListener("click", calculateShrink);

  // Preset chips
  const chips = document.querySelectorAll(".chip-btn");
  chips.forEach(c => {
    c.addEventListener("click", () => {
      document.getElementById("calc-old-weight").value = c.getAttribute("data-oldw");
      document.getElementById("calc-old-price").value = c.getAttribute("data-oldp");
      document.getElementById("calc-new-weight").value = c.getAttribute("data-neww");
      document.getElementById("calc-new-price").value = c.getAttribute("data-newp");
      calculateShrink();
    });
  });

  calculateShrink();
}

function calculateShrink() {
  const wOld = parseFloat(document.getElementById("calc-old-weight").value);
  const pOld = parseFloat(document.getElementById("calc-old-price").value);
  const wNew = parseFloat(document.getElementById("calc-new-weight").value);
  const pNew = parseFloat(document.getElementById("calc-new-price").value);

  if (!wOld || !pOld || !wNew || !pNew || wOld <= 0 || wNew <= 0) return;

  const pctWeightChg = (((wNew - wOld) / wOld) * 100);
  const uOld = (pOld / wOld) * 100;
  const uNew = (pNew / wNew) * 100;
  const pctUnitHike = (((uNew - uOld) / uOld) * 100);

  // What new pack would cost if weight stayed wOld:
  const equivPrice = (pNew / wNew) * wOld;

  document.getElementById("res-weight-cut").textContent = `${pctWeightChg.toFixed(1)}%`;
  document.getElementById("res-unit-hike").textContent = `${pctUnitHike >= 0 ? '+' : ''}${pctUnitHike.toFixed(1)}%`;
  document.getElementById("res-equiv-price").innerHTML = `₹${equivPrice.toFixed(2)} <small class="text-muted">(Nominal ₹${pNew} mask)</small>`;

  const badge = document.getElementById("res-badge");
  const explanation = document.getElementById("res-explanation");

  if (pctWeightChg < -3.0 && pNew === pOld) {
    badge.textContent = "SILENT SHRINKFLATION DETECTED";
    badge.className = "result-badge-large";
    explanation.innerHTML = `Even though you still pay ₹${pOld}, losing ${Math.abs(pctWeightChg).toFixed(1)}% of grammage is functionally equivalent to paying <strong>₹${equivPrice.toFixed(2)}</strong> for the original pack!`;
  } else if (pctWeightChg < -3.0 && pNew > pOld) {
    badge.textContent = "DOUBLE WHAMMY DETECTED (PRICE HIKE + WEIGHT CUT)";
    badge.className = "result-badge-large";
    badge.style.background = "rgba(168, 85, 247, 0.25)";
    badge.style.borderColor = "rgba(168, 85, 247, 0.5)";
    badge.style.color = "#c084fc";
    explanation.innerHTML = `Brand enacted both a direct price increase AND a grammage cut, resulting in a compounding <strong>${pctUnitHike.toFixed(1)}%</strong> surge in effective unit cost.`;
  } else if (pctWeightChg >= -3.0 && pNew > pOld) {
    badge.textContent = "TRANSPARENT OVERT PRICE INFLATION";
    badge.className = "result-badge-large";
    badge.style.background = "rgba(59, 130, 246, 0.2)";
    badge.style.borderColor = "rgba(59, 130, 246, 0.4)";
    badge.style.color = "#60a5fa";
    explanation.innerHTML = `The pack size was preserved intact. Inflation was absorbed purely via an upfront nominal price increase.`;
  } else {
    badge.textContent = "FAIR VALUE / STABLE PACK";
    badge.className = "result-badge-large";
    badge.style.background = "rgba(16, 185, 129, 0.2)";
    badge.style.borderColor = "rgba(16, 185, 129, 0.4)";
    badge.style.color = "#34d399";
    explanation.innerHTML = `No adverse shrinkflation detected on this product SKU.`;
  }
}
