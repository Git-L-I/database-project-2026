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

def generate_order_distribution_schedule():
    engine = get_engine()
    print("running.")
    
    query = """
    SELECT 
        EXTRACT(HOUR FROM fecha_hora_creacion) AS order_hour,
        COUNT(*) AS total_orders
    from "analyticsMain_marts"."fct_ordenes"
    GROUP BY order_hour
    ORDER BY order_hour;
    """
    
    df = pd.read_sql(query, engine)
    
    full_hours = pd.DataFrame({"order_hour": range(24)})
    df = pd.merge(full_hours, df, on="order_hour", how="left").fillna({"total_orders": 0})
    df["order_hour"] = df["order_hour"].astype(int)
    
    df["hour_label"] = df["order_hour"].apply(lambda h: f"{h:02d}:00")
    
    plt.figure(figsize=(12, 6))
    
    ax = sns.barplot(
        data=df, 
        x="hour_label", 
        y="total_orders", 
        color="#2b5c8f"
    )
    
    plt.title("Distribucion de ordenes por Horario", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Hora del dia", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Total de ordenes", fontsize=10, fontname="Times New Roman")
    plt.xticks(rotation=45, ha="right", fontweight="bold", fontsize=9)
    plt.yticks(fontweight="bold", fontsize=9)
    plt.tight_layout()
    
    output_path = os.path.join("Output", "order_distribution_schedule.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_order_distribution_schedule()