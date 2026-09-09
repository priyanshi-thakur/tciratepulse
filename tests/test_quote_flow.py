from fastapi import HTTPException
from backend.schemas import QuoteRequest
from backend.features import FEATURES,build,factor_summary
from backend.services import coords,weather

def request(**extra):
    return QuoteRequest(origin='Mumbai',destination='Pune',weight_kg=800,**extra)

def test_optional_inputs_and_expanded_vector():
    f=build(request(vehicle_type='Pickup',product_category='High-value',security_level='High',insurance_option='Full',shipment_value_inr=200000),{'distance_km':150,'travel_hours':4},{'risk':'Low','source':'fallback-estimated'})
    assert set(FEATURES)==set(f) and len(FEATURES)==21 and f['insurance_factor']==3

def test_missing_optional_inputs_are_neutral():
    f=build(request(),{'distance_km':150,'travel_hours':4},{'risk':'Low','source':'fallback-estimated'})
    assert f['fuel_index']==1 and f['insurance_factor']==0

def test_factor_provenance_and_weather_fallback(monkeypatch):
    monkeypatch.setattr('backend.services.httpx.get',lambda *a,**k: (_ for _ in ()).throw(RuntimeError('offline')))
    w=weather(19.076,72.877)
    assert w['source']=='fallback-estimated' and w['temperature_c'] is None
    f=build(request(),{'distance_km':150,'travel_hours':4},{'risk':'Low','source':'fallback-estimated'})
    assert len(factor_summary(f,{'source':'OSRM'},w))==16

def test_invalid_location_is_rejected(monkeypatch):
    monkeypatch.setattr('backend.services.get_cache',lambda _:None)
    monkeypatch.setattr('backend.services.httpx.get',lambda *a,**k: type('R',(),{'json':lambda s: []})())
    try: coords('not-a-real-place-zz')
    except HTTPException as exc: assert exc.status_code==422
    else: raise AssertionError('invalid location was accepted')
