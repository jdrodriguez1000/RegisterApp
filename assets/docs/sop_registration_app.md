# SOP: Construcción de Aplicación de Registro de Usuarios (Flet + Fleting + Supabase)

Este documento detalla el Procedimiento Operativo Estándar (SOP) para el desarrollo de la aplicación de aprendizaje de Flet y Fleting, con integración de Supabase.

---

## 1. Visión General del Proyecto
La aplicación es una plataforma de registro de usuarios que implementa flujos de autenticación seguros, gestión de perfiles avanzada y soporte multi-idioma.

### Restricciones de Diseño y Visualización
- **Enfoque Mobile-Only**: La aplicación debe mostrarse **siempre** con dimensiones de dispositivo móvil (ej. iPhone 17), independientemente de si se ejecuta en escritorio o web.
- **Dimensiones sugeridas**: ~390x844px (o dimensiones estándar de iPhone recientes).
- **Control de Ventana**: Se debe configurar en `main.py` o `core/app.py` para bloquear el tamaño de la ventana o centrar el contenido en un "contenedor móvil".

### Tecnologías Core
- **Framework**: Flet (Python)
- **Micro-framework**: Fleting (Arquitectura MVC, i18n, Responsividad)
- **Backend/Base de Datos**: Supabase (Auth & PostgreSQL)

---

## 2. Requisitos Funcionales

### A. Onboarding / Bienvenida
1.  **Vista de Bienvenida**:
    - Imagen de fondo premium (basada en el diseño de referencia).
    - Título impactante y descripción corta.
    - Botón "Get Started" destacado para iniciar el flujo de la aplicación.

### A. Flujo de Autenticación
1.  **Registro**:
    - Campos: Correo electrónico, Contraseña, Nombre completo.
    - Acción: Envío de correo electrónico de confirmación tras el registro.
2.  **Verificación**:
    - Un usuario **no puede** entrar a la aplicación sin confirmar su correo.
    - Se debe mostrar una vista informativa si intenta ingresar sin haber validado su email.
3.  **Inicio de Sesión**:
    - Validar credenciales y estado de confirmación de email.
4.  **Recuperación de Contraseña**:
    - Flujo de "Olvidé mi contraseña" mediante envío de correo para reseteo.
5.  **Cambio de Contraseña (Autenticado)**:
    - Solicitar contraseña actual y nueva contraseña para mayor seguridad.

### B. Gestión de Perfil
1.  **Validación de Datos Faltantes**:
    - Tras el login, verificar si existen: Género, Fecha de nacimiento, Estado civil, Color favorito, Deporte favorito.
2.  **Formulario de Completitud**:
    - Si falta información, redirección obligatoria a la vista de registro de datos adicionales.
3.  **Dashboard de Usuario**:
    - Mostrar: Nombre, Email, Género, Fecha de nacimiento, Estado civil, Color favorito, Deporte favorito.

---

## 3. Arquitectura Técnica y Estructura

Siguiendo las mejores prácticas de **Fleting**:

-   **Modelos (`models/`)**: Definir la estructura del `UserProfile`.
-   **Vistas (`views/pages/`)**:
    -   `WelcomeView` (Punto de entrada con botón "Get Started")
    -   `LoginView`
    -   `RegisterView`
    -   `EmailVerificationPendingView`
    -   `ProfileCompletionView`
    -   `DashboardView`
    -   `ForgotPasswordView`
    -   `ChangePasswordView`
-   **Controladores (`controllers/`)**: Lógica de interacción con Supabase Auth y Database.
-   **Idiomas (`configs/languages/`)**: Archivos `es.json` y `en.json`.

### Detalle de Carpeta Core (`core/`)
Infraestructura fundamental del micro-framework:

- **`core/app.py`**: Orquestador principal. Configura la app de Flet e inicializa componentes dinámicos como el AppBar.
- **`core/state.py`**: Gestiona el `AppState` global (idioma activo, tipo de dispositivo, estado de sesión).
- **`core/router.py`**: Lógica de navegación y transiciones entre vistas.
- **`core/responsive.py`**: Determina si el dispositivo es `mobile`, `tablet` o `desktop`.
- **`core/i18n.py`**: Sistema de internacionalización para cargar traducciones mediante `I18n.t()`.
- **`core/database.py`**: Centraliza la conexión con **Supabase** (Singleton).
- **`core/logger.py`**: Interfaz unificada para logs en desarrollo y producción.
- **`core/error_handler.py`**: Capturador global de excepciones para evitar cierres inesperados.

### Detalle de Carpeta Configs (`configs/`)
Configuraciones globales y personalización de la aplicación:

- **`configs/app_config.py`**: Ajustes generales (nombre de la app, versión, tema inicial, links de soporte).
- **`configs/routes.py`**: Mapa de rutas centralizado. Utiliza *lazy loading* para cargar las vistas solo cuando se necesitan, optimizando memoria.
- **`configs/languages/`**: Directorio que contiene los archivos JSON de traducción (`es.json`, `en.json`). Es el corazón del sistema i18n.

---

## 4. Diseño de Base de Datos (Supabase)

### Tabla: `profiles`
| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | uuid (PK) | Relacionado con `auth.users.id` |
| `full_name` | text | Nombre completo |
| `email` | text | Email del usuario |
| `gender` | text | Género |
| `birth_date` | date | Fecha de nacimiento |
| `civil_status` | text | Estado civil |
| `favorite_color` | text | Color favorito |
| `favorite_sport` | text | Deporte favorito |
| `updated_at` | timestamp | Última actualización |

---

## 5. Estándares de Seguridad
1.  **Contraseñas Fuertes**:
    - Mínimo 8 caracteres.
    - Al menos una mayúscula, una minúscula, un número y un carácter especial.
2.  **Row Level Security (RLS)**: En Supabase, asegurar que los usuarios solo puedan leer/editar su propio perfil.
3.  **Validación Server-side**: No confiar solo en la UI; validar datos en Supabase.

---

## 6. Configuración Multi-idioma (i18n)
La aplicación debe utilizar el sistema `I18n.t()` de Fleting.
- El cambio de idioma debe ser accesible desde el AppBar o Configuración.
- Todas las etiquetas de UI, mensajes de error y notificaciones deben estar en `es.json` y `en.json`.

---

## 7. Plan de Implementación Sugerido
1.  **Módulo Supabase**: Configuración de tablas, políticas RLS y Auth settings.
2.  **Módulo Fleting Core**: Configuración inicial, rutas y carpetas de idiomas.
3.  **Vista de Bienvenida**: Implementación del onboarding inicial.
4.  **Vistas de Auth**: Implementación de Login, Registro y Recuperación.
4.  **Lógica de Redirección**: `Router` personalizado que verifique `email_confirmed` y `profile_complete`.
5.  **Vistas de Perfil**: Formulario de datos adicionales y Dashboard.
