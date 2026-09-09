def alerts(req, factors, weather):
    out=[]
    if factors['utilization']>.95: out.append({"level":"warning","text":"Vehicle is near capacity; availability may constrain pricing."})
    if weather['risk'] in ('Moderate','High'): out.append({"level":"warning","text":f"{weather['risk']} weather risk may affect transit and handling."})
    if req.sla=='Critical':out.append({"level":"info","text":"Critical SLA premium is included in the predicted tariff."})
    if req.product_category in ('Pharma','Electronics'):out.append({"level":"info","text":"Security-sensitive cargo risk is included."})
    if factors['calamity_risk']: out.append({"level":"warning","text":"Severe weather creates a derived natural-calamity risk; verify route operations."})
    if factors['festival_pressure']>1: out.append({"level":"info","text":"Festival-period demand pressure is included using a calendar-derived proxy."})
    if factors['security_risk']>=2: out.append({"level":"warning","text":"High declared security risk requires operational review."})
    if factors['regulatory_index']>1: out.append({"level":"info","text":"Declared regulatory-impact index is included; validate applicable restrictions."})
    if not out:out.append({"level":"success","text":"No unusual operating conditions detected."})
    return out
