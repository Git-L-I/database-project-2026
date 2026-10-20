select
    id_zona,
    nombre_zona,
    cast(latitud as numeric(9, 6)) as latitud,
    cast(longitud as numeric(9, 6)) as longitud,
    cast(distancia_km as numeric(5, 2)) as distancia_km,
    cast(tiempo_base_minutos as integer) as tiempo_base_minutos,
    cast(tarifa_envio_base as numeric(8, 2)) as tarifa_envio_base
from {{ source('raw', 'zonas') }}