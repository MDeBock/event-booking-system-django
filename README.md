# Sistema de Gestión de Reservas y Eventos (Backend Django)

## Descripción del Proyecto
Este proyecto es una refactorización completa y escalable de un sistema de reservas de eventos. Diseñado con un enfoque estricto en la robustez del backend, implementa lógicas de negocio reales como el congelamiento de precios históricos, manejo de señas con recálculos por inflación, prevención de solapamiento de fechas y control de accesos basado en roles.

## Características Principales
* **Gestión de Usuarios y Roles:** Sistema de permisos estructurado para SuperAdmin, Administradores, Empleados (Reservas/Administrativos) y Clientes, integrando el sistema nativo de grupos de Django con un modelo de usuario personalizado.
* **Cotización y Congelamiento de Precios:** Lógica contable que preserva el valor histórico de salones y servicios adicionales al momento de la reserva, protegiendo las señas iniciales contra la devaluación o cambios de tarifas.
* **Prevención de Solapamientos:** Motor de validación de fechas que bloquea la disponibilidad considerando tanto el horario de duración del evento como los tiempos posteriores de limpieza y liberación de las instalaciones.
* **Catálogo Dinámico y Paquetes:** Sistema dual que permite el armado de eventos a medida o la selección de paquetes prearmados (combos) orientados a facilitar la elección del cliente.
* **Sistema de Reseñas:** Feedback de solo lectura y acceso público, restringido de forma estricta a reservas que hayan alcanzado el estado "Finalizada".

## Tecnologías Utilizadas
* **Framework:** Django (Python)
* **Base de Datos:** SQLite (Modelo de datos optimizado para migraciones directas a entornos de producción)
* **Dependencias:** 100% Open Source, sin librerías ni herramientas de pago.

## Arquitectura de la Base de Datos (MER)
A continuación se detalla el Modelo Entidad-Relación, diseñado para garantizar la integridad de los datos financieros, temporales y relacionales del sistema:

```mermaid
erDiagram
    USUARIO ||--o{ RESERVA : "realiza"
    USUARIO {
        int id PK
        string username "Heredado Django"
        string password "Heredado Django"
        string email "Heredado Django"
        string first_name "Heredado Django"
        string last_name "Heredado Django"
        string telefono "Custom"
        string dni_rut "Custom"
    }

    SALON ||--o{ RESERVA : "alberga"
    SALON }|--|{ ADICIONAL : "tiene_disponibles"
    SALON {
        int id PK
        string nombre
        text descripcion
        int capacidad_maxima
        decimal precio_base
    }

    ADICIONAL {
        int id PK
        string nombre
        text descripcion
        decimal precio_actual
    }

    TIPO_EVENTO ||--o{ RESERVA : "clasifica_estadistica"
    TIPO_EVENTO ||--o{ PAQUETE : "categoriza"
    TIPO_EVENTO {
        int id PK
        string nombre "Ej: 15 Años, Corporativo"
    }

    PAQUETE }|--|{ ADICIONAL : "incluye_servicios"
    PAQUETE }|--|| SALON : "incluye_salon"
    PAQUETE {
        int id PK
        int tipo_evento_id FK
        string nombre_combo "Ej: Fiesta 15 Oro"
        text descripcion
        int max_invitados
        decimal precio_paquete_actual
    }

    RESERVA ||--|{ RESERVA_ADICIONAL : "desglosa_extras"
    RESERVA ||--o| RESENA : "genera_feedback"
    RESERVA {
        int id PK
        int cliente_id FK
        int salon_id FK
        int tipo_evento_id FK
        int paquete_id FK "Opcional, null si es a medida"
        datetime fecha_hora_inicio
        datetime fecha_hora_liberacion
        string estado "Pendiente, Confirmada, Finalizada, Cancelada"
        decimal precio_historico_salon
        decimal monto_abonado "Admite 10% (min), 100% o custom"
        datetime fecha_creacion
    }

    RESERVA_ADICIONAL {
        int id PK
        int reserva_id FK
        int adicional_id FK
        decimal precio_historico_adicional
    }

    RESENA {
        int id PK
        int reserva_id FK
        int calificacion "1 a 5"
        text comentario
        datetime fecha_publicacion
    }
