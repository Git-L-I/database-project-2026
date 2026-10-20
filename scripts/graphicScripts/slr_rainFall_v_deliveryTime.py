import os
import configparser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

os.makedirs("Output", exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")

def get_engine():
    config = configparser.ConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ini_path = os.path.join(base_dir, "../../config/database.ini")
    config.read(ini_path)
    db = config["postgresql"]
    return create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")

def generate_slr_rain_delivery():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        precipitacion_mm,
        tiempo_entrega_minutos
    from analyticsMain_marts.fct_ordenes
    where precipitacion_mm is not null 
      and tiempo_entrega_minutos is not null
      and estado_orden = 'entregada';
    """
    
    df = pd.read_sql(query, engine)
    
    x = df["precipitacion_mm"]
    y = df["tiempo_entrega_minutos"]
    slope, intercept = np.polyfit(x, y, 1)
    
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=df, x="precipitacion_mm", y="tiempo_entrega_minutos", alpha=0.3, color="b", label="Ordenes")
    plt.plot(x, slope * x + intercept, color="red", linewidth=2, label=f"Ajuste: y = {slope:.2f}x + {intercept:.2f}")
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.title("Regresion Linear Simple: Lluvia y Tiempo de Entrega/Delivery", fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Precipitation (en mm)", fontname="Times New Roman")
    plt.ylabel("Tiempo de Delivery/Entrega (minutos)", fontname="Times New Roman")
    plt.legend()
    plt.tight_layout()
    output_path = os.path.join("Output", "slr_rain_v_delivery.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_slr_rain_delivery()