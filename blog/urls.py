from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # URLs públicas
    path('', views.lista_posts, name='lista_posts'),
    path('categoria/<str:categoria_slug>/', views.posts_por_categoria, name='posts_por_categoria'),
    path('autor/<str:username>/', views.posts_por_autor, name='posts_por_autor'),
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
    
    # URLs de administración
    path('admin/', views.dashboard, name='dashboard'),
    
    # CRUD Posts
    path('admin/posts/', views.admin_posts, name='admin_posts'),
    path('admin/posts/crear/', views.crear_post, name='crear_post'),
    path('admin/posts/<int:pk>/', views.detalle_post_admin, name='detalle_post_admin'),
    path('admin/posts/<int:pk>/editar/', views.editar_post, name='editar_post'),
    path('admin/posts/<int:pk>/eliminar/', views.eliminar_post, name='eliminar_post'),
    
    # CRUD Categorías
    path('admin/categorias/', views.admin_categorias, name='admin_categorias'),
    path('admin/categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('admin/categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('admin/categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
]
