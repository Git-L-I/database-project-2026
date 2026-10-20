select
    id_promocion,
    nombre_campana,
    costo_campana,
    retorno_esperado,
    descuento_pct,
    fecha_inicio,
    fecha_fin
from {{ ref('stg_promociones') }}