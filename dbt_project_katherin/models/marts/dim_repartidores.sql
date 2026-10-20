select
    id_repartidor,
    nombre,
    tipo_vehiculo,
    calificacion_promedio,
    capacidad_maxima_ordenes,
    estado
from {{ ref('stg_repartidores') }}