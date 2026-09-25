"""
Analytics and Machine Learning Engine for Large-Scale Grocery Dataset (16,800 records, 1,400 SKUs)
Title: "The Shrink Before the Hike": Detecting Silent Shrinkflation in Indian Packaged Grocery Products
Author: Business Analytics Individual Case Study
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)
from sklearn.preprocessing import StandardScaler

# Directory verification
os.makedirs("data", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# High-resolution visual configuration
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 300
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10

def run_large_scale_analytics():
    print("[1/5] Ingesting 16,800-row longitudinal grocery dataset...")
    raw_path = os.path.join("data", "raw_scraped_grocery_data.csv")
    df_raw = pd.read_csv(raw_path)
    print(f"Loaded {len(df_raw)} records across {df_raw['sku_id'].nunique()} unique SKUs and {df_raw['wave_id'].nunique()} waves.")

    # -------------------------------------------------------------
    # 2. Longitudinal Price-Weight Decomposition (Wave 1 to Wave 12)
    # -------------------------------------------------------------
    print("[2/5] Running longitudinal econometric log-decomposition across 1,400 SKUs...")
    df_sorted = df_raw.sort_values(by=["sku_id", "wave_id"]).copy()

    # Extract Baseline (Wave 1) and Terminal (Wave 12)
    min_wave = df_sorted["wave_id"].min()
    max_wave = df_sorted["wave_id"].max()

    w_base = df_sorted[df_sorted["wave_id"] == min_wave].set_index("sku_id")
    w_term = df_sorted[df_sorted["wave_id"] == max_wave].set_index("sku_id")

    sku_summaries = []
    for sku in w_base.index:
        row1 = w_base.loc[sku]
        row_last = w_term.loc[sku]

        p1 = float(row1["selling_price_inr"])
        p_last = float(row_last["selling_price_inr"])

        w1 = float(row1["pack_weight_volume"])
        w_last = float(row_last["pack_weight_volume"])

        u1 = float(row1["unit_price_per_100"])
        u_last = float(row_last["unit_price_per_100"])

        # Percentage shifts
        pct_chg_price = ((p_last - p1) / p1) * 100.0
        pct_chg_weight = ((w_last - w1) / w1) * 100.0
        pct_chg_unit_price = ((u_last - u1) / u1) * 100.0

        # Logarithmic Decomposition: dln(U) = dln(P) - dln(W)
        dln_u = np.log(u_last / u1) if (u_last > 0 and u1 > 0) else 0.0
        dln_p = np.log(p_last / p1) if (p_last > 0 and p1 > 0) else 0.0
        dln_w = np.log(w_last / w1) if (w_last > 0 and w1 > 0) else 0.0

        if dln_u > 0.001:
            share_shrinkflation = max(0.0, min(1.0, (-dln_w) / dln_u))
            share_price_hike = max(0.0, min(1.0, dln_p / dln_u))
        else:
            share_shrinkflation = 0.0
            share_price_hike = 0.0

        # Stealth Index (SI)
        if pct_chg_unit_price > 0.5:
            stealth_index = max(0.0, min(1.0, (-pct_chg_weight) / pct_chg_unit_price))
        else:
            stealth_index = 0.0

        # Four-Quadrant Categorization
        if pct_chg_weight < -3.0 and pct_chg_price > 3.0:
            quadrant = "Q3: Double Whammy (Price Up + Weight Down)"
            quadrant_code = "Q3_Double_Whammy"
            is_shrinkflated = 1
        elif pct_chg_weight < -3.0 and pct_chg_price <= 3.0:
            quadrant = "Q2: Silent Shrinkflation (Weight Down, Price Flat)"
            quadrant_code = "Q2_Silent_Shrink"
            is_shrinkflated = 1
        elif pct_chg_weight >= -3.0 and pct_chg_price > 3.0:
            quadrant = "Q1: Overt Inflation (Price Up, Weight Flat)"
            quadrant_code = "Q1_Overt_Inflation"
            is_shrinkflated = 0
        else:
            quadrant = "Q4: Stable / Fair Value"
            quadrant_code = "Q4_Stable_Fair"
            is_shrinkflated = 0

        # Marketing claim check across waves
        claims = df_sorted[df_sorted["sku_id"] == sku]["marketing_redesign_claim"].unique()
        has_redesign = 1 if any(c not in ["Standard Pack", "Classic Pack", "Original Quality"] for c in claims) else 0

        sku_summaries.append({
            "sku_id": sku,
            "product_name": row1["product_name"],
            "brand": row1["brand"],
            "parent_company": row1["parent_company"],
            "category": row1["category"],
            "sub_category": row1["sub_category"],
            "is_magic_price_point": int(row1["is_magic_price_point"]),
            "magic_price_tier": row1["magic_price_tier"],
            "packaging_type": row1["packaging_type"],
            "baseline_price_inr": round(p1, 2),
            "terminal_price_inr": round(p_last, 2),
            "baseline_weight": round(w1, 2),
            "terminal_weight": round(w_last, 2),
            "unit_of_measure": row1["unit_of_measure"],
            "baseline_unit_price": round(u1, 2),
            "terminal_unit_price": round(u_last, 2),
            "pct_change_nominal_price": round(pct_chg_price, 2),
            "pct_change_weight": round(pct_chg_weight, 2),
            "pct_change_unit_price": round(pct_chg_unit_price, 2),
            "dln_unit_price": round(dln_u, 4),
            "dln_nominal_price": round(dln_p, 4),
            "dln_pack_weight": round(dln_w, 4),
            "share_from_shrinkflation": round(share_shrinkflation, 4),
            "share_from_price_hike": round(share_price_hike, 4),
            "stealth_index": round(stealth_index, 4),
            "quadrant": quadrant,
            "quadrant_code": quadrant_code,
            "is_shrinkflated": is_shrinkflated,
            "has_marketing_redesign_claim": has_redesign
        })

    df_cleaned = pd.DataFrame(sku_summaries)
    cleaned_path = os.path.join("data", "cleaned_shrinkflation_analytics_data.csv")
    df_cleaned.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned analytical dataset with {len(df_cleaned)} SKU rows at '{cleaned_path}'.")

    # -------------------------------------------------------------
    # 3. Descriptive Stats & High-Res Figure Generation
    # -------------------------------------------------------------
    print("[3/5] Generating publication-grade visualization plots...")

    # Figure 1: Grammage Distribution
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.hist(df_cleaned["pct_change_weight"], bins=25, color="#d9534f", edgecolor="black", alpha=0.85)
    ax.axvline(0, color="black", linestyle="--", linewidth=1.2, label="Zero Weight Change")
    ax.axvline(-3, color="darkred", linestyle=":", linewidth=1.8, label="Shrinkflation Threshold (-3%)")
    ax.set_title("Distribution of Net Pack Weight Changes (%) Across 1,400 FMCG SKUs", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Percentage Change in Net Pack Weight (%)")
    ax.set_ylabel("Number of SKUs")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True, facecolor="white", framealpha=0.9, fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "eda_grammage_distribution.png"))
    plt.close()

    # Figure 2: Price vs Weight Scatter Matrix
    fig, ax = plt.subplots(figsize=(8.5, 5))
    quad_colors = {
        "Q2_Silent_Shrink": ("#d9534f", "Q2: Silent Shrink (Weight Down, Price Flat)"),
        "Q3_Double_Whammy": ("#8e44ad", "Q3: Double Whammy (Price Up + Weight Down)"),
        "Q1_Overt_Inflation": ("#2980b9", "Q1: Overt Inflation (Price Up, Weight Flat)"),
        "Q4_Stable_Fair": ("#27ae60", "Q4: Stable / Fair Value")
    }
    for q_code, (color, label) in quad_colors.items():
        subset = df_cleaned[df_cleaned["quadrant_code"] == q_code]
        ax.scatter(subset["pct_change_nominal_price"], subset["pct_change_weight"], color=color, label=label, s=35, edgecolors="none", alpha=0.75)

    ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7)
    ax.set_title("Price-Weight Quadrant Analysis: Nominal Price vs. Grammage Shifts (N = 1,400)", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Nominal Price Change (%)")
    ax.set_ylabel("Pack Net Weight Change (%)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower left", frameon=True, fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "price_vs_weight_scatter.png"))
    plt.close()

    # Figure 3: Category Shrinkflation Rate
    cat_rates = df_cleaned.groupby("category")["is_shrinkflated"].agg(["count", "mean"]).reset_index()
    cat_rates["shrinkflation_pct"] = cat_rates["mean"] * 100.0
    cat_rates = cat_rates.sort_values(by="shrinkflation_pct", ascending=True)

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars = ax.barh(cat_rates["category"], cat_rates["shrinkflation_pct"], color="#e67e22", edgecolor="black", alpha=0.85)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", ha="left", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 105)
    ax.set_title("Shrinkflation Incidence Rate Across FMCG Categories (%)", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Percentage of Monitored SKUs Undergoing Grammage Cuts (%)")
    ax.grid(True, linestyle=":", alpha=0.6, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "category_shrinkflation_rate.png"))
    plt.close()

    # Figure 4: Magic Price Point Vulnerability
    magic_comp = df_cleaned.groupby("is_magic_price_point")["is_shrinkflated"].mean() * 100.0
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    bar_vals = [magic_comp.loc[0], magic_comp.loc[1]]
    bars = ax.bar(["Standard Non-LUP Packs", "Magic Price Points (₹5/10/20)"], bar_vals, color=["#3498db", "#e74c3c"], edgecolor="black", width=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.set_title("Shrinkflation Incidence: Magic Price Points vs. Standard", fontsize=10.5, fontweight="bold", pad=10)
    ax.set_ylabel("Shrinkflation Incidence Rate (%)")
    ax.grid(True, linestyle=":", alpha=0.6, axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "magic_price_point_vulnerability.png"))
    plt.close()

    # Figure 5: Annotated 4-Quadrant Matrix Pie
    quad_counts = df_cleaned["quadrant_code"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors_pie = ["#d9534f", "#2980b9", "#8e44ad", "#27ae60"]
    labels_pie = [
        f"Q2: Pure Silent Shrink ({quad_counts.get('Q2_Silent_Shrink', 0)})",
        f"Q1: Overt Inflation ({quad_counts.get('Q1_Overt_Inflation', 0)})",
        f"Q3: Double Whammy ({quad_counts.get('Q3_Double_Whammy', 0)})",
        f"Q4: Stable / Fair ({quad_counts.get('Q4_Stable_Fair', 0)})"
    ]
    ax.pie(quad_counts.values, labels=labels_pie, autopct="%1.1f%%", startangle=140, colors=colors_pie, textprops={'fontsize': 9, 'fontweight': 'bold'})
    ax.set_title("Distribution of 1,400 Grocery SKUs Across Pricing Archetypes", fontsize=11, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "quad_quadrant_matrix.png"))
    plt.close()

    # -------------------------------------------------------------
    # 4. Brand Transparency Index (BTI) Computation
    # -------------------------------------------------------------
    print("[4/5] Computing Brand Transparency Index across conglomerates...")
    brand_stats = df_cleaned.groupby("parent_company").agg(
        sku_count=("sku_id", "count"),
        shrink_count=("is_shrinkflated", "sum"),
        shrink_rate=("is_shrinkflated", "mean"),
        avg_stealth_index=("stealth_index", "mean"),
        avg_unit_price_hike=("pct_change_unit_price", "mean"),
        deceptive_claim_rate=("has_marketing_redesign_claim", "mean")
    ).reset_index()

    # Filter for companies with at least 15 SKUs for statistical strength
    brand_stats = brand_stats[brand_stats["sku_count"] >= 15].copy()

    brand_stats["transparency_score"] = 100.0 - (
        (brand_stats["shrink_rate"] * 45.0) +
        (brand_stats["avg_stealth_index"] * 35.0) +
        (brand_stats["deceptive_claim_rate"] * 20.0)
    )
    brand_stats["transparency_score"] = brand_stats["transparency_score"].clip(0.0, 100.0).round(1)
    brand_stats = brand_stats.sort_values(by="transparency_score", ascending=True)

    def assign_risk_tier(s):
        if s >= 75:
            return "Transparent (Pro-Consumer)"
        elif s >= 50:
            return "Moderate Risk (Mixed Disclosure)"
        else:
            return "High Shrinkflation Risk (Stealth Dominant)"

    brand_stats["risk_tier"] = brand_stats["transparency_score"].apply(assign_risk_tier)

    # Plot BTI
    fig, ax = plt.subplots(figsize=(9, 5))
    bar_colors = ["#c0392b" if s < 50 else ("#f39c12" if s < 75 else "#27ae60") for s in brand_stats["transparency_score"]]
    bars = ax.barh(brand_stats["parent_company"], brand_stats["transparency_score"], color=bar_colors, edgecolor="black", alpha=0.85)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f} / 100", va="center", ha="left", fontsize=9, fontweight="bold")
    ax.axvline(50, color="orange", linestyle="--", linewidth=1.2, label="Moderate Risk (50)")
    ax.axvline(75, color="green", linestyle="--", linewidth=1.2, label="High Transparency (75)")
    ax.set_xlim(0, 105)
    ax.set_title("Brand Transparency Index (BTI) Across Major Indian FMCG Conglomerates", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Transparency Score (0 = Opaque, 100 = Transparent)")
    ax.grid(True, linestyle=":", alpha=0.6, axis="x")
    ax.legend(loc="lower right", frameon=True, fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "brand_transparency_ranking.png"))
    plt.close()

    # -------------------------------------------------------------
    # 5. Machine Learning Modeling on 1,400 SKUs
    # -------------------------------------------------------------
    print("[5/5] Training predictive ML models (Random Forest, Logistic Regression, Gradient Boosting)...")
    df_ml = df_cleaned.copy()
    features_cat = ["category", "packaging_type"]
    df_ml_encoded = pd.get_dummies(df_ml, columns=features_cat, drop_first=True)

    feature_cols = [
        "is_magic_price_point",
        "baseline_price_inr",
        "baseline_weight",
        "has_marketing_redesign_claim"
    ] + [c for c in df_ml_encoded.columns if c.startswith("category_") or c.startswith("packaging_type_")]

    X = df_ml_encoded[feature_cols].copy()
    y = df_ml_encoded["is_shrinkflated"].copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Logistic Regression
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]

    # 2. Random Forest
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]

    # 3. Gradient Boosting
    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=3, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    y_prob_gb = gb.predict_proba(X_test)[:, 1]

    # Cross validation scores
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_lr = cross_val_score(lr, X_train_scaled, y_train, cv=cv, scoring="accuracy").mean()
    cv_rf = cross_val_score(rf, X_train, y_train, cv=cv, scoring="accuracy").mean()
    cv_gb = cross_val_score(gb, X_train, y_train, cv=cv, scoring="accuracy").mean()

    auc_lr = roc_auc_score(y_test, y_prob_lr)
    auc_rf = roc_auc_score(y_test, y_prob_rf)
    auc_gb = roc_auc_score(y_test, y_prob_gb)

    # Summary metrics payload
    metrics = {
        "dataset_summary": {
            "total_skus": int(len(df_cleaned)),
            "total_observations": int(len(df_raw)),
            "time_span": "2022-Q1 to 2024-Q4 (12 Waves)",
            "shrinkflated_sku_count": int(df_cleaned["is_shrinkflated"].sum()),
            "shrinkflated_percentage": round(float(df_cleaned["is_shrinkflated"].mean() * 100), 1),
            "average_unit_price_inflation": round(float(df_cleaned["pct_change_unit_price"].mean()), 1),
            "average_weight_reduction_in_shrunk_skus": round(float(df_cleaned[df_cleaned["is_shrinkflated"] == 1]["pct_change_weight"].mean()), 1),
            "magic_price_point_shrink_rate": round(float(magic_comp.loc[1]), 1),
            "standard_pack_shrink_rate": round(float(magic_comp.loc[0]), 1)
        },
        "model_performance": {
            "logistic_regression": {
                "accuracy": round(float(accuracy_score(y_test, y_pred_lr)), 3),
                "precision": round(float(precision_score(y_test, y_pred_lr)), 3),
                "recall": round(float(recall_score(y_test, y_pred_lr)), 3),
                "f1_score": round(float(f1_score(y_test, y_pred_lr)), 3),
                "roc_auc": round(float(auc_lr), 3),
                "cv_accuracy_10fold": round(float(cv_lr), 3),
                "confusion_matrix": confusion_matrix(y_test, y_pred_lr).tolist()
            },
            "random_forest": {
                "accuracy": round(float(accuracy_score(y_test, y_pred_rf)), 3),
                "precision": round(float(precision_score(y_test, y_pred_rf)), 3),
                "recall": round(float(recall_score(y_test, y_pred_rf)), 3),
                "f1_score": round(float(f1_score(y_test, y_pred_rf)), 3),
                "roc_auc": round(float(auc_rf), 3),
                "cv_accuracy_10fold": round(float(cv_rf), 3),
                "confusion_matrix": confusion_matrix(y_test, y_pred_rf).tolist()
            },
            "gradient_boosting": {
                "accuracy": round(float(accuracy_score(y_test, y_pred_gb)), 3),
                "precision": round(float(precision_score(y_test, y_pred_gb)), 3),
                "recall": round(float(recall_score(y_test, y_pred_gb)), 3),
                "f1_score": round(float(f1_score(y_test, y_pred_gb)), 3),
                "roc_auc": round(float(auc_gb), 3),
                "cv_accuracy_10fold": round(float(cv_gb), 3),
                "confusion_matrix": confusion_matrix(y_test, y_pred_gb).tolist()
            }
        },
        "brand_transparency_table": brand_stats.to_dict(orient="records")
    }

    with open(os.path.join("data", "model_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    # Plot ROC Curves
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_prob_lr)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)
    fpr_gb, tpr_gb, _ = roc_curve(y_test, y_prob_gb)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(fpr_rf, tpr_rf, color="#2ecc71", linewidth=2.2, label=f"Random Forest (AUC = {auc_rf:.3f})")
    ax.plot(fpr_gb, tpr_gb, color="#e67e22", linewidth=1.8, linestyle="-.", label=f"Gradient Boosting (AUC = {auc_gb:.3f})")
    ax.plot(fpr_lr, tpr_lr, color="#3498db", linewidth=1.8, linestyle="--", label=f"Logistic Regression (AUC = {auc_lr:.3f})")
    ax.plot([0, 1], [0, 1], color="navy", linestyle=":", label="Random Guess (AUC = 0.500)")
    ax.set_title("ROC Curves for Silent Shrinkflation Classifiers (Holdout N = 350)", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("False Positive Rate (1 - Specificity)")
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", frameon=True, fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "ml_roc_curve.png"))
    plt.close()

    # Plot Feature Importance from Random Forest
    importances = rf.feature_importances_
    feat_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances}).sort_values(by="Importance", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars = ax.barh(feat_df["Feature"][::-1], feat_df["Importance"][::-1], color="#34495e", edgecolor="black", alpha=0.85)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.005, bar.get_y() + bar.get_height()/2, f"{w:.3f}", va="center", ha="left", fontsize=9, fontweight="bold")
    ax.set_title("Top 10 Feature Importances in Predicting Shrinkflation (Random Forest Gini)", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Mean Decrease in Impurity (Gini Importance)")
    ax.grid(True, linestyle=":", alpha=0.6, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "ml_feature_importance.png"))
    plt.close()

    print("Large-scale analytics and ML engine execution complete!")
    print(f"Dataset summary: {metrics['dataset_summary']}")
    print(f"Random Forest test accuracy: {metrics['model_performance']['random_forest']['accuracy']}, AUC: {auc_rf:.3f}")

if __name__ == "__main__":
    run_large_scale_analytics()
