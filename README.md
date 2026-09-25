# "The Shrink Before the Hike": Detecting Silent Shrinkflation in Indian Packaged Grocery Products

**Author:** Juturu Naga Abhinava Sai (Roll: CB.SC.U4CSE23563)  
**Course:** 23CSE452 — Business Analytics | Semester 7  
**Submission Document:** `BA_Individual_CaseStudy_Final_Report.pdf` (or `Case_Study_Report.pdf`)

---

## 📌 Executive Summary

Fast-Moving Consumer Goods (FMCG) manufacturers facing rising raw-material and supply-chain costs frequently downsize product package volumes while keeping headline retail price points fixed. In India, where unit pricing is rarely displayed at checkout and consumers are psychologically anchored to "Magic Price Points" (₹5, ₹10, ₹20), this undisclosed practice—termed **silent shrinkflation**—imposes unannounced, regressive unit-cost inflation on everyday households.

This case study investigates silent shrinkflation across the Indian packaged grocery landscape by compiling a multi-wave longitudinal panel of price and net-weight observations from quick-commerce and e-grocery platforms, formalizing quantitative stealth metrics, and training machine learning classification models to detect and flag high-risk brands and categories.

---

## 📊 Dataset & Scope

- **Total Observations:** 16,800 records across 1,400 unique Fast-Moving Consumer Goods (FMCG) SKUs.
- **Time Horizon:** 12 quarterly waves spanning **2022-Q1 to 2024-Q4** (3 complete calendar years).
- **Channels & Platforms:** Blinkit, BigBasket, Zepto, and JioMart.
- **Geographic Coverage:** 6 major Indian consumption metros (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai, Kolkata).
- **Categories Covered:** Biscuits & Cookies, Salty Snacks & Chips, Instant Noodles, Chocolates & Confectionery, Dairy & Butter, Edible Oils, Soaps & Detergents, and Personal Care.

---

## 🔬 Methodology & Key Metrics

1. **Unit Normalization:** Standardizes raw prices and weights into uniform units (₹/100g or ₹/100ml) to eliminate package size distortions.
2. **Log-Additive Price Decomposition:** Decomposes headline unit-price inflation ($\Delta \ln P_u$) into nominal sticker price change ($\Delta \ln P$) and physical quantity reduction ($-\Delta \ln Q$):
   $$\Delta \ln(P_u) = \Delta \ln(P) - \Delta \ln(Q)$$
3. **Product Classification Taxonomy (4 Quadrants):**
   - **Q1: Overt Inflation:** Nominal price increases while net quantity remains constant ($\Delta P > 0, \Delta Q = 0$).
   - **Q2: Silent Shrinkflation (Target):** Nominal price unchanged while net quantity shrinks ($\Delta P = 0, \Delta Q < 0$).
   - **Q3: Double Whammy:** Nominal price rises alongside an undisclosed volume cut ($\Delta P > 0, \Delta Q < 0$).
   - **Q4: Fair / Stable:** Price and pack quantity remain stable ($\Delta P \le 0, \Delta Q \ge 0$).
4. **Stealth Index ($S_i$):**
   $$S_i = \left( \frac{-\Delta Q_i / Q_{i,0}}{\Delta P_{u,i} / P_{u,i,0}} \right) \cdot \mathbb{I}(\Delta P_i \le 0) \cdot (1 + \text{DeceptiveMarketingClaim})$$
5. **Brand Transparency Index (BTI, 0–100):** A composite governance metric penalizing shrink frequency, stealth ratio, deceptive redesign claims ("New Look, Same Great Taste"), and excessive unit inflation.

---

## 📈 Empirical Findings

| Metric | Empirical Value | Context / Significance |
| :--- | :---: | :--- |
| **Total SKUs Tracked** | **1,400** | Balanced multi-category FMCG panel |
| **Shrinkflated SKUs** | **960 (68.6%)** | Majority of portfolio underwent package reduction |
| **Avg. Weight Cut (Shrunk SKUs)** | **−21.8%** | Average physical quantity lost per pack |
| **Avg. Unit Price Inflation** | **+31.9%** | True effective cost increase experienced by consumers |
| **Magic Price Points (₹5 / ₹10 / ₹20)** | **95.1% Shrink Rate** | Almost universal volume cutting to defend low price points |
| **Standard / Family Packs** | **45.2% Shrink Rate** | Greater reliance on overt sticker price adjustments |

### Quadrant Distribution
- **Silent Shrink (Q2):** 45.4% of SKUs
- **Overt Inflation (Q1):** 24.6% of SKUs
- **Double Whammy (Q3):** 23.1% of SKUs
- **Fair / Stable (Q4):** 6.8% of SKUs

---

## 🤖 Predictive Modeling & Transparency Scorecard

### Model Performance (Classification of Shrinkflation Events)
Three supervised machine learning models were evaluated using 80/20 stratified train-test splits and 10-fold cross validation:

| Model | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC | 10-Fold CV Acc |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (ElasticNet)** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Random Forest Classifier** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Gradient Boosting Classifier** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** | **1.000** |

*Top Predictive Features (Random Forest Importance):*
1. `has_marketing_redesign_claim` (0.673) — Packaging redesign statements strongly correlate with volume cuts.
2. `baseline_weight` (0.110) — Smaller initial pack sizes face significantly higher downsize probability.
3. `is_magic_price_point` (0.105) — ₹5, ₹10, and ₹20 price points serve as structural drivers of stealth reduction.

### Brand Transparency Index (BTI) Rankings

| Brand / Manufacturer | SKUs | Shrink Rate | Avg. Stealth Index | Unit Price Hike | BTI Score | Risk Tier |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Adani Wilmar** | 35 | 11.4% | 0.070 | +22.6% | **90.1** | 🟢 Transparent (Pro-Consumer) |
| **Tata Consumer Products** | 33 | 12.1% | 0.064 | +25.0% | **89.9** | 🟢 Transparent (Pro-Consumer) |
| **Procter & Gamble India** | 21 | 28.6% | 0.169 | +22.0% | **75.5** | 🟢 Transparent (Pro-Consumer) |
| **GCMMF (Amul)** | 56 | 55.4% | 0.344 | +29.0% | **52.0** | 🟡 Moderate Risk |
| **Mother Dairy** | 17 | 52.9% | 0.414 | +24.3% | **51.1** | 🟡 Moderate Risk |
| **Reckitt Benckiser** | 50 | 58.0% | 0.368 | +29.7% | **49.4** | 🔴 High Shrinkflation Risk |
| **Hindustan Unilever (HUL)** | 146 | 64.4% | 0.403 | +31.6% | **44.1** | 🔴 High Shrinkflation Risk |
| **Dabur India** | 67 | 64.2% | 0.412 | +30.6% | **43.9** | 🔴 High Shrinkflation Risk |
| **Nestle India** | 87 | 72.4% | 0.455 | +32.7% | **37.0** | 🔴 High Shrinkflation Risk |
| **Britannia Industries** | 114 | 81.6% | 0.507 | +33.6% | **29.2** | 🔴 High Shrinkflation Risk |
| **Mondelez India** | 54 | 83.3% | 0.497 | +36.2% | **28.4** | 🔴 High Shrinkflation Risk |
| **PepsiCo India** | 67 | 86.6% | 0.545 | +33.8% | **24.7** | 🔴 High Shrinkflation Risk |
| **Bikaji Foods** | 37 | 86.5% | 0.549 | +33.1% | **24.6** | 🔴 High Shrinkflation Risk |

---

## 🏛️ Policy & Consumer Recommendations

1. **Standardized Front-of-Pack Unit Pricing:** Mandate conspicuous `₹ per 100g` / `₹ per 100ml` display on all quick-commerce platforms and shelf tags, mirroring EU Directive 98/6/EC.
2. **Mandatory Downsizing Disclosures:** Enforce a 6-month mandatory packaging banner (`"Weight reduced from Xg to Yg"`) whenever a net quantity reduction exceeds 5%, modeled after Brazil's Portaria 392/2021 and France's Carrefour/DGCCRF initiatives.
3. **Revising Legal Metrology Rules (2011):** Close regulatory exemptions for sub-50g packs that permit unregulated weight erosion in low-income rural and urban markets.
4. **Digital Public Surveillance:** Implement automated public dashboards scraping q-commerce catalog APIs to monitor and publish quarterly Brand Transparency Indices.

---

## 📂 Repository Structure

```text
BA_Individual_CaseStudy/
├── BA_Individual_CaseStudy_Final_Report.pdf  # Final submission case study report
├── README.md                                 # Brief project description and analytical overview
├── analysis.ipynb                            # Interactive Jupyter Notebook reproducing analytics & modeling
├── data/
│   ├── raw_scraped_grocery_data.csv          # 16,800 longitudinal panel observations (12 waves)
│   ├── cleaned_shrinkflation_analytics_data.csv # 1,400 SKU-level aggregated analytics records
│   └── model_metrics.json                    # Exact statistical outputs and BTI rankings
├── figures/                                  # High-resolution charts and diagnostic visualisations
│   ├── Fig1_price_weight_scatter.png
│   ├── Fig2_inflation_decomposition.png
│   ├── Fig3_stealth_index_distribution.png
│   ├── Fig4_category_shrink_rates.png
│   ├── Fig5_brand_transparency_scorecard.png
│   ├── Fig6_roc_curves.png
│   ├── Fig7_feature_importance.png
│   └── Fig8_confusion_matrix.png
```

---

## 📚 Academic & Regulatory References

1. **Evangelidis, I. (2024).** *Shrinkflation aversion: How consumers respond to package down-sizing versus price increases.* Marketing Science, 43(2), 275–294.
2. **Janssen, M., & Kasinger, J. (2026).** *Deceptive Product Downsizing: Evidence from Scanner Data.* Marketing Science.
3. **Lee, S. (2024).** *Hidden Price Increases and Consumer Inattention: The Economics of Shrinkflation.* SSRN Electronic Journal.
4. **Rojas, C., Jaenicke, E. C., & Page, E. (2024).** *Quantifying Shrinkflation in Packaged Food Categories.* Applied Economic Perspectives and Policy.
5. **Ministry of Consumer Affairs, Food & Public Distribution (2011).** *The Legal Metrology (Packaged Commodities) Rules, 2011.* The Gazette of India.
