select
    id_detalle,
    id_orden,
    id_platillo,
    cast(cantidad as integer) as cantidad,
    cast(precio_unitario as numeric(8, 2)) as precio_unitario,
    cast(subtotal as numeric(10, 2)) as subtotal
from {{ source('raw', 'detalle_ordenes') }}
