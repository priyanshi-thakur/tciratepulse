from backend.features import build
from backend.schemas import QuoteRequest
def test_feature_build():
 r={'distance_km':150,'travel_hours':4};w={'risk':'Low'}
 x=build(QuoteRequest(origin='Mumbai',destination='Pune',weight_kg=500,vehicle_type='Pickup',product_category='General',sla='Standard'),r,w)
 assert x['distance_km']==150 and x['utilization']>0
