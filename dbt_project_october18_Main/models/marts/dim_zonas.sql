select
    id_zona,
    nombre_zona,
    latitud,
    longitud,
    distancia_km,
    tiempo_base_minutos,
    tarifa_envio_base
from {{ ref('stg_zonas') }}