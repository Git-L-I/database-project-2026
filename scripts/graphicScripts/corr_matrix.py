import os
import configparser
import pandas as pd
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

def generate_correlation_matrix():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        tiempo_entrega_minutos,
        cantidad,
        precio_unitario_item,
        subtotal_item,
        costo_total_ingredientes,
        ganancia_bruta_item,
        total_orden,
        costo_envio,
        propina,
        precipitacion_mm,
        temperatura_c
    from "analyticsMain_marts"."fct_ordenes";
    """
    
    df = pd.read_sql(query, engine)
    corr = df.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, annot_kws={"size": 8})
    plt.title("Correlation Matrix - Antojitos Express")
    plt.tight_layout()
    
    output_path = os.path.join("Output", "correlation_matrix.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_correlation_matrix()