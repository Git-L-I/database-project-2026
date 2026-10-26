import os
import configparser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from scipy import stats
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

def generate_htm_delivery_times():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        tiempo_entrega_minutos,
        case 
            when extract(hour from fecha_hora_creacion) between 12 and 14 
              or extract(hour from fecha_hora_creacion) between 19 and 21 
            then 'Hora de Mayor Demanda' 
            else 'Fuera de Pico' 
        end as tipo_horario
    from "analyticsMain_marts"."fct_ordenes"
    where tiempo_entrega_minutos is not null
      and estado_orden = 'entregada';
    """
    
    df = pd.read_sql(query, engine)
    
    peak = df[df["tipo_horario"] == "Hora de Mayor Demanda"]["tiempo_entrega_minutos"]
    off_peak = df[df["tipo_horario"] == "Fuera de Pico"]["tiempo_entrega_minutos"]
    t_stat, p_val = stats.ttest_ind(peak, off_peak, equal_var=False)
    
    plt.figure(figsize=(9, 6))
    sns.kdeplot(
        data=df, 
        x="tiempo_entrega_minutos", 
        hue="tipo_horario", 
        common_norm=False, 
        fill=True, 
        alpha=0.4, 
        palette={"Hora de Mayor Demanda": "red", "Fuera de Pico": "blue"}
    )
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', alpha=0.4, label='Fuera de Pico'),
        Patch(facecolor='red', alpha=0.4, label='Hora de Mayor Demanda')
    ]
    plt.legend(handles=legend_elements, title="Tipo de Horario", prop={"family": "Times New Roman", "size": 10}, title_fontsize=10)
    
    plt.title(f"Prueba de Hipótesis para la Media: Tiempos de Entrega ($p = {p_val:.3f}$)", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Tiempo de Entrega (minutos)", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Densidad", fontsize=10, fontname="Times New Roman")
    plt.tight_layout()

    output_path = os.path.join("Output", "htm_deliveryTimes.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")
if __name__ == "__main__":
    generate_htm_delivery_times()