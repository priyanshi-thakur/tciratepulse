from pydantic import BaseModel,Field
from typing import Literal
class QuoteRequest(BaseModel):
 origin:str=Field(min_length=2,examples=["Mumbai"]);destination:str=Field(min_length=2,examples=["Pune"]);weight_kg:float=Field(gt=0,le=30000)
 vehicle_type:Literal["Tata Ace","Pickup","14ft Truck","19ft Truck","32ft MXL"]="Pickup"
 product_category:Literal["General","FMCG","Electronics","Pharma","Perishable","Industrial","Fragile","High-value","Hazard-sensitive"]="General"
 sla:Literal["Standard","Express","Critical"]="Standard";customer_loyalty:Literal["New","Regular","Strategic"]="Regular"
 security_level:Literal["Normal","Elevated","High"]|None=None;insurance_option:Literal["Basic","Enhanced","Full"]|None=None;shipment_value_inr:float|None=Field(default=None,gt=0)
 fuel_cost_index:float|None=Field(default=None,ge=.7,le=1.5);labour_cost_index:float|None=Field(default=None,ge=.7,le=1.5);regulatory_impact_index:float|None=Field(default=None,ge=.8,le=1.3);geopolitical_risk_index:float|None=Field(default=None,ge=.8,le=1.3)
class QuoteResponse(BaseModel):
 tariff_inr:float;low_inr:float;high_inr:float;confidence:str;distance_km:float;travel_hours:float;route_source:str;weather:dict;drivers:list[dict];alerts:list[dict];factors:dict;factor_summary:list[dict];trend:list[dict];trend_label:str;model_metrics:dict;model_version:str
