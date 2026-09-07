from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
DB_PATH = DATA_DIR / "ratepulse.db"
MODEL_PATH = MODEL_DIR / "xgb_tariff.json"
META_PATH = MODEL_DIR / "model_metadata.json"
for folder in (DATA_DIR, MODEL_DIR):
    folder.mkdir(exist_ok=True)
