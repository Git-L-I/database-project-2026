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

def generate_lp_allocation():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        z.nombre_zona,
        count(o.id_orden) as total_ordenes
    from analyticsMain_marts.fct_ordenes o
    join analyticsMain_marts.dim_zonas z on o.id_zona = z.id_zona
    group by z.nombre_zona
    order by total_ordenes desc;
    """
    
    df = pd.read_sql(query, engine)
    
    # simulacion de programacion lineal > asignacion de recursos de 25 repartidores
    total_couriers = 25
    total_demand = df["total_ordenes"].sum()
    df["asignacion_optima_repartidores"] = (df["total_ordenes"] / total_demand) * total_couriers
    df["asignacion_optima_repartidores"] = df["asignacion_optima_repartidores"].round(1)
    
    fig, ax1 = plt.subplots(figsize=(11, 6))
    
    color = "tab:blue"
    ax1.set_xlabel("Zona", fontname="Times New Roman", fontsize=10)
    ax1.set_ylabel("Demanda (Total de Ordenes)", color=color, fontweight="bold", fontsize=10)
    ax1.bar(df["nombre_zona"], df["total_ordenes"], color=color, alpha=0.5, label="Demanda de Ordenes")
    ax1.tick_params(axis="y", labelcolor=color)
    plt.xticks(rotation=45, ha="right", fontweight="bold", fontsize=9)
    
    ax2 = ax1.twinx()  
    color = "tab:red"
    ax2.set_ylabel("Repartidores Optimos Asignados (Modelo)", color=color, fontweight="bold", fontsize=10)
    ax2.plot(df["nombre_zona"], df["asignacion_optima_repartidores"], color=color, marker="o", linewidth=2, label="Asignacion optima")
    ax2.tick_params(axis="y", labelcolor=color)
    ax2.grid(False)
    
    plt.title("Programacion Lineal: Asignacion Optima de Repartidores vs. Demanda por Zona", fontsize=12, fontname="Times New Roman", fontweight="bold")
    fig.tight_layout()
    
    output_path = os.path.join("Output", "lp_zoneDemand_deliveryGuy.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_lp_allocation()