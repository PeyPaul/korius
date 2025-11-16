"""Supplier controller for cheaper alternatives endpoints."""

from typing import Optional

from fastapi import APIRouter

from backend.services.models import CheaperAlternativesResponse, SupplierROIResponse
from backend.services.supplier_analysis_service import SupplierAnalysisService

router = APIRouter(prefix="/api/suppliers", tags=["suppliers"])

# Initialize service
supplier_service = SupplierAnalysisService()


@router.get("/cheaper-alternatives", response_model=CheaperAlternativesResponse)
async def get_cheaper_alternatives(
    min_savings_percent: float = 5.0, product_id: Optional[str] = None
):
    """
    Get cheaper supplier alternatives for in-store products.

    Args:
        min_savings_percent: Minimum savings percentage to flag (default: 5.0)
        product_id: Optional product ID to filter by

    Returns:
        List of cheaper alternatives with supplier information
    """
    alternatives = supplier_service.find_cheaper_alternatives(
        min_savings_percent=min_savings_percent, product_id=product_id
    )

    return CheaperAlternativesResponse(
        alternatives=alternatives,
        total_count=len(alternatives),
        min_savings_percent=min_savings_percent,
    )


@router.get("/roi", response_model=SupplierROIResponse)
async def get_supplier_roi():
    """
    Get supplier ROI and performance metrics.

    Returns:
        SupplierROIResponse with supplier performance data including:
        - Performance scores
        - Monthly spending
        - Status and trends
        - Active issues
    """
    return supplier_service.get_supplier_roi()
