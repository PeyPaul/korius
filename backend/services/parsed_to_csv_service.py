from pathlib import Path
from typing import List, Optional

from backend.services.data_loader import get_data_loader
from backend.services.models import ModifiedProductInformation


class ParsedToCsvService:
    """Service to convert parsed data to CSV."""

    def __init__(
        self,
        modified_product_information: List[ModifiedProductInformation],
        data_dir: Optional[Path] = None,
    ):
        """Initialize the parsed to CSV service."""
        if data_dir is None:
            # Default to ../data relative to this file
            backend_dir = Path(__file__).parent.parent
            data_dir = backend_dir.parent / "data"
        self.data_dir = Path(data_dir)
        self.modified_product_information = modified_product_information
        self.data_loader = get_data_loader(self.data_dir)
        self.fournisseurs = self.data_loader.load_fournisseurs()
        self.available_products = self.data_loader.load_available_products()

    def prepare_product_information(self):
        """Prepare product information for CSV."""
        for product in self.modified_product_information:
            product.product_id = self.available_products.loc[
                self.available_products.name == product.product_name, "id"
            ].values[0]
            product.fournisseur_id = self.fournisseurs.loc[
                self.fournisseurs.name == product.fournisseur_name, "id"
            ].values[0]

    def update_product_information(self):
        """Update product information."""
        for product in self.modified_product_information:
            if product.product_id and product.fournisseur_id:
                # Select the row matching both product_id and fournisseur_id in available_products
                mask = (self.available_products.id == product.product_id) & (
                    self.available_products.fournisseur_id == product.fournisseur_id
                )
                # update price if new price is provided
                if product.new_price is not None:
                    self.available_products.loc[mask, "price"] = product.new_price
                # update delivery time if new delivery time is provided
                if product.new_delivery_time is not None:
                    self.available_products.loc[mask, "delivery_time"] = (
                        product.new_delivery_time
                    )
                # update last information update
                self.available_products.loc[mask, "last_information_update"] = (
                    product.new_last_information_update
                )

    def save_to_csv(self):
        """Save modified product information to CSV."""
        self.available_products.to_csv(
            self.data_dir / "available_product.csv", index=False
        )

    def convert_to_csv(self) -> str:
        """Convert modified product information to CSV."""
        return "\n".join([row.to_csv() for row in self.modified_product_information])
