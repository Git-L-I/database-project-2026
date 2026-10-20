select
    id_repartidor,
    nombre,
    tipo_vehiculo,
    cast(calificacion_promedio as numeric(3, 2)) as calificacion_promedio,
    cast(capacidad_maxima_ordenes as integer) as capacidad_maxima_ordenes,
    estado
from {{ source('raw', 'repartidores') }}