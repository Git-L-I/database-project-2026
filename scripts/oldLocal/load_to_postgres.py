import configparser
import requests
import pandas as pd
from sqlalchemy import create_engine, text

BASE_URL = "http://20.228.134.116:8000"

def get_db_engine():
    config = configparser.ConfigParser()
    config.read("config/database.ini")
    db = config["postgresql"]
    connection_url = f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
    return create_engine(connection_url)

def fetch_all_paginated(endpoint, limit=100):
    all_records = []
    offset = 0
    
    while True:
        url = f"{BASE_URL}{endpoint}?limit={limit}&offset={offset}"
        response = requests.get(url, timeout=30)
        
        if response.status_code != 200:
            print(f"  [HTTP {response.status_code}] Failed URL: {url}")
            print(f"  Response Body: {response.text}")
            break
            
        data = response.json()
        
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = data.get("items", data.get("results", data.get("data", [])))
        else:
            records = []
        
        if not records:
            break
            
        all_records.extend(records)
        offset += len(records)
        
        if len(records) < limit:
            break
            
    print(f"  Total records fetched: {len(all_records)}")
    return pd.DataFrame(all_records)

def run_pipeline():
    engine = get_db_engine()
    
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()
    print("Schema 'raw' verified in PostgreSQL.\n")

    endpoints = {
        "/antojitos/zonas": "raw_zonas",
        "/antojitos/repartidores": "raw_repartidores",
        "/antojitos/categorias": "raw_categorias",
        "/antojitos/platillos": "raw_platillos",
        "/antojitos/promociones": "raw_promociones",
        "/antojitos/clima": "raw_clima",
        "/antojitos/ordenes": "raw_ordenes",
        "/antojitos/detalles": "raw_detalles"
    }

    for endpoint, table_name in endpoints.items():
        print(f"Extracting {endpoint} -> raw.{table_name}")
        df = fetch_all_paginated(endpoint, limit=100)
        
        if not df.empty:
            df.to_sql(
                name=table_name,
                con=engine,
                schema="raw",
                if_exists="replace",
                index=False
            )
            print(f"loaded {len(df)}rows into raw .{table_name}\n")
        else:
            print(f"no data for raw.{table_name}\n")

if __name__ == "__main__":
    run_pipeline()