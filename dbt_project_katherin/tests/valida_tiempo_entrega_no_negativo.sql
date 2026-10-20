-- Las órdenes entregadas no deben tener tiempo de entrega negativo
select
    id_orden,
    tiempo_entrega_minutos
from {{ ref('fct_ordenes') }}
where estado_orden = 'entregada'
  and tiempo_entrega_minutos < 0
