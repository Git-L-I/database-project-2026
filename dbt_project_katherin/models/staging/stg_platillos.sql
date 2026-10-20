select
    id_platillo,
    id_categoria,
    nombre_platillo,
    cast(precio_unitario as numeric(8, 2)) as precio_unitario,
    cast(costo_ingredientes as numeric(8, 2)) as costo_ingredientes,
    cast(tiempo_preparacion_minutos as numeric(5, 2)) as tiempo_preparacion_minutos,
    cast(requiere_horno as boolean) as requiere_horno,
    cast(activo as boolean) as activo
from {{ source('raw', 'platillos') }}