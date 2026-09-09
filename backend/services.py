import hashlib, math, httpx
from datetime import date
from fastapi import HTTPException
from .db import get_cache, set_cache

CITY = {"mumbai":(19.076,72.877),"pune":(18.520,73.856),"delhi":(28.614,77.209),"bengaluru":(12.972,77.594),"bangalore":(12.972,77.594),"chennai":(13.083,80.271),"hyderabad":(17.385,78.487),"kolkata":(22.572,88.364),"ahmedabad":(23.023,72.572),"surat":(21.170,72.831),"jaipur":(26.912,75.787),"nagpur":(21.146,79.089)}
def key(prefix, *parts): return prefix+":"+hashlib.sha256("|".join(map(str,parts)).encode()).hexdigest()
def coords(place):
    normalized=place.lower().strip()
    if normalized in CITY: return CITY[normalized], "local-city"
    k=key("geo",normalized); cached=get_cache(k)
    if cached: return tuple(cached), "cache"
    try:
        data=httpx.get("https://nominatim.openstreetmap.org/search",params={"q":place+", India","format":"json","limit":1},headers={"User-Agent":"TCI-RatePulse-MVP/1.0"},timeout=4).json()
        if data:
            val=(float(data[0]["lat"]),float(data[0]["lon"]));set_cache(k,val,604800);return val,"nominatim"
    except Exception: pass
    raise HTTPException(status_code=422, detail=f"Could not resolve Indian location: {place}. Please enter a city or a more specific place.")
def route(origin,destination):
    a,sa=coords(origin);b,sb=coords(destination); k=key("route",a,b); cached=get_cache(k)
    if cached:return cached
    try:
        u=f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}"
        r=httpx.get(u,params={"overview":"false"},timeout=6).json()["routes"][0]
        val={"distance_km":round(r["distance"]/1000,1),"travel_hours":round(r["duration"]/3600,1),"source":"OSRM"}
    except Exception:
        # Haversine x road detour factor: deterministic usable degradation
        d=6371*2*math.asin(math.sqrt(math.sin(math.radians(b[0]-a[0])/2)**2+math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(math.radians(b[1]-a[1])/2)**2))
        val={"distance_km":round(max(15,d*1.23),1),"travel_hours":round(max(.5,d*1.23/42),1),"source":"haversine-fallback"}
    set_cache(k,val);return val
def weather(lat,lon):
    k=key("weather",round(lat,2),round(lon,2),date.today()); cached=get_cache(k)
    if cached:return cached
    try:
        d=httpx.get("https://api.open-meteo.com/v1/forecast",params={"latitude":lat,"longitude":lon,"current":"temperature_2m,precipitation,wind_speed_10m,weather_code"},timeout=5).json()["current"]
        risk="High" if d["precipitation"]>4 or d["wind_speed_10m"]>45 else "Moderate" if d["precipitation"]>0.5 or d["wind_speed_10m"]>25 else "Low"
        val={"temperature_c":d["temperature_2m"],"precipitation_mm":d["precipitation"],"wind_kph":d["wind_speed_10m"],"risk":risk,"source":"Open-Meteo"}
    except Exception: val={"temperature_c":None,"precipitation_mm":None,"wind_kph":None,"risk":"Low","source":"fallback-estimated","note":"Live Open-Meteo was unavailable; neutral weather-risk fallback applied."}
    set_cache(k,val,3600);return val
