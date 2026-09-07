import math
VEHICLE={"Tata Ace":750,"Pickup":1500,"14ft Truck":3500,"19ft Truck":7000,"32ft MXL":16000}
PRODUCT={"General":1,"FMCG":1.05,"Electronics":1.12,"Pharma":1.18,"Perishable":1.22,"Industrial":1.08}
SLA={"Standard":1,"Express":1.14,"Critical":1.28}; LOYALTY={"New":1,"Regular":.97,"Strategic":.92}
FEATURES=["distance_km","weight_kg","capacity_kg","utilization","vehicle_code","product_risk","sla_factor","loyalty_factor","seasonal_factor","fuel_index","toll_inr","labour_index","demand_index","weather_risk","security_risk","regulatory_index","geopolitical_index","transit_hours"]
def build(req,r,w):
    month=__import__('datetime').date.today().month; seasonal=1.12 if month in (9,10,11,12) else 1.06 if month in (6,7,8) else .98
    cap=VEHICLE[req.vehicle_type]; util=min(req.weight_kg/cap,1.5); risk={"Low":0,"Moderate":1,"High":2}[w['risk']]
    return {"distance_km":r['distance_km'],"weight_kg":req.weight_kg,"capacity_kg":cap,"utilization":util,"vehicle_code":list(VEHICLE).index(req.vehicle_type),"product_risk":PRODUCT[req.product_category],"sla_factor":SLA[req.sla],"loyalty_factor":LOYALTY[req.customer_loyalty],"seasonal_factor":seasonal,"fuel_index":1.0,"toll_inr":r['distance_km']*.75,"labour_index":1.0,"demand_index":seasonal,"weather_risk":risk,"security_risk":1 if req.product_category in ('Electronics','Pharma') else 0,"regulatory_index":1.0,"geopolitical_index":1.0,"transit_hours":r['travel_hours']}
