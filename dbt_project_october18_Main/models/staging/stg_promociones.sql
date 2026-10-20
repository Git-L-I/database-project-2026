select
    id_promocion,
    nombre_campana,
    cast(costo_campana as numeric(10, 2)) as costo_campana,
    cast(retorno_esperado as numeric(10, 2)) as retorno_esperado,
    cast(descuento_pct as numeric(4, 2)) as descuento_pct,
    cast(fecha_inicio as date) as fecha_inicio,
    cast(fecha_fin as date) as fecha_fin
from {{ source('raw', 'promociones') }}