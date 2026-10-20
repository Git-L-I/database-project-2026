with detalles as (
    select *
    from {{ ref('stg_detalles') }}
),

ordenes as (
    select *
    from {{ ref('stg_ordenes') }}
),

platillos as (
    select *
    from {{ ref('stg_platillos') }}
),

clima as (
    select *
    from {{ ref('stg_clima') }}
)

select
    d.id_detalle,
    d.id_orden,
    o.id_zona,
    o.id_repartidor,
    o.id_promocion,
    d.id_platillo,
    p.nombre_platillo,

    o.fecha_hora_creacion,
    o.fecha_hora_entrega,
    o.fecha_orden,

    extract(
        epoch from (
            o.fecha_hora_entrega - o.fecha_hora_creacion
        )
    ) / 60.0 as tiempo_entrega_minutos,

    o.metodo_pago,
    o.estado_orden,
    o.notas_entrega,
    o.comentario_cliente,
    o.motivo_cancelacion,

    d.cantidad,
    d.precio_unitario as precio_unitario_item,
    d.subtotal as subtotal_item,

    p.costo_ingredientes,

    (
        d.cantidad * p.costo_ingredientes
    ) as costo_total_ingredientes,

    (
        d.subtotal - (d.cantidad * p.costo_ingredientes)
    ) as ganancia_bruta_item,

    case
        when d.subtotal > 0
        then round((((d.subtotal - (d.cantidad * p.costo_ingredientes)) / d.subtotal) * 100)::numeric, 2)
        else 0
    end as margen_bruto_item_pct,

    o.total_orden,
    o.costo_envio,
    o.propina,

    c.precipitacion_mm,
    c.temperatura_c,
    c.condicion_cielo

from detalles d
inner join ordenes o
    on d.id_orden = o.id_orden
left join platillos p
    on d.id_platillo = p.id_platillo
left join clima c
    on o.fecha_orden = c.fecha_clima
