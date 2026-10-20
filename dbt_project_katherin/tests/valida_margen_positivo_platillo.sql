-- Ningún platillo activo en el menú debe venderse por debajo de su costo de ingredientes
select
    id_platillo,
    nombre_platillo,
    precio_unitario,
    costo_ingredientes
from {{ ref('dim_platillos') }}
where precio_unitario < costo_ingredientes
