from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('categoria/<str:categoria_slug>/', views.posts_por_categoria, name='posts_por_categoria'),
    path('autor/<str:username>/', views.posts_por_autor, name='posts_por_autor'),
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
]
