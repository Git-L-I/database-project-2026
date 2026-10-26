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

def generate_most_popular_orders():
    engine = get_engine()
    print("running.")
    
    query = """
    SELECT 
        p.nombre_platillo AS item_name,
        SUM(o.cantidad) AS total_quantity
    FROM "analyticsMain_marts"."fct_ordenes" o
    JOIN "analyticsMain_marts"."dim_platillos" p ON o.id_platillo = p.id_platillo
    GROUP BY p.nombre_platillo
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    
    df = pd.read_sql(query, engine)
    
    plt.figure(figsize=(10, 6))
    
    ax = sns.barplot(
        data=df, 
        x="total_quantity", 
        y="item_name", 
        order=df["item_name"],
        color="#2b5c8f"
    )
    
    plt.title("Platillos mas Populares (Top 10)", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Cantidad Total Vendida", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Platillo", fontsize=10, fontname="Times New Roman")
    
    plt.xticks(fontweight="bold", fontsize=9)
    plt.yticks(fontweight="bold", fontsize=9)
    plt.tight_layout()
    
    output_path = os.path.join("Output", "most_popular_orders.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_most_popular_orders()