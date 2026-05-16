from pathlib import Path
import json
import pandas as pd


def read_csv():
    BASE_DIR = Path(__file__).resolve().parents[2]      
    DATA_PATH = BASE_DIR / "pliki testowe" / "triage_csv.csv" 
    plik_csv = pd.read_csv(DATA_PATH, low_memory=False)
    return plik_csv

def read_json():
    BASE_DIR = Path(__file__).resolve().parents[2]      
    json_path = BASE_DIR / "pliki testowe" / "testing_json.json"      

    with json_path.open("r", encoding="utf-8") as f:
        plik_json = json.load(f)
    return plik_json

def read_microservice_config():
    BASE_DIR = Path(__file__).resolve().parents[2]      
    json_path = BASE_DIR / "src" / "config" / "microservices.json"    

    with json_path.open("r", encoding="utf-8") as f:
        plik_json = json.load(f)
    return plik_json
