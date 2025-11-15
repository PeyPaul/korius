"""Product controller for innovative products endpoints."""

from fastapi import APIRouter

from backend.services.models import InnovativeProductsResponse
from backend.services.product_discovery_service import ProductDiscoveryService

router = APIRouter(prefix="/api/products", tags=["products"])

# Initialize service
product_service = ProductDiscoveryService()


@router.get("/innovative", response_model=InnovativeProductsResponse)
async def get_innovative_products(min_suppliers: int = 1, sort_by: str = "suppliers"):
    """
    Get list of innovative products not currently in store.

    Args:
        min_suppliers: Minimum number of suppliers required (default: 1)
        sort_by: Sort criteria - 'price', 'suppliers', or 'delivery_time' (default: 'suppliers')

    Returns:
        List of innovative products with supplier information
    """
    if sort_by not in ["price", "suppliers", "delivery_time"]:
        sort_by = "suppliers"

    products = product_service.find_innovative_products(
        min_suppliers=min_suppliers, sort_by=sort_by
    )

    return InnovativeProductsResponse(
        products=products, total_count=len(products), min_suppliers=min_suppliers
    )
