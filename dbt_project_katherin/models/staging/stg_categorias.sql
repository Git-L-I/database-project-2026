select
    id_categoria,
    nombre_categoria,
    cast(margen_contribucion_pct as numeric(4, 2)) as margen_contribucion_pct
from {{ source('raw', 'categorias_platillo') }}