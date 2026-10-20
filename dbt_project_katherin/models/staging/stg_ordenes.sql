select
    id_orden,
    id_zona,
    id_repartidor,
    id_promocion,
    cast(fecha_hora_creacion as timestamp) as fecha_hora_creacion,
    cast(fecha_hora_entrega as timestamp) as fecha_hora_entrega,
    metodo_pago,
    estado_orden,
    cast(total_orden as numeric(10, 2)) as total_orden,
    cast(costo_envio as numeric(8, 2)) as costo_envio,
    cast(propina as numeric(8, 2)) as propina,
    notas_entrega,
    comentario_cliente,
    motivo_cancelacion,
    cast(fecha_hora_creacion as date) as fecha_orden
from {{ source('raw', 'ordenes') }}