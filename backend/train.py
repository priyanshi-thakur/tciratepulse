"""Reproducible synthetic benchmark generator, not TCI historical data."""
import json
from pathlib import Path
import numpy as np, pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .config import MODEL_PATH, META_PATH, DATA_DIR
from .features import FEATURES

def generate(n=5000, seed=42):
    rng=np.random.default_rng(seed); dates=pd.date_range('2023-01-01','2025-12-31',periods=n)
    distance=rng.uniform(25,1800,n); capacity=rng.choice([750,1500,3500,7000,16000],n); utilization=rng.uniform(.1,1,n)
    d=pd.DataFrame({"date":dates,"distance_km":distance,"weight_kg":capacity*utilization,"capacity_kg":capacity,"utilization":utilization,"vehicle_code":rng.integers(0,5,n),"product_risk":rng.uniform(1,1.22,n),"sla_factor":rng.choice([1,1.14,1.28],n),"loyalty_factor":rng.choice([1,.97,.92],n),"seasonal_factor":1+rng.normal(.04,.08,n),"fuel_index":rng.normal(1,.08,n),"toll_inr":distance*rng.normal(.75,.08,n),"labour_index":rng.normal(1,.06,n),"demand_index":rng.normal(1.04,.09,n),"weather_risk":rng.integers(0,3,n),"security_risk":rng.integers(0,2,n),"regulatory_index":rng.normal(1,.03,n),"geopolitical_index":rng.normal(1,.025,n),"transit_hours":distance/rng.normal(42,4,n)})
    # Transparent synthetic tariff mechanism plus noise: a benchmark only.
    d['tariff_inr']=(850+d.distance_km*8.5+d.weight_kg*.72+d.toll_inr+d.transit_hours*95+d.weather_risk*280+d.security_risk*220)*d.product_risk*d.sla_factor*d.seasonal_factor*d.fuel_index*d.labour_index*d.demand_index*d.loyalty_factor+rng.normal(0,260,n)
    return d
def train():
    d=generate(); cut=int(len(d)*.8); train,test=d.iloc[:cut],d.iloc[cut:]
    model=XGBRegressor(n_estimators=350,max_depth=5,learning_rate=.045,subsample=.85,colsample_bytree=.9,objective='reg:squarederror',random_state=42,n_jobs=2)
    model.fit(train[FEATURES],train.tariff_inr); pred=model.predict(test[FEATURES])
    metrics={"mae_inr":round(mean_absolute_error(test.tariff_inr,pred),2),"rmse_inr":round(mean_squared_error(test.tariff_inr,pred)**.5,2),"r2":round(r2_score(test.tariff_inr,pred),4),"split":"chronological 80/20 (2023–2025)","dataset":"Reproducible synthetic Indian PTL benchmark; not proprietary TCI data"}
    model.save_model(MODEL_PATH); META_PATH.write_text(json.dumps(metrics,indent=2)); d.to_csv(DATA_DIR/'benchmark_freight.csv',index=False); return metrics
if __name__=='__main__': print(train())
