select
    cast(fecha as date) as fecha_clima,
    cast(precipitacion_mm as numeric(5, 2)) as precipitacion_mm,
    cast(temperatura_c as numeric(4, 2)) as temperatura_c,
    condicion_cielo
from {{ source('raw', 'clima_diario') }}