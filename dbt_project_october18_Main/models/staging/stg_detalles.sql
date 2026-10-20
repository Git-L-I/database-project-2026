select
    id_detalle,
    id_orden,
    id_platillo,
    cantidad::integer as cantidad,
    precio_unitario::numeric(8, 2) as precio_unitario,
    subtotal::numeric(10, 2) as subtotal
from {{ source('raw', 'detalle_ordenes') }}