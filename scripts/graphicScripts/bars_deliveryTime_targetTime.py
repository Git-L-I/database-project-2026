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

def generate_bars_delivery_target():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        z.nombre_zona,
        z.tiempo_base_minutos,
        round(avg(o.tiempo_entrega_minutos)::numeric, 2) as avg_tiempo_entrega
    from analyticsMain_marts.fct_ordenes o
    join analyticsMain_marts.dim_zonas z on o.id_zona = z.id_zona
    where o.estado_orden = 'entregada'
    group by z.nombre_zona, z.tiempo_base_minutos
    order by avg_tiempo_entrega desc;
    """
    
    df = pd.read_sql(query, engine)
    
    df_melted = df.melt(id_vars="nombre_zona", 
                        value_vars=["tiempo_base_minutos", "avg_tiempo_entrega"],
                        var_name="Tipo", value_name="Minutos")
    
    df_melted["Tipo"] = df_melted["Tipo"].replace({
        "tiempo_base_minutos": "Tiempo Base (Objetivo)",
        "avg_tiempo_entrega": "Tiempo Promedio Real"
    })
    
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_melted, 
        x="nombre_zona", 
        y="Minutos", 
        hue="Tipo", 
        palette={"Tiempo Base (Objetivo)": "skyblue", "Tiempo Promedio Real": "salmon"}
    )
    
    plt.title("Tiempo Promedio de Entrega vs. Tiempo Base por Zona", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Zona", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Minutos", fontsize=10, fontname="Times New Roman")
    plt.xticks(rotation=45, ha="right", fontweight="bold", fontsize=9)
    plt.legend(title="Metrica", prop={"family": "Times New Roman", "size": 10}, title_fontsize=10)
    plt.tight_layout()
    
    output_path = os.path.join("Output", "bars_deliveryTime_targetTime.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_bars_delivery_target()