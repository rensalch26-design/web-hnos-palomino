# Hnos Palomino

Catálogo de textiles con diseño neumórfico, HTML, CSS, JavaScript nativo y Python. Incluye administrador, selección de producto/variante → sede → asesor → WhatsApp, y conexión preparada para Supabase.

## Abrir la web

Desde esta carpeta, ejecuta:

```powershell
python server.py
```

También puedes hacer doble clic en `INICIAR.bat`. Abre http://127.0.0.1:8000 y el administrador en http://127.0.0.1:8000/admin.html. Python 3.10 o superior; no requiere instalar dependencias. No abras el HTML con doble clic: necesita el servidor para cargar la configuración.

## Estado de esta entrega

- La versión local funciona en **demostración** sin credenciales.
- Los cambios del administrador demo se guardan en el navegador (localStorage), no en una base de datos compartida. No subir información confidencial a esta demostración.
- Las fotos son ilustrativas, generadas con IA. Los seis productos y los nombres de asesores son ejemplos, no inventario real. Los Olivos y Lince incluyen los tres teléfonos por sede proporcionados por el propietario, con prefijo +51. La Molina continúa sin teléfonos configurados.
- La disponibilidad es manual por producto y sede; las variantes se incluyen en la consulta, pero no tienen inventario independiente todavía. La consulta no reserva ni descuenta unidades.
- No se ha creado ni conectado un proyecto de Supabase, ni publicado la web en Vercel.

## Archivos

```text
public/
  index.html             Catálogo público
  admin.html             Administrador
  css/styles.css         Diseño neumórfico y adaptación a móvil
  js/catalog.js          Buscador, filtros y contacto por WhatsApp
  js/admin.js            Productos, fotografías y asesores
  js/store.js            Datos demo / REST de Supabase / autenticación
  js/data.js             Datos de demostración
  js/ui.js               Componentes y validaciones compartidas
  assets/                Fotografías y favicon locales
server.py                Servidor local Python, solo expone public/
app_config.py            Configuración pública y cabeceras
api/config.py            Función Python para Vercel
supabase/setup.sql       Tablas, permisos RLS y bucket de fotografías
.env.example             Plantilla de configuración, sin secretos
vercel.json              Configuración para publicar posteriormente
tests/                   Pruebas de lógica y del servidor
```

## Conectar Supabase

1. Crear un proyecto de Supabase. En un proyecto nuevo, ejecutar `supabase/setup.sql` una sola vez en SQL Editor. Si ya hay tablas con esos nombres, revisar el esquema antes de ejecutarlo. El catálogo real arranca vacío.
2. En Authentication → Users, crear la cuenta del administrador. Desactivar el registro público de usuarios. La web no ofrece registro abierto.
3. En SQL Editor, dar permiso a la cuenta con el correo exacto:

   ```sql
   insert into public.admin_users(user_id)
   select id from auth.users where email = 'CORREO_REAL_DEL_ADMINISTRADOR';
   ```

4. Copiar `.env.example` como `.env` y completar `SUPABASE_URL` y `SUPABASE_PUBLISHABLE_KEY` con la URL del proyecto y una clave **sb_publishable_**. No usar `service_role`, `sb_secret_` ni la contraseña de la base de datos. `.env` no se sirve al navegador ni se incluye en Git.
5. Reiniciar Python e ingresar al administrador con correo y contraseña. Crear los productos reales y los asesores de cada sede. Los datos demo no se migran automáticamente.
6. Comprobar desde una ventana sin sesión: solo productos publicados y asesores activos. Probar con una cuenta sin rol administrador: no puede editar datos ni subir fotos. La autenticación y las políticas RLS deben validarse en el proyecto real antes del lanzamiento.

La URL y la clave publicable son públicas por diseño; las políticas RLS controlan quién puede leer y escribir. El navegador no recibe claves privilegiadas. El rol administrador se asigna desde SQL, nunca desde campos editables de la cuenta. Los teléfonos comerciales activos son públicos para construir los enlaces de WhatsApp.

## Imágenes

Las nuevas fotos se reducen a un máximo de 1200 px y se convierten a WebP antes de subirlas. El bucket `catalog` acepta fotos hasta 2 MB. Las fotos reemplazadas se conservan para no borrar una imagen compartida; revisar y limpiar archivos sin referencias periódicamente desde Storage. Los respaldos de la base de datos no sustituyen el respaldo de las imágenes: exportar ambos.

El archivo `public/assets/textiles.webp` es un atlas de cuatro fotografías de ejemplo usado mediante CSS; el PNG original se conserva en la misma carpeta. Generado con la herramienta integrada de imágenes. Resumen del prompt: cuatro escenas fotográficas en cuadrícula 2×2 sin texto (sábanas marfil, edredón salvia, cortinas de lino y almohadas blancas), luz natural y tonos cálidos.

## Vercel (siguiente etapa)

Importar esta carpeta como proyecto con preset **Other**. `vercel.json` usa `public` como salida estática y `api/config.py` como función Python. Configurar las mismas dos variables de Supabase en Vercel. El despliegue sin Supabase muestra un error de configuración; no habilita el administrador demo. Verificar el despliegue antes de compartir la URL. Google Fonts se carga desde su CDN; hay tipografías de respaldo.

## Verificación local

```powershell
node --test tests/logic.test.js
python -m unittest discover -s tests -p "test_*.py"
```

Pendiente de validación externa: autenticación, RLS y almacenamiento de un proyecto real de Supabase; despliegue en Vercel; números reales de WhatsApp. No se ha integrado Odoo ni una pasarela de pago.
