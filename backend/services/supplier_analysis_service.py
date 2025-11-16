"""Service for analyzing supplier alternatives and finding cheaper options."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

import pandas as pd

from backend.services.data_loader import get_data_loader
from backend.services.models import CheaperAlternative, SupplierROI, SupplierROIResponse


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

    def get_supplier_roi(self) -> SupplierROIResponse:
        """
        Calculate supplier ROI and performance metrics.

        Returns:
            SupplierROIResponse with supplier performance data
        """
        # Load all data
        fournisseurs_models = self.data_loader.load_fournisseurs_models()
        in_store_models = self.data_loader.load_in_store_products_models()
        available_models = self.data_loader.load_available_products_models()
        orders_df = self.data_loader.load_orders()

        # Calculate monthly spend from orders (estimate from last 30 days or average)
        orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
        orders_df["estimated_time_arrival"] = pd.to_datetime(
            orders_df["estimated_time_arrival"]
        )

        # Get orders from last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = orders_df[orders_df["order_date"] >= thirty_days_ago]

        # Calculate spend per supplier (quantity * price from in-store products)
        in_store_by_name = {p.name: p for p in in_store_models}

        supplier_spend = {}
        supplier_order_counts = {}
        supplier_late_deliveries = {}
        supplier_on_time_deliveries = {}

        for _, order in recent_orders.iterrows():
            supplier_id = order["fournisseur_id"]
            product_name = order["product_name"]
            quantity = order["quantity"]

            # Find product price
            product = in_store_by_name.get(product_name)
            if product and product.fournisseur_id == supplier_id:
                price = product.price
                spend = quantity * price
                supplier_spend[supplier_id] = supplier_spend.get(supplier_id, 0) + spend
                supplier_order_counts[supplier_id] = (
                    supplier_order_counts.get(supplier_id, 0) + 1
                )

                # Check delivery performance
                if pd.notna(order.get("time_of_arrival")):
                    actual = pd.to_datetime(order["time_of_arrival"])
                    estimated = pd.to_datetime(order["estimated_time_arrival"])
                    if actual > estimated:
                        supplier_late_deliveries[supplier_id] = (
                            supplier_late_deliveries.get(supplier_id, 0) + 1
                        )
                    else:
                        supplier_on_time_deliveries[supplier_id] = (
                            supplier_on_time_deliveries.get(supplier_id, 0) + 1
                        )

        # If no recent orders, estimate from all orders
        if not supplier_spend:
            for _, order in orders_df.iterrows():
                supplier_id = order["fournisseur_id"]
                product_name = order["product_name"]
                quantity = order["quantity"]

                product = in_store_by_name.get(product_name)
                if product and product.fournisseur_id == supplier_id:
                    price = product.price
                    spend = quantity * price
                    supplier_spend[supplier_id] = (
                        supplier_spend.get(supplier_id, 0) + spend
                    )

        # Calculate performance metrics for each supplier
        supplier_roi_list = []

        for supplier in fournisseurs_models:
            supplier_id = supplier.id
            monthly_spend = supplier_spend.get(supplier_id, 0.0)

            # Count products from this supplier
            supplier_products = [
                p for p in in_store_models if p.fournisseur_id == supplier_id
            ]
            product_count = len(supplier_products)

            # Calculate price competitiveness (how many cheaper alternatives exist)
            cheaper_alternatives_count = 0
            for product in supplier_products:
                matching_available = [
                    a
                    for a in available_models
                    if a.name == product.name and a.fournisseur != supplier_id
                ]
                cheaper = [a for a in matching_available if a.price < product.price]
                cheaper_alternatives_count += len(cheaper)

            # Calculate delivery performance
            total_deliveries = supplier_on_time_deliveries.get(
                supplier_id, 0
            ) + supplier_late_deliveries.get(supplier_id, 0)
            delivery_score = 100.0
            if total_deliveries > 0:
                on_time_rate = (
                    supplier_on_time_deliveries.get(supplier_id, 0) / total_deliveries
                )
                delivery_score = on_time_rate * 100

            # Calculate performance score (0-100)
            # Factors: delivery performance (40%), price competitiveness (30%), order volume (20%), product diversity (10%)
            price_score = max(
                0, 100 - (cheaper_alternatives_count / max(1, product_count)) * 30
            )
            volume_score = (
                min(100, (monthly_spend / 1000) * 20) if monthly_spend > 0 else 0
            )
            diversity_score = min(100, product_count * 5)

            performance = (
                delivery_score * 0.4
                + price_score * 0.3
                + volume_score * 0.2
                + diversity_score * 0.1
            )
            performance = max(0, min(100, performance))

            # Determine status
            if performance >= 90:
                status = "excellent"
            elif performance >= 75:
                status = "good"
            elif performance >= 60:
                status = "fair"
            else:
                status = "warning"

            # Determine trend (simplified - could be improved with historical data)
            if monthly_spend > 5000:
                trend = "up"
            elif monthly_spend > 1000:
                trend = "stable"
            else:
                trend = "down"

            # Collect issues
            issues = []
            if supplier_late_deliveries.get(supplier_id, 0) > 0:
                issues.append("Late Deliveries")
            if cheaper_alternatives_count > product_count * 0.5:
                issues.append("Price Increases")
            if total_deliveries == 0 and monthly_spend == 0:
                issues.append("No Recent Activity")

            supplier_roi_list.append(
                SupplierROI(
                    id=supplier.id,
                    name=supplier.name,
                    performance=round(performance, 1),
                    monthly_spend=round(monthly_spend, 2),
                    status=status,
                    trend=trend,
                    issues=issues,
                    phone_number=supplier.phone_number,
                )
            )

        # Sort by performance (descending)
        supplier_roi_list.sort(key=lambda x: x.performance, reverse=True)

        # Calculate summary metrics
        total_monthly_spend = sum(s.monthly_spend for s in supplier_roi_list)
        avg_performance = (
            sum(s.performance for s in supplier_roi_list) / len(supplier_roi_list)
            if supplier_roi_list
            else 0
        )
        excellent_count = sum(1 for s in supplier_roi_list if s.status == "excellent")
        warning_count = sum(1 for s in supplier_roi_list if s.status == "warning")

        return SupplierROIResponse(
            suppliers=supplier_roi_list,
            total_count=len(supplier_roi_list),
            total_monthly_spend=round(total_monthly_spend, 2),
            avg_performance=round(avg_performance, 1),
            excellent_count=excellent_count,
            warning_count=warning_count,
        )
