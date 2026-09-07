# TCI-RatePulse

Demo-ready, local MVP for dynamic Indian PTL/LTL tariff prediction. It combines routing, weather, engineered operating conditions, a trained XGBoost regressor, SHAP local explanations, SQLite caching, and a React dashboard.

## Important data note

There is **no TCI proprietary historical data** in this project. `backend/train.py` deterministically generates a labelled Indian PTL benchmark dataset from disclosed tariff assumptions, saves it to `data/benchmark_freight.csv`, and trains/evaluates the model. It is intentionally a reproducible demo baseline, not a claim about TCI rates or business performance. Replace the generator with a governed historical-data adapter later; the API/UI feature contract stays unchanged.

## What works

- `POST /quote`: validates a shipment and makes a real XGBoost inference
- Chronological 80/20 evaluation (MAE, RMSE, R² computed at training time, never hard-coded)
- SHAP TreeExplainer contributions for the individual quote
- OpenStreetMap Nominatim + OSRM route distance/time and Open-Meteo current weather
- SQLite response caching; city lookup / Haversine and conservative weather fallbacks when services fail
- Factors: seasonality/demand, fuel and toll proxies, capacity/utilization, labour, customer tier, regulation/geopolitical indices, transit, product/security and weather risks
- Rules after prediction for weather, capacity, urgent SLA, and sensitive cargo

## Run on Windows

Requires Python 3.10+ and Node 20+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m backend.train
uvicorn backend.main:app --reload
```

In another PowerShell window:

```powershell
npm install
npm run dev
```

Open the URL Vite prints (normally `http://localhost:5173`). Try Mumbai → Pune, 800 kg, Pickup, FMCG.

## Tests and checks

```powershell
pytest -q
npm run build
```

## Production integration boundaries

`backend/features.py` is the stable feature boundary. A future TCI data importer should source governed historic bookings/rates, apply data-quality checks and retrain `backend/train.py`. Live fuel, toll, compliance and disruption feeds should replace the transparent benchmark proxies. Dashboard alerts are intentionally local only; WhatsApp/SMS needs approved provider credentials and an opt-in workflow.
