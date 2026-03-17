# Sistema de Gestión de Reservas y Eventos (SaaS B2B2C)

## Descripción del Proyecto
Plataforma web desarrollada en Django para la comercialización y gestión de salones de eventos. Este proyecto no es un simple CRUD; está diseñado con un enfoque estricto en la lógica de negocios real, resolviendo el problema de las cotizaciones en economías inflacionarias. Permite a los clientes congelar porcentajes de su evento mediante el pago de señas, y le provee al staff un tablero de control (Dashboard) segmentado por roles.

## Características Principales (Fase 1 - Core)

* **Motor Financiero Anti-Inflación:** Algoritmo de recálculo dinámico. Si el precio del salón aumenta, el sistema respeta matemáticamente el porcentaje del evento que el cliente ya abonó (seña) y solo aplica el nuevo precio al porcentaje deudor, generando automáticamente una bonificación contable ("Descuento por Pago Anticipado") para cuadrar la caja del negocio.
* **Control de Acceso Basado en Roles (RBAC):** Separación total de vistas. Los clientes acceden a un panel de seguimiento de cuenta, mientras que el personal (Staff/Administrativos) es redirigido a un Dashboard Gerencial exclusivo, sin necesidad de darles acceso al `/admin/` nativo de Django.
* **Catálogo y Alta Dinámica:** Gestión de salones, servicios adicionales y capacidades desde el frontend. Inclusión de subida de imágenes optimizadas (`ImageField`) y galerías interactivas con Lightbox.
* **Arquitectura de Vistas Desacopladas:** Uso intensivo de plantillas dinámicas y Modales de Bootstrap para renderizar relaciones complejas (Reservas -> Detalles -> Adicionales) garantizando una experiencia de usuario (UX) fluida y sin recargas innecesarias.

*Nota: La arquitectura de la base de datos ya se encuentra preparada para la Fase 2 del roadmap (Sistema de Reseñas y Paquetes/Combos).*

## Tecnologías Utilizadas
* **Backend:** Python 3, Django
* **Base de Datos:** SQLite3 (Modelo de datos normalizado y preparado para migración a PostgreSQL)
* **Frontend:** HTML5, Bootstrap 5, FontAwesome, FsLightbox
* **Arquitectura:** MVT (Model-View-Template), DRY (Don’t Repeat Yourself)

## Arquitectura de la Base de Datos (MER)
El Modelo Entidad-Relación fue diseñado para garantizar la integridad financiera y escalar hacia futuras integraciones de módulos (Reseñas y Paquetes prearmados):

```mermaid
erDiagram
    USUARIO ||--o{ RESERVA : "realiza"
    USUARIO {
        int id PK
        string username "Heredado Django"
        string password "Heredado Django"
        string email "Heredado Django"
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
        decimal precio_actual
    }

    TIPO_EVENTO ||--o{ RESERVA : "clasifica"
    TIPO_EVENTO ||--o{ PAQUETE : "categoriza"
    TIPO_EVENTO {
        int id PK
        string nombre
    }

    PAQUETE }|--|{ ADICIONAL : "incluye_servicios"
    PAQUETE }|--|| SALON : "incluye_salon"
    PAQUETE {
        int id PK
        string nombre_combo
        decimal precio_paquete_actual
    }

    RESERVA ||--|{ RESERVA_ADICIONAL : "desglosa_extras"
    RESERVA ||--o| RESENA : "genera_feedback"
    RESERVA {
        int id PK
        int cliente_id FK
        int salon_id FK
        string estado "Pendiente, Confirmada, Finalizada"
        decimal monto_abonado "Admite señas parciales"
    }

    RESERVA_ADICIONAL {
        int id PK
        int reserva_id FK
        int adicional_id FK
    }

    RESENA {
        int id PK
        int reserva_id FK
        int calificacion
    }

## Cómo ejecutar este proyecto localmente
Clonar el repositorio.

Crear un entorno virtual: python -m venv env

Activar el entorno virtual e instalar dependencias: pip install -r requirements.txt

Aplicar las migraciones para crear la base de datos local: python manage.py migrate

Crear un superusuario para acceder al Dashboard Gerencial: python manage.py createsuperuser

Iniciar el servidor: python manage.py runserver

Acceder a http://127.0.0.1:8000 en el navegador. Para habilitar las funciones financieras y métricas en el panel, asignar el grupo "Administrativos" al usuario desde el admin nativo (/admin/).