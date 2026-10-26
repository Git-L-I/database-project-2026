import os
import configparser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

# times new roman!!!!
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

def generate_mlr_prediction():
    engine = get_engine()
    print("running.")
    
    query = """
    select 
        tiempo_entrega_minutos,
        precipitacion_mm,
        costo_envio,
        cantidad
    from "analyticsMain_marts"."fct_ordenes"
    where tiempo_entrega_minutos is not null
      and precipitacion_mm is not null
      and costo_envio is not null
      and cantidad is not null
      and estado_orden = 'entregada';
    """
    
    df = pd.read_sql(query, engine)
    
    X = df[["precipitacion_mm", "costo_envio", "cantidad"]]
    y = df["tiempo_entrega_minutos"]
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    plt.figure(figsize=(9, 6))
    sns.scatterplot(x=y_pred, y=y, alpha=0.3, color="b", label="Ordenes")
    
    min_val = min(y.min(), y_pred.min())
    max_val = max(y.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], color="red", linestyle="--", linewidth=2, label="Linea Ideal (y = x)")
    
    plt.title("Regresion Lineal Multiple: Prediccion de Tiempo de Entrega", fontsize=12, fontname="Times New Roman", fontweight="bold")
    plt.xlabel("Tiempo de Entrega Predicho (minutos)", fontsize=10, fontname="Times New Roman")
    plt.ylabel("Tiempo de Entrega Real (minutos)", fontsize=10, fontname="Times New Roman")
    plt.legend(prop={"family": "Times New Roman", "size": 10})
    plt.tight_layout()
    
    output_path = os.path.join("Output", "mlr_deliveryTimePrediction.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"completed. Saved to {output_path}")

if __name__ == "__main__":
    generate_mlr_prediction()