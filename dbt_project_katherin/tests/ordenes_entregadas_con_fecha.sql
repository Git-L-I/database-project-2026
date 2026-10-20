select
    id_orden,
    estado_orden,
    fecha_hora_entrega
from {{ ref('fct_ordenes') }}
where estado_orden = 'entregada'
  and fecha_hora_entrega is null