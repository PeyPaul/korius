"""Root controller for API information."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Supplier Optimization API",
        "version": "0.1.0",
        "endpoints": {
            "cheaper_alternatives": "/api/suppliers/cheaper-alternatives",
            "innovative_products": "/api/products/innovative",
        },
    }
