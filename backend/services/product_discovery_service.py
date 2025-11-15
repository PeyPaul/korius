"""Service for discovering innovative products not currently in store."""

from pathlib import Path
from typing import List, Optional

from backend.services.data_loader import get_data_loader
from backend.services.models import InnovativeProduct, SupplierInfo


class ProductDiscoveryService:
    """Service to discover innovative products not currently in store."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the product discovery service.

        Args:
            data_dir: Path to the data directory.
        """
        self.data_loader = get_data_loader(data_dir)

    def find_innovative_products(
        self, min_suppliers: int = 1, sort_by: str = "suppliers"
    ) -> List[InnovativeProduct]:
        """
        Find products available from suppliers but not currently in store.

        Args:
            min_suppliers: Minimum number of suppliers required (default: 1)
            sort_by: Sort criteria - 'price', 'suppliers', or 'delivery_time' (default: 'suppliers')

        Returns:
            List of InnovativeProduct models
        """
        in_store_models = self.data_loader.load_in_store_products_models()
        available_models = self.data_loader.load_available_products_models()
        fournisseurs_models = self.data_loader.load_fournisseurs_models()

        # Get unique product names from in-store products
        in_store_names = {p.name for p in in_store_models}

        # Get unique product names from available products
        available_names = {p.name for p in available_models}

        # Find products in available but not in store
        innovative_names = available_names - in_store_names

        # Group available products by name
        available_by_name = {}
        for avail in available_models:
            if avail.name not in available_by_name:
                available_by_name[avail.name] = []
            available_by_name[avail.name].append(avail)

        # Create supplier lookup
        fournisseurs_dict = {f.id: f for f in fournisseurs_models}

        results = []

        # For each innovative product, aggregate supplier information
        for product_name in innovative_names:
            product_entries = available_by_name.get(product_name, [])

            # Filter by minimum suppliers
            if len(product_entries) < min_suppliers:
                continue

            # Aggregate supplier information
            prices = [p.price for p in product_entries]
            delivery_times = [p.delivery_time for p in product_entries]

            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            min_delivery_time = min(delivery_times)
            avg_delivery_time = sum(delivery_times) / len(delivery_times)

            # Get unique supplier IDs and create supplier details
            supplier_ids = {p.fournisseur for p in product_entries}
            supplier_details = []
            for supplier_id in supplier_ids:
                supplier = fournisseurs_dict.get(supplier_id)
                if supplier:
                    supplier_details.append(
                        SupplierInfo(
                            id=supplier.id,
                            name=supplier.name,
                            phone=supplier.phone_number,
                        )
                    )

            results.append(
                InnovativeProduct(
                    product_name=product_name,
                    supplier_count=len(product_entries),
                    avg_price=avg_price,
                    min_price=min_price,
                    max_price=max_price,
                    min_delivery_time=min_delivery_time,
                    avg_delivery_time=avg_delivery_time,
                    suppliers=supplier_details,
                )
            )

        # Sort results
        if sort_by == "price":
            results.sort(key=lambda x: x.avg_price)
        elif sort_by == "delivery_time":
            results.sort(key=lambda x: x.min_delivery_time)
        else:  # sort_by == "suppliers" (default)
            results.sort(key=lambda x: x.supplier_count, reverse=True)

        return results
