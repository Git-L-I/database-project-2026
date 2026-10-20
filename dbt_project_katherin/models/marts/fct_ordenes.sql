with ordenes as (
    select *
    from {{ ref('stg_ordenes') }}
),

detalles as (
    select
        d.id_orden,
        count(*) as cantidad_detalles,
        sum(d.cantidad) as cantidad_total_platillos,
        sum(d.subtotal) as subtotal_orden_calculado,
        sum(d.cantidad * p.costo_ingredientes) as costo_total_ingredientes_orden,
        sum(d.subtotal - (d.cantidad * p.costo_ingredientes)) as ganancia_bruta_orden
    from {{ ref('stg_detalles') }} d
    left join {{ ref('stg_platillos') }} p
        on d.id_platillo = p.id_platillo
    group by d.id_orden
),

zonas as (
    select *
    from {{ ref('stg_zonas') }}
),

clima as (
    select *
    from {{ ref('stg_clima') }}
)

select
    o.id_orden,
    o.id_zona,
    o.id_repartidor,
    o.id_promocion,
    o.fecha_hora_creacion,
    o.fecha_hora_entrega,
    o.fecha_orden,

    extract(
        epoch from (
            o.fecha_hora_entrega - o.fecha_hora_creacion
        )
    ) / 60.0 as tiempo_entrega_minutos,

    z.tiempo_base_minutos as tiempo_base_objetivo_minutos,

    (
        (extract(epoch from (o.fecha_hora_entrega - o.fecha_hora_creacion)) / 60.0)
        - z.tiempo_base_minutos
    ) as minutos_retraso,

    case
        when (extract(epoch from (o.fecha_hora_entrega - o.fecha_hora_creacion)) / 60.0) > z.tiempo_base_minutos
        then true
        else false
    end as es_entrega_retrasada,

    case
        when extract(hour from o.fecha_hora_creacion) between 12 and 14
          or extract(hour from o.fecha_hora_creacion) between 19 and 21
        then 'Hora de Mayor Demanda'
        else 'Fuera de Pico'
    end as tipo_horario,

    case
        when extract(hour from o.fecha_hora_creacion) between 12 and 14
          or extract(hour from o.fecha_hora_creacion) between 19 and 21
        then true
        else false
    end as es_hora_pico,

    o.metodo_pago,
    o.estado_orden,
    o.notas_entrega,
    o.comentario_cliente,
    o.motivo_cancelacion,

    coalesce(d.cantidad_detalles, 0) as cantidad_detalles,
    coalesce(d.cantidad_total_platillos, 0) as cantidad_total_platillos,
    -- Alias cantidad para compatibilidad con scripts analiticos existentes
    coalesce(d.cantidad_total_platillos, 0) as cantidad,
    d.subtotal_orden_calculado,

    coalesce(d.costo_total_ingredientes_orden, 0) as costo_total_ingredientes_orden,
    coalesce(d.ganancia_bruta_orden, 0) as ganancia_bruta_orden,

    case
        when coalesce(d.subtotal_orden_calculado, 0) > 0
        then round(((d.ganancia_bruta_orden / d.subtotal_orden_calculado) * 100)::numeric, 2)
        else 0
    end as margen_bruto_orden_pct,

    o.total_orden,
    o.costo_envio,
    o.propina,

    c.precipitacion_mm,
    c.temperatura_c,
    c.condicion_cielo

from ordenes o
left join detalles d
    on o.id_orden = d.id_orden
left join zonas z
    on o.id_zona = z.id_zona
left join clima c
    on o.fecha_orden = c.fecha_clima
