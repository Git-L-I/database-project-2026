import configparser
import pandas as pd
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read("config/database.ini")
db = config["postgresql"]
engine = create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")

tables = [
    "raw_zonas", "raw_repartidores", "raw_categorias", "raw_platillos",
    "raw_promociones", "raw_clima", "raw_ordenes", "raw_detalles"
]

print("--- raw schema table summary ---")
for t in tables:
    try:
        count = pd.read_sql(f"SELECT COUNT(*) FROM raw.{t}", engine).iloc[0, 0]
        print(f"raw.{t:<18} : {count:,} rows")
    except Exception as e:
        print(f"raw.{t:<18} : Table missing or error ({e})")