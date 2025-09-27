from django.contrib import admin
from .models import Post, Categoria, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']
    search_fields = ['nombre']
    prepopulated_fields = {'nombre': ('nombre',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'estado', 'fecha_publicacion', 'visitas']
    list_filter = ['estado', 'categoria', 'fecha_publicacion', 'autor']
    search_fields = ['titulo', 'contenido']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ['-fecha_publicacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'slug', 'autor', 'categoria')
        }),
        ('Contenido', {
            'fields': ('resumen', 'contenido', 'imagen')
        }),
        ('Configuración', {
            'fields': ('estado', 'fecha_publicacion')
        }),
    )

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'post', 'fecha_creacion', 'activo']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['contenido', 'autor__username', 'post__titulo']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
