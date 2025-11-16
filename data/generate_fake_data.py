"""
Script to generate fake datasets for the hackathon project.
Generates:
- Fournisseur (Suppliers)
- In store products
- Available products (can have multiple suppliers per product)
- Orders (Customer orders to suppliers)
"""

import random
import uuid
from datetime import datetime, timedelta

import pandas as pd

# Set random seed for reproducibility
random.seed(42)


# Generate Fournisseur (Suppliers)
def generate_fournisseurs(n=50):
    """Generate fake supplier data"""
    suppliers = []
    company_names = [
        "PharmaDistrib",
        "MedSupply Co.",
        "Health Products Inc.",
        "Pharmaceutical Express",
        "MediCare Distributors",
        "Pharma Solutions",
        "Medical Supply Pro",
        "Health Warehouse",
        "Pharma Direct",
        "MediSupply Network",
        "Pharmaceutical Hub",
        "Health Distributors",
        "MedSupply Express",
        "Pharma Central",
        "Medical Products Ltd",
        "Health Supply Chain",
        "Pharma Depot",
        "MediCare Solutions",
        "Pharmaceutical Network",
        "Health Express Pro",
        "MedSupply Direct",
        "Pharma Warehouse",
        "Medical Distributors",
        "Health Products Pro",
        "Pharma Solutions Plus",
        "MediCare Express",
        "Pharmaceutical Depot",
        "Health Supply Network",
        "MedSupply Central",
        "Pharma Network Pro",
        "Medical Express",
        "Health Distributors Plus",
        "Pharma Direct Pro",
        "MediCare Warehouse",
        "Pharmaceutical Solutions",
        "Health Supply Express",
        "MedSupply Network Pro",
        "Pharma Central Plus",
        "Medical Products Express",
        "Health Distributors Pro",
        "Pharma Depot Plus",
        "MediCare Direct",
        "Pharmaceutical Network Pro",
        "Health Express Network",
        "MedSupply Solutions",
        "Pharma Warehouse Pro",
        "Medical Distributors Plus",
        "Health Products Express",
        "Pharma Solutions Network",
        "MediCare Supply Pro",
        "Pharmaceutical Direct",
    ]

    for _ in range(1, n + 1):
        # Generate UUID with supp_ prefix
        supplier_id = f"supp_{uuid.uuid4()}"
        name = (
            random.choice(company_names)
            + f" {random.choice(['North', 'South', 'East', 'West', 'International', 'Global'])}"
        )
        # Generate French phone numbers
        phone = f"+33 {random.randint(1, 9)}{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"
        suppliers.append({"id": supplier_id, "name": name, "phone_number": phone})

    return pd.DataFrame(suppliers)


# Generate In Store Products from Available Products
def generate_in_store_products(available_products_df, n=200):
    """Generate in-store products as a subset of available products.
    Each product name appears only once with one supplier, and price matches available_products.
    """
    products = []

    # Get unique product names from available products
    unique_product_names = available_products_df["name"].unique().tolist()

    # Randomly select which products will be in-store (up to n products)
    products_to_include = random.sample(
        unique_product_names, min(n, len(unique_product_names))
    )

    for product_name in products_to_include:
        # Get all available entries for this product (with different suppliers)
        product_entries = available_products_df[
            available_products_df["name"] == product_name
        ]

        # Randomly select one supplier for this product
        selected_entry = product_entries.sample(1).iloc[0]

        # Stock between 0 and 500
        stock = random.randint(0, 500)

        products.append(
            {
                "id": selected_entry["id"],
                "name": selected_entry["name"],
                "price": selected_entry["price"],  # Use price from available_products
                "fournisseur_id": selected_entry[
                    "fournisseur"
                ],  # Use supplier from available_products
                "stock": stock,
            }
        )

    return pd.DataFrame(products)


# Generate Available Products (can have multiple suppliers per product)
def generate_available_products(
    product_names_list, fournisseur_df, product_id_map=None
):
    """Generate fake available product data with multiple suppliers per product"""
    available_products = []

    # Use provided product_id_map or create a new one
    if product_id_map is None:
        product_id_map = {}

    # Generate entries where each product can have multiple suppliers
    for product_name in product_names_list:
        # Generate a unique ID for this product name (if not already created)
        if product_name not in product_id_map:
            product_id_map[product_name] = f"prod_{uuid.uuid4()}"

        # Use the same ID for all entries with this product name
        product_id = product_id_map[product_name]

        # Each product can be available from 1 to 4 suppliers
        num_suppliers = random.randint(1, 4)
        selected_suppliers = random.sample(
            fournisseur_df["id"].tolist(), min(num_suppliers, len(fournisseur_df))
        )

        for supplier_id in selected_suppliers:
            # Price can vary by supplier (wholesale vs retail)
            base_price = random.uniform(2, 150)
            # Supplier price might be 10-30% different from store price
            price = round(base_price * random.uniform(0.7, 1.3), 2)

            # Delivery time between 1 and 14 days
            delivery_time = random.randint(1, 14)

            # Last information update between 1 and 90 days ago
            days_ago = random.randint(1, 90)
            last_update = (datetime.now() - timedelta(days=days_ago)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            available_products.append(
                {
                    "id": product_id,
                    "name": product_name,
                    "fournisseur": supplier_id,
                    "price": price,
                    "delivery_time": delivery_time,
                    "last_information_update": last_update,
                }
            )

    # Add some additional products that might not be in store
    additional_products = [
        "Amoxicilline 500mg",
        "Ciprofloxacine 500mg",
        "Azithromycine 250mg",
        "Doxycycline 100mg",
        "Métronidazole 500mg",
        "Insuline Glulisine",
        "Métformine 500mg",
        "Atorvastatine 20mg",
        "Amlodipine 5mg",
        "Lisinopril 10mg",
        "Oméprazole 20mg",
        "Lansoprazole 30mg",
        "Montélukast 10mg",
        "Salbutamol Spray",
        "Fluticasone Nasal",
    ]

    for product_name in additional_products:
        # Generate a unique ID for this product name (if not already created)
        if product_name not in product_id_map:
            product_id_map[product_name] = f"prod_{uuid.uuid4()}"

        # Use the same ID for all entries with this product name
        product_id = product_id_map[product_name]

        num_suppliers = random.randint(1, 3)
        selected_suppliers = random.sample(
            fournisseur_df["id"].tolist(), min(num_suppliers, len(fournisseur_df))
        )

        for supplier_id in selected_suppliers:
            base_price = random.uniform(5, 100)
            price = round(base_price * random.uniform(0.7, 1.3), 2)
            delivery_time = random.randint(1, 14)
            days_ago = random.randint(1, 90)
            last_update = (datetime.now() - timedelta(days=days_ago)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            available_products.append(
                {
                    "id": product_id,
                    "name": product_name,
                    "fournisseur": supplier_id,
                    "price": price,
                    "delivery_time": delivery_time,
                    "last_information_update": last_update,
                }
            )

    return pd.DataFrame(available_products)


# Generate Orders
def generate_orders(available_products_df, fournisseur_df, in_store_products_df, n=200):
    """Generate fake order data with diverse supplier performance.

    Creates good and bad suppliers based on:
    - Delivery performance (on-time vs late)
    - Order volume (number and size of orders)
    - Order recency (more recent orders for good suppliers)

    Args:
        available_products_df: DataFrame of available products
        fournisseur_df: DataFrame of suppliers
        in_store_products_df: DataFrame of in-store products
        n: Number of orders to generate

    Returns:
        DataFrame with columns: order_id, product_name, quantity, fournisseur_id,
                               estimated_time_arrival, time_of_arrival, order_date
    """
    orders = []

    # Categorize suppliers into performance tiers
    # Get suppliers that are actually used in in_store_products
    used_suppliers = set(in_store_products_df["fournisseur_id"].unique())
    supplier_list = fournisseur_df[fournisseur_df["id"].isin(used_suppliers)][
        "id"
    ].tolist()

    if not supplier_list:
        # Fallback: use all suppliers
        supplier_list = fournisseur_df["id"].tolist()

    # Divide suppliers into tiers
    # Exactly 5 very bad suppliers, rest distributed among excellent, good, fair
    random.shuffle(supplier_list)
    n_suppliers = len(supplier_list)

    # Select exactly 5 very bad suppliers
    num_warning = min(5, n_suppliers)
    warning_suppliers = set(supplier_list[:num_warning])
    remaining_suppliers = supplier_list[num_warning:]

    # Distribute remaining suppliers: 25% excellent, 35% good, 40% fair
    n_remaining = len(remaining_suppliers)
    excellent_suppliers = set(remaining_suppliers[: int(n_remaining * 0.25)])
    good_suppliers = set(
        remaining_suppliers[int(n_remaining * 0.25) : int(n_remaining * 0.60)]
    )
    fair_suppliers = set(remaining_suppliers[int(n_remaining * 0.60) :])

    # Create supplier performance profiles
    supplier_profiles = {}
    for supp_id in excellent_suppliers:
        supplier_profiles[supp_id] = {
            "on_time_rate": 0.95,  # 95% on-time
            "avg_delay_days": -1,  # Often early or on-time
            "delay_range": (-3, 1),  # Early to slightly late
            "order_frequency": 0.25,  # 25% of orders
            "quantity_range": (100, 500),  # Larger orders
            "recent_order_rate": 0.6,  # 60% of orders in last 30 days
        }
    for supp_id in good_suppliers:
        supplier_profiles[supp_id] = {
            "on_time_rate": 0.85,  # 85% on-time
            "avg_delay_days": 0,  # Usually on-time
            "delay_range": (-2, 2),
            "order_frequency": 0.30,  # 30% of orders
            "quantity_range": (50, 400),
            "recent_order_rate": 0.5,  # 50% of orders in last 30 days
        }
    for supp_id in fair_suppliers:
        supplier_profiles[supp_id] = {
            "on_time_rate": 0.70,  # 70% on-time
            "avg_delay_days": 2,  # Often slightly late
            "delay_range": (-1, 4),
            "order_frequency": 0.30,  # 30% of orders
            "quantity_range": (30, 300),
            "recent_order_rate": 0.3,  # 30% of orders in last 30 days
        }
    for supp_id in warning_suppliers:
        supplier_profiles[supp_id] = {
            "on_time_rate": 0.50,  # 50% on-time (many late deliveries)
            "avg_delay_days": 4,  # Often late
            "delay_range": (0, 8),  # Often late, rarely early
            "order_frequency": 0.15,  # 15% of orders (fewer orders)
            "quantity_range": (10, 200),  # Smaller orders
            "recent_order_rate": 0.1,  # 10% of orders in last 30 days (inactive)
        }

    # Generate orders weighted by supplier performance
    supplier_weights = []
    supplier_ids = []
    for supp_id, profile in supplier_profiles.items():
        # Get products available from this supplier
        supplier_products = available_products_df[
            available_products_df["fournisseur"] == supp_id
        ]
        if len(supplier_products) > 0:
            supplier_ids.append(supp_id)
            # Weight by order_frequency
            supplier_weights.append(profile["order_frequency"] * len(supplier_products))

    # Normalize weights
    total_weight = sum(supplier_weights)
    if total_weight > 0:
        supplier_weights = [w / total_weight for w in supplier_weights]

    # Ensure minimum monthly spend for all suppliers
    min_orders_per_supplier = (
        2  # Minimum orders per supplier (at least 2 recent orders)
    )

    # Create a mapping of products in in_store_products by supplier
    # This ensures orders match what the analysis service expects
    in_store_by_supplier = {}
    for _, row in in_store_products_df.iterrows():
        supp_id = row["fournisseur_id"]
        if supp_id not in in_store_by_supplier:
            in_store_by_supplier[supp_id] = []
        in_store_by_supplier[supp_id].append(row)

    # First, generate minimum orders for each supplier to ensure monthly spend
    for supp_id in supplier_ids:
        profile = supplier_profiles.get(
            supp_id,
            {
                "on_time_rate": 0.7,
                "avg_delay_days": 1,
                "delay_range": (-2, 5),
                "order_frequency": 0.2,
                "quantity_range": (50, 300),  # Reasonable minimum quantity
                "recent_order_rate": 1.0,  # All minimum orders should be recent
            },
        )

        # Get products from in_store_products for this supplier (to ensure spend is calculated)
        supplier_in_store_products = in_store_by_supplier.get(supp_id, [])

        if len(supplier_in_store_products) == 0:
            # Fallback: try to find products from available_products
            supplier_products = available_products_df[
                available_products_df["fournisseur"] == supp_id
            ]
            if len(supplier_products) == 0:
                continue
            # Use available products as fallback
            product_list = supplier_products.to_dict("records")
        else:
            # Use in_store products (preferred for spend calculation)
            product_list = supplier_in_store_products

        for _ in range(min_orders_per_supplier):
            # Select a random product from the list
            product_entry = random.choice(product_list)
            order_id = f"order_{uuid.uuid4()}"
            # Use profile quantity range, but ensure minimum quantity for monthly spend
            qty_min, qty_max = profile["quantity_range"]
            quantity = random.randint(max(50, qty_min), qty_max)  # At least 50 units

            # Recent order (last 30 days) to ensure monthly spend
            days_ago = random.randint(1, 30)
            order_date = datetime.now() - timedelta(days=days_ago)

            # Get delivery time from available_products or use default
            # Handle both dict and Series/DataFrame row formats
            if isinstance(product_entry, dict):
                product_name = product_entry["name"]
            else:
                product_name = (
                    product_entry.get("name", "")
                    if hasattr(product_entry, "get")
                    else product_entry["name"]
                )

            available_product = available_products_df[
                (available_products_df["name"] == product_name)
                & (available_products_df["fournisseur"] == supp_id)
            ]
            if len(available_product) > 0:
                estimated_delivery_days = int(
                    available_product.iloc[0]["delivery_time"]
                )
            else:
                estimated_delivery_days = random.randint(1, 14)  # Default
            estimated_time_arrival = order_date + timedelta(
                days=estimated_delivery_days
            )

            # Most minimum orders should be delivered (on-time or late based on supplier)
            should_have_arrived = order_date < datetime.now() - timedelta(
                days=estimated_delivery_days
            )

            if should_have_arrived and random.random() < profile["on_time_rate"]:
                delay = random.randint(*profile["delay_range"])
                time_of_arrival = estimated_time_arrival + timedelta(days=delay)
                if time_of_arrival > datetime.now():
                    time_of_arrival = datetime.now() - timedelta(
                        days=random.randint(1, 3)
                    )
            elif should_have_arrived:
                delay = random.randint(
                    profile["delay_range"][0] + 1, profile["delay_range"][1] + 3
                )
                time_of_arrival = estimated_time_arrival + timedelta(days=delay)
                if time_of_arrival > datetime.now():
                    time_of_arrival = datetime.now() - timedelta(
                        days=random.randint(1, 2)
                    )
            else:
                time_of_arrival = None

            orders.append(
                {
                    "order_id": order_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "fournisseur_id": supp_id,
                    "estimated_time_arrival": estimated_time_arrival.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "time_of_arrival": time_of_arrival.strftime("%Y-%m-%d %H:%M:%S")
                    if time_of_arrival
                    else None,
                    "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    # Now generate the remaining orders weighted by supplier performance
    remaining_orders = n - len(orders)
    for _ in range(remaining_orders):
        # Select supplier based on weights
        if supplier_ids and supplier_weights:
            selected_supplier_id = random.choices(
                supplier_ids, weights=supplier_weights
            )[0]
        else:
            # Fallback: random selection
            product_entry = available_products_df.sample(1).iloc[0]
            selected_supplier_id = product_entry["fournisseur"]

        profile = supplier_profiles.get(
            selected_supplier_id,
            {
                "on_time_rate": 0.7,
                "avg_delay_days": 1,
                "delay_range": (-2, 5),
                "order_frequency": 0.2,
                "quantity_range": (10, 500),
                "recent_order_rate": 0.4,
            },
        )

        # Get products from in_store_products for this supplier (to ensure spend is calculated)
        supplier_in_store_products = in_store_by_supplier.get(selected_supplier_id, [])

        if len(supplier_in_store_products) == 0:
            # Fallback: try available_products
            supplier_products = available_products_df[
                available_products_df["fournisseur"] == selected_supplier_id
            ]
            if len(supplier_products) == 0:
                # Last resort: any product
                product_entry = available_products_df.sample(1).iloc[0]
            else:
                product_entry = supplier_products.sample(1).iloc[0]
        else:
            # Use in_store products (preferred for spend calculation)
            product_entry = random.choice(supplier_in_store_products)

        # Generate order ID
        order_id = f"order_{uuid.uuid4()}"

        # Quantity based on supplier tier
        quantity = random.randint(*profile["quantity_range"])

        # Order date: more recent orders for better suppliers
        if random.random() < profile["recent_order_rate"]:
            # Recent order (last 30 days)
            days_ago = random.randint(1, 30)
        else:
            # Older order (31-180 days ago)
            days_ago = random.randint(31, 180)

        order_date = datetime.now() - timedelta(days=days_ago)

        # Estimated delivery time from available_products or use default
        product_name = (
            product_entry["name"]
            if isinstance(product_entry, dict)
            else product_entry.get("name", "")
        )
        available_product = available_products_df[
            (available_products_df["name"] == product_name)
            & (available_products_df["fournisseur"] == selected_supplier_id)
        ]
        if len(available_product) > 0:
            estimated_delivery_days = int(available_product.iloc[0]["delivery_time"])
        else:
            estimated_delivery_days = random.randint(1, 14)  # Default

        estimated_time_arrival = order_date + timedelta(days=estimated_delivery_days)

        # Time of arrival based on supplier performance
        # Check if order should have arrived by now
        should_have_arrived = order_date < datetime.now() - timedelta(
            days=estimated_delivery_days
        )

        if should_have_arrived and random.random() < profile["on_time_rate"]:
            # Order has been delivered (on-time or early)
            delay = random.randint(*profile["delay_range"])
            time_of_arrival = estimated_time_arrival + timedelta(days=delay)
            # Make sure arrival is not in the future
            if time_of_arrival > datetime.now():
                time_of_arrival = datetime.now() - timedelta(days=random.randint(1, 3))
        elif should_have_arrived:
            # Order is late (delivered but late)
            delay = random.randint(
                profile["delay_range"][0] + 1, profile["delay_range"][1] + 3
            )
            time_of_arrival = estimated_time_arrival + timedelta(days=delay)
            if time_of_arrival > datetime.now():
                time_of_arrival = datetime.now() - timedelta(days=random.randint(1, 2))
        else:
            # Order is still pending (not yet due)
            if random.random() < 0.3:  # 30% chance of pending orders
                time_of_arrival = None
            else:
                # Some pending orders might actually be delivered early
                delay = random.randint(-2, 0)
                time_of_arrival = estimated_time_arrival + timedelta(days=delay)
                if time_of_arrival > datetime.now():
                    time_of_arrival = None

        # Get product name (handle both dict and Series)
        if isinstance(product_entry, dict):
            product_name = product_entry["name"]
        else:
            product_name = (
                product_entry.get("name", "")
                if hasattr(product_entry, "get")
                else product_entry["name"]
            )

        orders.append(
            {
                "order_id": order_id,
                "product_name": product_name,
                "quantity": quantity,
                "fournisseur_id": selected_supplier_id,
                "estimated_time_arrival": estimated_time_arrival.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "time_of_arrival": time_of_arrival.strftime("%Y-%m-%d %H:%M:%S")
                if time_of_arrival
                else None,
                "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return pd.DataFrame(orders)


# Main execution
if __name__ == "__main__":
    print("Generating fake datasets...")

    # Define product names list
    product_names = [
        "Paracétamol 500mg",
        "Ibuprofène 400mg",
        "Aspirine 500mg",
        "Doliprane 1000mg",
        "Spasfon 80mg",
        "Smecta Sachets",
        "Strepsils Pastilles",
        "Vicks Vaporub 50g",
        "Biafine Crème",
        "Bétadine Solution",
        "Pansements Adhésifs",
        "Compresses Stériles",
        "Seringues 5ml",
        "Thermomètre Digital",
        "Tensiomètre Électronique",
        "Gants Nitrile Boîte",
        "Masque Chirurgical",
        "Alcool à 70°",
        "Sérum Physiologique",
        "Vitamine D3 1000UI",
        "Vitamine C 1000mg",
        "Magnésium 300mg",
        "Fer 14mg",
        "Oméga 3 Capsules",
        "Probiotiques Gélules",
        "Mélatonine 1mg",
        "Ginkgo Biloba",
        "Ginseng Extrait",
        "Echinacée Gélules",
        "Millepertuis",
        "Valériane Comprimés",
        "Passiflore Gélules",
        "Aubépine Tisane",
        "Camomille Sachets",
        "Tilleul Infusion",
        "Sirop Toux Sèche",
        "Sirop Toux Grasse",
        "Pastilles Miel Citron",
        "Spray Nasal Salin",
        "Collyre Larmes Artificielles",
        "Bain de Bouche",
        "Dentifrice Fluoré",
        "Brosse à Dents",
        "Fil Dentaire",
        "Bain de Bouche Antiseptique",
        "Crème Solaire SPF50",
        "Crème Hydratante Visage",
        "Shampoing Antipelliculaire",
        "Savon Dermatologique",
        "Crème Réparatrice Mains",
    ]

    # Generate datasets
    fournisseurs = generate_fournisseurs(50)

    # Create a shared product ID mapping so products with the same name
    # have the same ID in both in_store_product and available_product
    product_id_map = {}

    # Generate available_products first (with all products and multiple suppliers)
    available_products = generate_available_products(
        product_names, fournisseurs, product_id_map
    )

    # Generate in_store_products as a subset of available_products
    # Each product name appears only once with one supplier, price matches available_products
    in_store_products = generate_in_store_products(available_products, 200)

    # Generate orders based on available products with diverse supplier performance
    orders = generate_orders(available_products, fournisseurs, in_store_products, 200)

    # Save to CSV files
    fournisseurs.to_csv("fournisseur.csv", index=False)
    in_store_products.to_csv("in_store_product.csv", index=False)
    available_products.to_csv("available_product.csv", index=False)
    orders.to_csv("orders.csv", index=False)

    print(f"✓ Generated {len(fournisseurs)} suppliers")
    print(f"✓ Generated {len(in_store_products)} in-store products")
    print(f"✓ Generated {len(available_products)} available product entries")
    print(f"✓ Generated {len(orders)} orders")
    print("\nFiles created:")
    print("  - fournisseur.csv")
    print("  - in_store_product.csv")
    print("  - available_product.csv")
    print("  - orders.csv")
