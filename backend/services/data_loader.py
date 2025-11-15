"""Data loader service for loading and caching CSV data."""

from pathlib import Path
from typing import List, Optional

import pandas as pd

from backend.services.models import AvailableProduct, Fournisseur, InStoreProduct


class DataLoader:
    """Loads and caches CSV data files."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the data loader.

        Args:
            data_dir: Path to the data directory. If None, uses ../data relative to this file.
        """
        if data_dir is None:
            # Default to ../data relative to this file
            backend_dir = Path(__file__).parent.parent
            data_dir = backend_dir.parent / "data"

        self.data_dir = Path(data_dir)
        self._in_store_products: Optional[pd.DataFrame] = None
        self._available_products: Optional[pd.DataFrame] = None
        self._fournisseurs: Optional[pd.DataFrame] = None
        self._in_store_products_models: Optional[List[InStoreProduct]] = None
        self._available_products_models: Optional[List[AvailableProduct]] = None
        self._fournisseurs_models: Optional[List[Fournisseur]] = None

    def load_in_store_products(self) -> pd.DataFrame:
        """Load in-store products CSV as DataFrame."""
        if self._in_store_products is None:
            file_path = self.data_dir / "in_store_product.csv"
            self._in_store_products = pd.read_csv(file_path)
        return self._in_store_products.copy()

    def load_available_products(self) -> pd.DataFrame:
        """Load available products CSV as DataFrame."""
        if self._available_products is None:
            file_path = self.data_dir / "available_product.csv"
            self._available_products = pd.read_csv(file_path)
        return self._available_products.copy()

    def load_fournisseurs(self) -> pd.DataFrame:
        """Load fournisseurs (suppliers) CSV as DataFrame."""
        if self._fournisseurs is None:
            file_path = self.data_dir / "fournisseur.csv"
            self._fournisseurs = pd.read_csv(file_path)
        return self._fournisseurs.copy()

    def load_in_store_products_models(self) -> List[InStoreProduct]:
        """Load in-store products as Pydantic models."""
        if self._in_store_products_models is None:
            df = self.load_in_store_products()
            self._in_store_products_models = [
                InStoreProduct(**row) for row in df.to_dict("records")
            ]
        return self._in_store_products_models

    def load_available_products_models(self) -> List[AvailableProduct]:
        """Load available products as Pydantic models."""
        if self._available_products_models is None:
            df = self.load_available_products()
            self._available_products_models = [
                AvailableProduct(**row) for row in df.to_dict("records")
            ]
        return self._available_products_models

    def load_fournisseurs_models(self) -> List[Fournisseur]:
        """Load fournisseurs as Pydantic models."""
        if self._fournisseurs_models is None:
            df = self.load_fournisseurs()
            self._fournisseurs_models = [
                Fournisseur(**row) for row in df.to_dict("records")
            ]
        return self._fournisseurs_models

    def reload_all(self):
        """Reload all data from CSV files."""
        self._in_store_products = None
        self._available_products = None
        self._fournisseurs = None
        self._in_store_products_models = None
        self._available_products_models = None
        self._fournisseurs_models = None


# Global instance
_data_loader: Optional[DataLoader] = None


def get_data_loader(data_dir: Optional[Path] = None) -> DataLoader:
    """Get or create the global data loader instance."""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader(data_dir)
    return _data_loader
