import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

os.makedirs("reports/figures", exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")

def get_engine():
    config = configparser.ConfigParser()
    config.read("config/database.ini")
    db = config["postgresql"]
    return create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")

def run_eda():
    engine = get_engine()
    print("running.")

    q_zones = """
    select 
        z.nombre_zona,
        z.tiempo_base_minutos,
        count(distinct o.id_orden) as total_ordenes,
        round(avg(o.tiempo_entrega_minutos)::numeric, 2) as avg_tiempo_entrega
    from analytics_marts.fct_ordenes o
    join analytics_marts.dim_zonas z on o.id_zona = z.id_zona
    where o.estado_orden = 'entregada'
    group by z.nombre_zona, z.tiempo_base_minutos
    order by avg_tiempo_entrega desc;
    """
    df_zones = pd.read_sql(q_zones, engine)
    print("\n--- delivery by zone ---")
    print(df_zones.to_string(index=False))

    q_canc = """
    select 
        coalesce(motivo_cancelacion, 'completada / sin motivo') as motivo,
        count(distinct id_orden) as total_ordenes
    from analytics_marts.fct_ordenes
    group by motivo_cancelacion
    order by total_ordenes desc;
    """
    df_canc = pd.read_sql(q_canc, engine)
    print("\n--- cancellations ---")
    print(df_canc.to_string(index=False))

    q_dishes = """
    select 
        d.nombre_platillo,
        sum(o.cantidad) as unidades_vendidas,
        round(sum(o.ganancia_bruta_item)::numeric, 2) as ganancia_total
    from analytics_marts.fct_ordenes o
    join analytics_marts.dim_platillos d on o.id_platillo = d.id_platillo
    group by d.nombre_platillo
    order by ganancia_total desc
    limit 10;
    """
    df_dishes = pd.read_sql(q_dishes, engine)
    print("\n--- top dishes ---")
    print(df_dishes.to_string(index=False))

    print("completed.")

if __name__ == "__main__":
    run_eda()