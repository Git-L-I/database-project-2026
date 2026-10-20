with platillos as (
    select * from {{ ref('stg_platillos') }}
),
categorias as (
    select * from {{ ref('stg_categorias') }}
)

select
    p.id_platillo,
    p.nombre_platillo,
    p.id_categoria,
    c.nombre_categoria,
    p.precio_unitario,
    p.costo_ingredientes,
    (p.precio_unitario - p.costo_ingredientes) as margen_bruto_unitario,
    c.margen_contribucion_pct,
    p.tiempo_preparacion_minutos,
    p.requiere_horno,
    p.activo
from platillos p
left join categorias c on p.id_categoria = c.id_categoria