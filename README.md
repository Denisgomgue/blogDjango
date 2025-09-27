# Mi Blog - Django + Tailwind CSS

Un blog moderno y responsivo construido con Django y Tailwind CSS.

## 🚀 Características

- **Frontend moderno**: Diseño responsivo con Tailwind CSS
- **Sistema de posts**: Crear, editar y publicar artículos
- **Categorías**: Organizar posts por categorías
- **Comentarios**: Sistema de comentarios para usuarios autenticados
- **Búsqueda**: Buscar posts por título y contenido
- **Paginación**: Navegación fácil entre páginas
- **Admin panel**: Interfaz administrativa completa
- **Contador de visitas**: Seguimiento de popularidad de posts

## 🛠️ Tecnologías utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: Tailwind CSS (CDN)
- **Base de datos**: SQLite (desarrollo)
- **Iconos**: Font Awesome
- **Fuentes**: Google Fonts (Inter)

## 📋 Requisitos

- Python 3.8+
- pip

## 🚀 Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd blog
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install django pillow
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## 📱 Uso

### Acceso al blog
- **Blog principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

### Credenciales por defecto
- **Usuario**: admin
- **Contraseña**: admin123

## 🎨 Características del diseño

### Responsive Design
- Diseño adaptativo para móviles, tablets y desktop
- Navegación móvil con menú hamburguesa
- Grid system responsivo

### Componentes UI
- **Header**: Logo, navegación y menú móvil
- **Cards**: Posts con imagen, título, resumen y metadatos
- **Sidebar**: Posts relacionados y información del autor
- **Paginación**: Navegación entre páginas
- **Formularios**: Comentarios con validación
- **Footer**: Enlaces y redes sociales

### Paleta de colores
- **Primario**: Blue-600 (#2563eb)
- **Secundario**: Gray-900 (#111827)
- **Fondo**: Gray-50 (#f9fafb)
- **Texto**: Gray-700 (#374151)

## 📁 Estructura del proyecto

```
blog/
├── mi_blog/                 # Configuración del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── ...
├── blog/                   # Aplicación del blog
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── forms.py           # Formularios
│   ├── admin.py           # Configuración del admin
│   ├── urls.py            # URLs de la app
│   └── templates/         # Templates HTML
│       └── blog/
│           ├── base.html
│           ├── lista_posts.html
│           ├── detalle_post.html
│           ├── posts_por_categoria.html
│           └── posts_por_autor.html
├── static/                # Archivos estáticos
├── media/                 # Archivos subidos
├── manage.py             # Script de gestión
└── README.md             # Este archivo
```

## 🔧 Modelos de datos

### Categoria
- `nombre`: Nombre de la categoría
- `descripcion`: Descripción opcional
- `fecha_creacion`: Fecha de creación

### Post
- `titulo`: Título del post
- `slug`: URL amigable
- `autor`: Usuario que creó el post
- `categoria`: Categoría del post
- `contenido`: Contenido completo
- `resumen`: Resumen del post
- `imagen`: Imagen opcional
- `estado`: Borrador o publicado
- `fecha_publicacion`: Fecha de publicación
- `visitas`: Contador de visitas

### Comentario
- `post`: Post relacionado
- `autor`: Usuario que comentó
- `contenido`: Contenido del comentario
- `fecha_creacion`: Fecha del comentario
- `activo`: Estado del comentario

## 🎯 Funcionalidades

### Para visitantes
- Ver lista de posts publicados
- Leer posts completos
- Buscar posts
- Filtrar por categorías
- Ver posts por autor
- Comentar (requiere autenticación)

### Para administradores
- Crear, editar y eliminar posts
- Gestionar categorías
- Moderar comentarios
- Ver estadísticas de visitas
- Configurar estado de posts

## 🚀 Despliegue

### Variables de entorno
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECRET_KEY = 'tu-clave-secreta'
```

### Archivos estáticos
```bash
python manage.py collectstatic
```

### Base de datos
- Configurar PostgreSQL o MySQL para producción
- Actualizar `DATABASES` en `settings.py`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

- **Autor**: Tu nombre
- **Email**: tu-email@ejemplo.com
- **Proyecto**: [https://github.com/tu-usuario/mi-blog](https://github.com/tu-usuario/mi-blog)

---

¡Gracias por usar Mi Blog! 🎉
