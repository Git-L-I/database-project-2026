-- El subtotal de la línea de detalle debe coincidir con cantidad * precio unitario
select
    id_detalle,
    id_orden,
    cantidad,
    precio_unitario_item,
    subtotal_item,
    abs(subtotal_item - (cantidad * precio_unitario_item)) as diferencia
from {{ ref('fct_detalles_orden') }}
where abs(subtotal_item - (cantidad * precio_unitario_item)) > 0.05
