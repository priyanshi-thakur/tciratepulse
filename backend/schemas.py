from pydantic import BaseModel, Field
from typing import Literal

class QuoteRequest(BaseModel):
    origin: str = Field(min_length=2, examples=["Mumbai"])
    destination: str = Field(min_length=2, examples=["Pune"])
    weight_kg: float = Field(gt=0, le=30000)
    vehicle_type: Literal["Tata Ace", "Pickup", "14ft Truck", "19ft Truck", "32ft MXL"]
    product_category: Literal["General", "FMCG", "Electronics", "Pharma", "Perishable", "Industrial"]
    sla: Literal["Standard", "Express", "Critical"] = "Standard"
    customer_loyalty: Literal["New", "Regular", "Strategic"] = "Regular"

class QuoteResponse(BaseModel):
    tariff_inr: float
    low_inr: float
    high_inr: float
    confidence: str
    distance_km: float
    travel_hours: float
    route_source: str
    weather: dict
    drivers: list[dict]
    alerts: list[dict]
    factors: dict
    trend: list[dict]
    model_metrics: dict
