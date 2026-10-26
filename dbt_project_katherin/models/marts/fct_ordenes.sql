
with ordenes as (
    select *
    from {{ ref('stg_ordenes') }}
),

detalles as (
    select
        d.id_orden,

        -- Resumen de los detalles de cada orden
        count(*) as cantidad_detalles,
        sum(d.cantidad) as cantidad_total_platillos,
        sum(d.subtotal) as subtotal_orden_calculado,

        sum(
            d.cantidad * coalesce(p.costo_ingredientes, 0)
        ) as costo_total_ingredientes_orden,

        sum(
            d.subtotal
            - (d.cantidad * coalesce(p.costo_ingredientes, 0))
        ) as ganancia_bruta_orden,

        -- Información individual de cada platillo
        jsonb_agg(
            jsonb_build_object(
                'id_detalle', d.id_detalle,
                'id_orden', d.id_orden,
                'id_platillo', d.id_platillo,
                'nombre_platillo', p.nombre_platillo,

                'cantidad', d.cantidad,
                'precio_unitario_item', d.precio_unitario,
                'subtotal_item', d.subtotal,

                'costo_ingredientes',
                    coalesce(p.costo_ingredientes, 0),

                'costo_total_ingredientes',
                    d.cantidad
                    * coalesce(p.costo_ingredientes, 0),

                'ganancia_bruta_item',
                    d.subtotal
                    - (
                        d.cantidad
                        * coalesce(p.costo_ingredientes, 0)
                    ),

                'margen_bruto_item_pct',
                    case
                        when d.subtotal > 0 then
                            round(
                                (
                                    (
                                        d.subtotal
                                        - (
                                            d.cantidad
                                            * coalesce(p.costo_ingredientes, 0)
                                        )
                                    ) / d.subtotal * 100
                                )::numeric,
                                2
                            )
                        else 0
                    end
            )
            order by d.id_detalle
        ) as detalles_orden

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
    -- Identificación de la orden
    o.id_orden,
    o.id_zona,
    o.id_repartidor,
    o.id_promocion,

    -- Fechas de la orden
    o.fecha_hora_creacion,
    o.fecha_hora_entrega,
    o.fecha_orden,

    -- Tiempo de entrega en minutos
    extract(
        epoch from (
            o.fecha_hora_entrega - o.fecha_hora_creacion
        )
    ) / 60.0 as tiempo_entrega_minutos,

    -- Tiempo objetivo de entrega según la zona
    z.tiempo_base_minutos as tiempo_base_objetivo_minutos,

    -- Diferencia entre el tiempo real y el tiempo objetivo
    (
        extract(
            epoch from (
                o.fecha_hora_entrega - o.fecha_hora_creacion
            )
        ) / 60.0
        - z.tiempo_base_minutos
    ) as minutos_retraso,

    -- Indicador de entrega retrasada
    case
        when o.fecha_hora_entrega is not null
         and z.tiempo_base_minutos is not null
         and (
            extract(
                epoch from (
                    o.fecha_hora_entrega - o.fecha_hora_creacion
                )
            ) / 60.0
         ) > z.tiempo_base_minutos
        then true
        else false
    end as es_entrega_retrasada,

    -- Clasificación del horario de la orden
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

    -- Información general de la orden
    o.metodo_pago,
    o.estado_orden,
    o.notas_entrega,
    o.comentario_cliente,
    o.motivo_cancelacion,

    -- Resumen de los platillos de la orden
    coalesce(d.cantidad_detalles, 0) as cantidad_detalles,

    coalesce(
        d.cantidad_total_platillos, 0
    ) as cantidad_total_platillos,

    -- Alias para mantener compatibilidad con análisis anteriores
    coalesce(
        d.cantidad_total_platillos, 0
    ) as cantidad,

    d.subtotal_orden_calculado,

    -- Detalles individuales de los platillos en formato JSON
    coalesce(
        d.detalles_orden,
        '[]'::jsonb
    ) as detalles_orden,

    -- Costos y ganancias de la orden
    coalesce(
        d.costo_total_ingredientes_orden, 0
    ) as costo_total_ingredientes_orden,

    coalesce(
        d.ganancia_bruta_orden, 0
    ) as ganancia_bruta_orden,

    case
        when coalesce(d.subtotal_orden_calculado, 0) > 0
        then round(
            (
                d.ganancia_bruta_orden
                / d.subtotal_orden_calculado * 100
            )::numeric,
            2
        )
        else 0
    end as margen_bruto_orden_pct,

    -- Importes registrados en la orden
    o.total_orden,
    o.costo_envio,
    o.propina,

    -- Información climática
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
