import configparser
import pandas as pd
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read("config/database.ini")
db = config["postgresql"]
engine = create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")

marts_tables = [
    "dim_zonas", "dim_repartidores", "dim_promociones", 
    "dim_platillos", "fct_ordenes", "fct_order_items"
]

print("--- analytics marts summary -")
for t in marts_tables:
    count = pd.read_sql(f"SELECT COUNT(*) FROM analytics_marts.{t}", engine).iloc[0, 0]
    print(f"analytics_marts.{t:<18} : {count:,} rows")