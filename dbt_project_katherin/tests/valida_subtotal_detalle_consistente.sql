
-- El subtotal de cada detalle debe coincidir con cantidad * precio unitario

with detalles as (
    select
        (detalle->>'id_detalle')::integer as id_detalle,
        (detalle->>'id_orden')::integer as id_orden,
        (detalle->>'cantidad')::numeric as cantidad,
        (detalle->>'precio_unitario_item')::numeric as precio_unitario_item,
        (detalle->>'subtotal_item')::numeric as subtotal_item
    from {{ ref('fct_ordenes') }} as orden,
         jsonb_array_elements(orden.detalles_orden) as detalle
)

select
    id_detalle,
    id_orden,
    cantidad,
    precio_unitario_item,
    subtotal_item,
    abs(subtotal_item - (cantidad * precio_unitario_item)) as diferencia
from detalles
where abs(subtotal_item - (cantidad * precio_unitario_item)) > 0.05
