"""Service for analyzing supplier alternatives and finding cheaper options."""

from pathlib import Path
from typing import List, Optional

from backend.services.data_loader import get_data_loader
from backend.services.models import CheaperAlternative


class SupplierAnalysisService:
    """Service to find cheaper supplier alternatives for in-store products."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the supplier analysis service.

        Args:
            data_dir: Path to the data directory.
        """
        self.data_loader = get_data_loader(data_dir)

    def find_cheaper_alternatives(
        self, min_savings_percent: float = 5.0, product_id: Optional[str] = None
    ) -> List[CheaperAlternative]:
        """
        Find cheaper supplier alternatives for in-store products.

        Args:
            min_savings_percent: Minimum savings percentage to flag (default: 5.0)
            product_id: Optional product ID to filter by

        Returns:
            List of CheaperAlternative models
        """
        in_store_models = self.data_loader.load_in_store_products_models()
        available_models = self.data_loader.load_available_products_models()
        fournisseurs_models = self.data_loader.load_fournisseurs_models()

        # Create lookup dictionaries for faster access
        fournisseurs_dict = {f.id: f for f in fournisseurs_models}
        available_by_name = {}
        for avail in available_models:
            if avail.name not in available_by_name:
                available_by_name[avail.name] = []
            available_by_name[avail.name].append(avail)

        # Filter by product_id if provided
        if product_id:
            in_store_models = [p for p in in_store_models if p.id == product_id]

        results = []

        # For each in-store product, find cheaper alternatives
        for product in in_store_models:
            # Find all available products with the same name
            matching_available = available_by_name.get(product.name, [])

            # Filter out current supplier and find cheaper alternatives
            for alt in matching_available:
                if alt.fournisseur == product.fournisseur_id:
                    continue

                savings = product.price - alt.price
                savings_percent = (savings / product.price) * 100

                if savings_percent >= min_savings_percent:
                    # Get supplier information
                    current_supplier = fournisseurs_dict.get(
                        product.fournisseur_id,
                        None,
                    )
                    alternative_supplier = fournisseurs_dict.get(
                        alt.fournisseur,
                        None,
                    )

                    results.append(
                        CheaperAlternative(
                            product_id=product.id,
                            product_name=product.name,
                            current_price=product.price,
                            current_supplier_id=product.fournisseur_id,
                            current_supplier_name=current_supplier.name
                            if current_supplier
                            else "Unknown",
                            current_stock=product.stock,
                            alternative_supplier_id=alt.fournisseur,
                            alternative_supplier_name=alternative_supplier.name
                            if alternative_supplier
                            else "Unknown",
                            alternative_supplier_phone=alternative_supplier.phone_number
                            if alternative_supplier
                            else "N/A",
                            alternative_price=alt.price,
                            savings_amount=savings,
                            savings_percent=savings_percent,
                            delivery_time=alt.delivery_time,
                            last_information_update=alt.last_information_update,
                        )
                    )

        # Sort by savings percentage (descending)
        results.sort(key=lambda x: x.savings_percent, reverse=True)

        return results
