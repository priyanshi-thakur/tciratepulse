import json, numpy as np, pandas as pd, shap
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from xgboost import XGBRegressor
from .schemas import QuoteRequest,QuoteResponse
from .config import MODEL_PATH,META_PATH
from .db import init_db,save_quote
from .services import route,coords,weather
from .features import build,FEATURES
from .rules import alerts
from .train import train

app=FastAPI(title='TCI-RatePulse API',version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)
model=None; explainer=None; metrics={}
# Create local cache schema at import time too, so in-process consumers are safe;
# startup still loads the model before serving requests.
init_db()
@app.on_event('startup')
def startup():
 global model,explainer,metrics
 init_db()
 if not MODEL_PATH.exists(): train()
 model=XGBRegressor();model.load_model(MODEL_PATH); metrics=json.loads(META_PATH.read_text());explainer=shap.TreeExplainer(model)
@app.get('/health')
def health(): return {'status':'ok','model_ready':model is not None,'metrics':metrics}
@app.get('/metadata')
def metadata(): return {'metrics':metrics,'dataset_note':'This MVP trains on a reproducible synthetic benchmark, not TCI proprietary data.'}
@app.post('/quote',response_model=QuoteResponse)
def quote(req:QuoteRequest):
 r=route(req.origin,req.destination);c,_=coords(req.destination);w=weather(*c);f=build(req,r,w); frame=pd.DataFrame([f])[FEATURES]
 p=float(model.predict(frame)[0]); sv=explainer.shap_values(frame)[0]; top=sorted(zip(FEATURES,sv),key=lambda x:abs(x[1]),reverse=True)[:5]
 labels={'distance_km':'Route distance','weight_kg':'Shipment weight','sla_factor':'SLA','toll_inr':'Tolls','seasonal_factor':'Seasonality','weather_risk':'Weather risk','utilization':'Capacity utilization','product_risk':'Product risk'}
 drivers=[{'feature':labels.get(x,x.replace('_',' ').title()),'impact_inr':round(float(v),0),'direction':'up' if v>=0 else 'down'} for x,v in top]
 uncertainty=.09+.025*f['weather_risk']+.02*(1 if req.sla=='Critical' else 0); low=round(p*(1-uncertainty)/10)*10;high=round(p*(1+uncertainty)/10)*10
 trend=[{'month':m,'tariff_inr':round(p*(.94+.012*i))} for i,m in enumerate(['Apr','May','Jun','Jul','Aug','Sep'])]
 out={'tariff_inr':round(p/10)*10,'low_inr':low,'high_inr':high,'confidence':'Medium' if uncertainty>.12 else 'High','distance_km':r['distance_km'],'travel_hours':r['travel_hours'],'route_source':r['source'],'weather':w,'drivers':drivers,'alerts':alerts(req,f,w),'factors':f,'trend':trend,'model_metrics':metrics};save_quote(req.model_dump(),out);return out
