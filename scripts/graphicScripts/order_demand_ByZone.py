import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]
plt.rcParams["mathtext.fontset"] = "stix"

os.makedirs("Output", exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")

def get_engine():
    config = configparser.ConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ini_path = os.path.join(base_dir, "../../config/database.ini")
    config.read(ini_path)
    db = config["postgresql"]
    return create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")

def generate_order_demand_by_zone():
    engine = get_engine()
    print("running.")
    
    query = """
    SELECT 
        z.nombre_zona AS zone_name,
        COUNT(o.id_orden) AS total_orders
    FROM "analyticsMain_marts"."fct_ordenes" o
    JOIN "analyticsMain_marts"."dim_zonas" z ON o.id_zona = z.id_zona
    GROUP BY z.nombre_zona
    ORDER BY total_orders DESC;
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(10, 6))
    
    ax = sns.barplot(
        data=df, 
        x="total_orders", 
        y="zone_name", 
        order=df["zone_name"],
        color="#2b5c8f"
    )
    
    plt.title("Demanda de ordenes por Zona", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Total de ordenes", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Zona", fontsize=10, fontname="Times New Roman")
    
    plt.xticks(fontweight="bold", fontsize=9)
    plt.yticks(fontweight="bold", fontsize=9)
    plt.tight_layout()
    
    output_path = os.path.join("Output", "order_demand_by_zone.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_order_demand_by_zone()