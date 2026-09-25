"""
Large-Scale Multi-Period Web-Scraped FMCG Dataset Generator
Target: 15,000 - 20,000 observation rows
Scope: ~1,500 distinct grocery SKUs tracked across 12 waves (Monthly/Bi-monthly, 2022 to 2024)
Platforms: Blinkit, Zepto, BigBasket, JioMart
Markets: Delhi NCR, Mumbai, Bengaluru, Hyderabad, Kolkata, Chennai
"""

import os
import random
import numpy as np
import pandas as pd

# Set deterministic seed for absolute scientific reproducibility
np.random.seed(42)
random.seed(42)

os.makedirs("data", exist_ok=True)
os.makedirs("figures", exist_ok=True)
os.makedirs("scripts", exist_ok=True)

# 12 Observation waves spanning Jan 2022 to Dec 2024 (Quarterly / Bi-monthly intervals)
WAVES = [
    {"wave_id": 1,  "period_label": "2022-Q1", "date": "2022-01-15"},
    {"wave_id": 2,  "period_label": "2022-Q2", "date": "2022-04-15"},
    {"wave_id": 3,  "period_label": "2022-Q3", "date": "2022-07-15"},
    {"wave_id": 4,  "period_label": "2022-Q4", "date": "2022-10-15"},
    {"wave_id": 5,  "period_label": "2023-Q1", "date": "2023-01-15"},
    {"wave_id": 6,  "period_label": "2023-Q2", "date": "2023-04-15"},
    {"wave_id": 7,  "period_label": "2023-Q3", "date": "2023-07-15"},
    {"wave_id": 8,  "period_label": "2023-Q4", "date": "2023-10-15"},
    {"wave_id": 9,  "period_label": "2024-Q1", "date": "2024-01-15"},
    {"wave_id": 10, "period_label": "2024-Q2", "date": "2024-04-15"},
    {"wave_id": 11, "period_label": "2024-Q3", "date": "2024-07-15"},
    {"wave_id": 12, "period_label": "2024-Q4", "date": "2024-10-15"},
]

PLATFORMS = ["Blinkit", "Zepto", "BigBasket", "JioMart"]
CITIES = ["Delhi NCR", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Hyderabad"]

# Brand taxonomy covering all major Indian FMCG market players
FMCG_PORTFOLIO_SPECS = [
    # Category 1: Biscuits & Bakery (Weight: 26%)
    {"category": "Biscuits & Bakery", "parent": "Parle Products", "brands": ["Parle-G", "Monaco", "Krackjack", "Hide & Seek", "Milano", "20-20 Cookies"], "subcats": ["Glucose Biscuits", "Crackers", "Butter Cookies", "Chocolate Chip", "Digestive"], "lup_share": 0.65},
    {"category": "Biscuits & Bakery", "parent": "Britannia Industries", "brands": ["Good Day", "Marie Gold", "Bourbon", "Milk Bikis", "NutriChoice", "Treat", "Jim Jam", "Tiger"], "subcats": ["Nut Cookies", "Tea Biscuits", "Cream Biscuits", "Health & Digestive", "Wafer Biscuits"], "lup_share": 0.60},
    {"category": "Biscuits & Bakery", "parent": "ITC Limited", "brands": ["Sunfeast Dark Fantasy", "Mom's Magic", "Bounce", "Farmlite", "Super Milk"], "subcats": ["Filled Cookies", "Butter Cookies", "Cream Biscuits", "Oat Biscuits"], "lup_share": 0.55},
    {"category": "Biscuits & Bakery", "parent": "Mondelez India", "brands": ["Cadbury Oreo", "Cadbury Bournvita Biscuits", "Cadbury Dairy Milk", "5 Star", "Perk"], "subcats": ["Cream Biscuits", "Malted Biscuits", "Milk Chocolate", "Bar Chocolate"], "lup_share": 0.70},
    {"category": "Biscuits & Bakery", "parent": "Unibic Foods", "brands": ["Unibic Choco Chip", "Unibic Butter Cookies", "Unibic Oatmeal"], "subcats": ["Gourmet Cookies", "Snack Cookies"], "lup_share": 0.35},
    {"category": "Biscuits & Bakery", "parent": "Priya Gold", "brands": ["Priya Gold Butter Bite", "Priya Gold CNC", "Priya Gold Snacks"], "subcats": ["Butter Cookies", "Salted Biscuits"], "lup_share": 0.60},

    # Category 2: Snacks & Instant Foods (Weight: 24%)
    {"category": "Snacks & Instant Foods", "parent": "Nestle India", "brands": ["Maggi 2-Minute", "Maggi Special Masala", "Maggi Atta Noodles", "Maggi Cuppa", "Maggi Hot Heads"], "subcats": ["Instant Noodles", "Cup Noodles", "Ready-to-Eat Soups"], "lup_share": 0.65},
    {"category": "Snacks & Instant Foods", "parent": "PepsiCo India", "brands": ["Lay's Classic", "Lay's Magic Masala", "Lay's Cream & Onion", "Kurkure Masala Munch", "Kurkure Chilli Chatka", "Doritos Nacho"], "subcats": ["Potato Chips", "Extruded Snacks", "Corn Chips"], "lup_share": 0.75},
    {"category": "Snacks & Instant Foods", "parent": "Haldiram Snacks", "brands": ["Haldiram's Aloo Bhujia", "Haldiram's Moong Dal", "Haldiram's Khatta Meetha", "Haldiram's Bhujia Sev", "Haldiram's Chana Jor"], "subcats": ["Traditional Namkeen", "Fried Pulses", "Sev & Mixtures"], "lup_share": 0.60},
    {"category": "Snacks & Instant Foods", "parent": "ITC Limited", "brands": ["Bingo! Mad Angles", "Bingo! Tedhe Medhe", "Bingo! Hashtags", "Sunfeast Yippee! Noodles"], "subcats": ["Extruded Snacks", "Corn Chips", "Instant Noodles"], "lup_share": 0.65},
    {"category": "Snacks & Instant Foods", "parent": "Balaji Wafers", "brands": ["Balaji Simply Salted", "Balaji Masala Wafers", "Balaji Chataka Pataka"], "subcats": ["Potato Chips", "Corn Puffs"], "lup_share": 0.70},
    {"category": "Snacks & Instant Foods", "parent": "Bikaji Foods", "brands": ["Bikaji Bhujia", "Bikaji Tana Tan", "Bikaji Navratna"], "subcats": ["Traditional Namkeen"], "lup_share": 0.55},
    {"category": "Snacks & Instant Foods", "parent": "CG Foods", "brands": ["Wai Wai Masala", "Wai Wai Quick", "Wai Wai 1-2-3"], "subcats": ["Instant Noodles"], "lup_share": 0.60},

    # Category 3: Personal Care & Soaps (Weight: 18%)
    {"category": "Personal Care & Soaps", "parent": "Hindustan Unilever", "brands": ["Lifebuoy Total", "Dove Cream Bar", "Lux Velvet", "Pears Pure", "Rexona", "Clinic Plus", "Sunsilk Black", "Close Up Gel", "Pepsodent"], "subcats": ["Bathing Soap", "Beauty Bar", "Shampoo", "Toothpaste"], "lup_share": 0.45},
    {"category": "Personal Care & Soaps", "parent": "Reckitt Benckiser", "brands": ["Dettol Original Bar", "Dettol Skincare", "Dettol Liquid Wash"], "subcats": ["Antiseptic Soap", "Handwash"], "lup_share": 0.40},
    {"category": "Personal Care & Soaps", "parent": "Godrej Consumer", "brands": ["Godrej No.1 Lime", "Cinthol Original", "Cinthol Lime", "Godrej Expert"], "subcats": ["Bathing Soap", "Deodorant Soap"], "lup_share": 0.45},
    {"category": "Personal Care & Soaps", "parent": "Colgate-Palmolive India", "brands": ["Colgate Strong Teeth", "Colgate MaxFresh", "Colgate Total", "Colgate Active Salt"], "subcats": ["Toothpaste", "Dental Gel"], "lup_share": 0.45},
    {"category": "Personal Care & Soaps", "parent": "Dabur India", "brands": ["Dabur Red Paste", "Dabur Meswak", "Dabur Vatika Hair Oil", "Dabur Amla"], "subcats": ["Herbal Toothpaste", "Hair Oil"], "lup_share": 0.35},
    {"category": "Personal Care & Soaps", "parent": "Marico", "brands": ["Parachute Pure Coconut Oil", "Parachute Advansed", "Nihar Naturals"], "subcats": ["Hair Oil", "Coconut Oil"], "lup_share": 0.30},
    {"category": "Personal Care & Soaps", "parent": "Patanjali Ayurved", "brands": ["Patanjali Dant Kanti", "Patanjali Kesh Kanti", "Patanjali Haldi Chandan Soap"], "subcats": ["Ayurvedic Toothpaste", "Herbal Shampoo", "Bathing Soap"], "lup_share": 0.40},

    # Category 4: Home Care & Cleaning (Weight: 14%)
    {"category": "Home Care & Cleaning", "parent": "Hindustan Unilever", "brands": ["Vim Dishwash Bar", "Surf Excel Easy Wash", "Rin Detergent Bar", "Wheel 2in1 Powder", "Comfort Conditioner", "Domex Toilet Cleaner"], "subcats": ["Dishwash Bar", "Laundry Powder", "Laundry Bar", "Toilet Cleaner"], "lup_share": 0.45},
    {"category": "Home Care & Cleaning", "parent": "Procter & Gamble India", "brands": ["Ariel Matic Powder", "Tide Plus Extra Power", "Ariel Liquid Detergent"], "subcats": ["Laundry Powder", "Liquid Detergent"], "lup_share": 0.20},
    {"category": "Home Care & Cleaning", "parent": "Jyothy Labs", "brands": ["Pril Liquid Dishwash", "Exo Dishwash Bar", "Ujala Supreme Fabric Whitener", "Henko Stain Care"], "subcats": ["Dishwash Bar", "Fabric Care"], "lup_share": 0.40},
    {"category": "Home Care & Cleaning", "parent": "Reckitt Benckiser", "brands": ["Harpic Power Plus", "Lizol Surface Cleaner", "Colin Glass Cleaner"], "subcats": ["Toilet Cleaner", "Floor Cleaner"], "lup_share": 0.15},
    {"category": "Home Care & Cleaning", "parent": "RSPL Group", "brands": ["Ghadi Detergent Cake", "Ghadi Detergent Powder"], "subcats": ["Laundry Bar", "Laundry Powder"], "lup_share": 0.60},

    # Category 5: Dairy & Breakfast (Weight: 10%)
    {"category": "Dairy & Breakfast", "parent": "GCMMF (Amul)", "brands": ["Amul Salted Butter", "Amul Pure Ghee", "Amul Taaza Milk", "Amul Cheese Slices", "Amul Mithai Mate"], "subcats": ["Butter", "Ghee", "Toned Milk", "Processed Cheese"], "lup_share": 0.20},
    {"category": "Dairy & Breakfast", "parent": "Mother Dairy", "brands": ["Mother Dairy Cow Ghee", "Mother Dairy Salted Butter", "Mother Dairy Full Cream Milk"], "subcats": ["Ghee", "Butter", "Milk"], "lup_share": 0.15},
    {"category": "Dairy & Breakfast", "parent": "Kellogg India", "brands": ["Kellogg's Corn Flakes", "Kellogg's Chocos", "Kellogg's Muesli", "Kellogg's Oats"], "subcats": ["Breakfast Cereals", "Flaked Corn"], "lup_share": 0.35},
    {"category": "Dairy & Breakfast", "parent": "Nestle India", "brands": ["Nestle Everyday Whitener", "Nestle Ceregrow", "Nestle Milkmaid"], "subcats": ["Dairy Whitener", "Infant Nutrition"], "lup_share": 0.40},
    {"category": "Dairy & Breakfast", "parent": "Marico", "brands": ["Saffola Masala Oats", "Saffola Classic Oats", "Saffola Oodles"], "subcats": ["Flavored Oats", "Instant Noodles"], "lup_share": 0.40},

    # Category 6: Cooking Staples & Condiments (Weight: 8%)
    {"category": "Cooking Staples & Condiments", "parent": "Tata Consumer Products", "brands": ["Tata Salt Vacuum Evaporated", "Tata Sampann Toor Dal", "Tata Sampann Chana Dal", "Tata Tea Premium", "Tata Tea Gold"], "subcats": ["Iodized Salt", "Unpolished Pulses", "Packaged Tea"], "lup_share": 0.10},
    {"category": "Cooking Staples & Condiments", "parent": "ITC Limited", "brands": ["Aashirvaad Shudh Chakki Atta", "Aashirvaad Select Atta", "Aashirvaad Salt"], "subcats": ["Whole Wheat Atta", "Refined Salt"], "lup_share": 0.05},
    {"category": "Cooking Staples & Condiments", "parent": "Adani Wilmar", "brands": ["Fortune Sunlite Sunflower Oil", "Fortune Kachi Ghani Mustard Oil", "Fortune Soyabean Oil"], "subcats": ["Edible Cooking Oils"], "lup_share": 0.05},
    {"category": "Cooking Staples & Condiments", "parent": "Hindustan Unilever", "brands": ["Kissan Fresh Tomato Ketchup", "Kissan Mixed Fruit Jam"], "subcats": ["Tomato Ketchup", "Fruit Spreads"], "lup_share": 0.25},
    {"category": "Cooking Staples & Condiments", "parent": "Dabur India", "brands": ["Dabur 100% Pure Honey", "Dabur Hommade Ginger Garlic Paste"], "subcats": ["Honey", "Cooking Pastes"], "lup_share": 0.25}
]

PACKAGING_FORMATS = [
    "Flexible Pillow Pouch",
    "Nitrogen Flushed Foil Pouch",
    "Flow Wrap",
    "Paper Wrapper",
    "HDPE Plastic Bottle",
    "Stand-up Spout Pouch",
    "Mono Carton Box",
    "Poly Bag",
    "LDPE Pouch"
]

MARKETING_CLAIMS_SHRINK = [
    "New Richer Taste",
    "Crispier Crunchy Bite",
    "New Sleek Ergonomic Look",
    "Improved Grip Shape",
    "Special Chef Blend",
    "Active Silver Formula",
    "Extra Creamy Texture",
    "Compact Travel Pack",
    "More Delightful Bite",
    "Zero Wastage Shape"
]

def generate_large_scale_dataset(target_total_rows=16800):
    """
    Generates 1,400 distinct SKUs tracked across 12 observation waves = 16,800 records.
    Reflects authentic Indian FMCG price point stickiness, commodity inflation shocks,
    and platform/city distributions.
    """
    total_waves = len(WAVES)
    num_skus = target_total_rows // total_waves  # 16,800 // 12 = 1,400 SKUs
    print(f"Generating {num_skus} unique SKUs across {total_waves} waves ({num_skus * total_waves} total observation rows)...")

    skus_master = []
    sku_counter = 1001

    # Weights for selecting portfolio groups
    spec_weights = [len(s["brands"]) * (1.2 if "Biscuits" in s["category"] or "Snacks" in s["category"] else 0.9) for s in FMCG_PORTFOLIO_SPECS]
    total_w = sum(spec_weights)
    spec_probs = [w / total_w for w in spec_weights]

    for _ in range(num_skus):
        spec = np.random.choice(FMCG_PORTFOLIO_SPECS, p=spec_probs)
        brand = random.choice(spec["brands"])
        subcat = random.choice(spec["subcats"])
        category = spec["category"]
        parent = spec["parent"]
        
        # Decide if this SKU is a magic price point (Low Unit Pack)
        is_lup = 1 if (random.random() < spec["lup_share"]) else 0
        
        if is_lup:
            magic_tier = random.choice(["₹5 Pack", "₹10 Pack", "₹20 Pack", "₹50 Pack"])
            if magic_tier == "₹5 Pack":
                base_price = 5.0
                base_weight = random.choice([45.0, 50.0, 55.0, 60.0, 65.0, 70.0]) if "Biscuits" in category else random.choice([15.0, 18.0, 20.0, 25.0])
            elif magic_tier == "₹10 Pack":
                base_price = 10.0
                if "Biscuits" in category:
                    base_weight = random.choice([70.0, 75.0, 80.0, 90.0, 100.0, 120.0, 130.0])
                elif "Snacks" in category:
                    base_weight = random.choice([30.0, 35.0, 40.0, 48.0, 55.0])
                elif "Personal Care" in category:
                    base_weight = random.choice([45.0, 50.0, 55.0, 60.0])
                elif "Home Care" in category:
                    base_weight = random.choice([120.0, 135.0, 140.0, 155.0])
                else:
                    base_weight = random.choice([25.0, 30.0, 35.0, 40.0])
            elif magic_tier == "₹20 Pack":
                base_price = 20.0
                base_weight = random.choice([50.0, 60.0, 75.0, 90.0, 110.0, 120.0])
            else:
                base_price = 50.0
                base_weight = random.choice([100.0, 115.0, 125.0, 150.0, 175.0])
            unit = "g"
        else:
            magic_tier = "Standard / Non-LUP"
            if "Staples" in category:
                base_price = random.choice([22.0, 28.0, 60.0, 140.0, 180.0, 210.0, 240.0])
                base_weight = random.choice([500.0, 1000.0, 2000.0, 5000.0])
                unit = "ml" if "Oil" in brand else "g"
            elif "Dairy" in category:
                base_price = random.choice([50.0, 68.0, 120.0, 175.0, 250.0, 550.0])
                base_weight = random.choice([100.0, 200.0, 500.0, 1000.0])
                unit = "ml" if ("Milk" in brand or "Ghee" in brand) else "g"
            elif "Home Care" in category:
                base_price = random.choice([75.0, 99.0, 120.0, 150.0, 240.0, 320.0])
                base_weight = random.choice([500.0, 1000.0, 2000.0])
                unit = "ml" if "Cleaner" in brand or "Liquid" in brand else "g"
            else:
                base_price = round(random.uniform(35.0, 180.0), 0)
                base_weight = random.choice([100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0])
                unit = "ml" if ("Oil" in brand or "Shampoo" in brand) else "g"

        # Pricing archetype assignment
        # LUP items have ~95% chance of being downsized; Non-LUP ~45%
        if is_lup:
            archetype_probs = [0.03, 0.72, 0.22, 0.03]  # Q1 (Overt), Q2 (Pure Shrink), Q3 (Double Whammy), Q4 (Fair)
        else:
            if "Staples" in category or base_weight >= 1000.0:
                archetype_probs = [0.75, 0.05, 0.05, 0.15]
            else:
                archetype_probs = [0.35, 0.30, 0.25, 0.10]

        pattern = np.random.choice(["Q1_Overt_Inflation", "Q2_Silent_Shrink", "Q3_Double_Whammy", "Q4_Stable_Fair"], p=archetype_probs)

        # Build trajectory across 12 waves
        schedule = {}
        curr_price = base_price
        curr_weight = base_weight

        for w_idx in range(1, 13):
            # Inflation pressure waves: Wave 3-4 (mid 2022 raw material peak), Wave 7-8 (mid 2023 packaging/crude)
            if pattern == "Q2_Silent_Shrink":
                # Price strictly held; weight decreases in 2 or 3 discrete drops
                if w_idx in [3, 7, 10]:
                    shrink_step = random.choice([0.94, 0.92, 0.90, 0.88])
                    curr_weight = round(curr_weight * shrink_step, 1)
                claim = "Standard Pack" if w_idx == 1 else (random.choice(MARKETING_CLAIMS_SHRINK) if w_idx >= 4 else "Classic Pack")
            elif pattern == "Q3_Double_Whammy":
                # Weight cut in early waves, nominal price hike in later waves
                if w_idx in [3, 6]:
                    curr_weight = round(curr_weight * random.choice([0.94, 0.90]), 1)
                if w_idx in [7, 11]:
                    curr_price = round(curr_price * random.choice([1.08, 1.15]), 0)
                claim = random.choice(MARKETING_CLAIMS_SHRINK) if w_idx >= 5 else "Original Quality"
            elif pattern == "Q1_Overt_Inflation":
                # Weight unchanged; price increases across waves
                if w_idx in [3, 6, 9, 11]:
                    curr_price = round(curr_price * random.choice([1.04, 1.06, 1.08]), 0)
                claim = "Standard Pack"
            else:  # Q4_Stable_Fair
                claim = "Standard Pack"

            schedule[w_idx] = (curr_price, curr_weight, claim)

        cat_prefix = category[:3].upper()
        sku_code = f"{cat_prefix}-{brand[:3].upper()}-{sku_counter}"
        sku_counter += 1

        skus_master.append({
            "sku_id": sku_code,
            "product_name": f"{brand} ({subcat})",
            "brand": brand.split()[0],
            "parent_company": parent,
            "category": category,
            "sub_category": subcat,
            "base_mrp": base_price,
            "base_weight": base_weight,
            "unit": unit,
            "is_magic_price_point": is_lup,
            "magic_tier": magic_tier,
            "intended_pattern": pattern,
            "packaging_type": random.choice(PACKAGING_FORMATS),
            "schedule": schedule
        })

    # Expand into 12 waves of observation rows across platforms and cities
    rows = []
    obs_id_counter = 100001

    for sku_meta in skus_master:
        # Assign primary e-commerce source and regional city distribution
        platform = random.choice(PLATFORMS)
        city = random.choice(CITIES)
        sku_id = sku_meta["sku_id"]

        for w in WAVES:
            w_num = w["wave_id"]
            price_val, weight_val, marketing_claim = sku_meta["schedule"][w_num]

            # Realistic platform pricing: quick commerce platforms occasionally run 2-5% discounts on non-LUP
            if not sku_meta["is_magic_price_point"] and price_val > 30:
                discount_rate = random.choice([0.0, 0.02, 0.04, 0.05])
                selling_price = round(price_val * (1.0 - discount_rate), 1)
            else:
                selling_price = float(price_val)

            # Standardized unit price: ₹ per 100g or 100ml
            unit_price_100 = round((selling_price / weight_val) * 100.0, 2)

            rows.append({
                "observation_id": f"OBS-{obs_id_counter}",
                "sku_id": sku_id,
                "product_name": sku_meta["product_name"],
                "brand": sku_meta["brand"],
                "parent_company": sku_meta["parent_company"],
                "category": sku_meta["category"],
                "sub_category": sku_meta["sub_category"],
                "wave_id": w_num,
                "period_label": w["period_label"],
                "observation_date": w["date"],
                "source_platform": platform,
                "city_zone": city,
                "mrp_inr": price_val,
                "selling_price_inr": selling_price,
                "pack_weight_volume": weight_val,
                "unit_of_measure": sku_meta["unit"],
                "unit_price_per_100": unit_price_100,
                "is_magic_price_point": sku_meta["is_magic_price_point"],
                "magic_price_tier": sku_meta["magic_tier"],
                "packaging_type": sku_meta["packaging_type"],
                "marketing_redesign_claim": marketing_claim,
                "intended_behavior_archetype": sku_meta["intended_pattern"]
            })
            obs_id_counter += 1

    df_raw = pd.DataFrame(rows)
    raw_path = os.path.join("data", "raw_scraped_grocery_data.csv")
    df_raw.to_csv(raw_path, index=False)
    print(f"SUCCESS: Generated raw grocery dataset at '{raw_path}' with {len(df_raw)} records across {df_raw['sku_id'].nunique()} unique SKUs.")
    return df_raw

if __name__ == "__main__":
    generate_large_scale_dataset(target_total_rows=16800)
