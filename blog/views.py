from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm

def lista_posts(request):
    """Vista para mostrar la lista de posts publicados"""
    posts = Post.objects.filter(estado='publicado')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query) |
            Q(resumen__icontains=query)
        )
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categoria_id=categoria_id)
    
    # Paginación
    paginator = Paginator(posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'query': query,
        'categoria_actual': categoria_id,
    }
    return render(request, 'blog/lista_posts.html', context)

def detalle_post(request, slug):
    """Vista para mostrar el detalle de un post"""
    post = get_object_or_404(Post, slug=slug, estado='publicado')
    
    # Incrementar contador de visitas
    post.incrementar_visitas()
    
    # Obtener comentarios activos
    comentarios = post.comentarios.filter(activo=True)
    
    # Formulario de comentario
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = post
                comentario.autor = request.user
                comentario.save()
                messages.success(request, 'Tu comentario ha sido publicado.')
                return redirect('blog:detalle_post', slug=post.slug)
        else:
            messages.warning(request, 'Debes iniciar sesión para comentar.')
    else:
        form = ComentarioForm()
    
    # Posts relacionados (misma categoría)
    posts_relacionados = Post.objects.filter(
        categoria=post.categoria,
        estado='publicado'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'posts_relacionados': posts_relacionados,
    }
    return render(request, 'blog/detalle_post.html', context)

def posts_por_categoria(request, categoria_slug):
    """Vista para mostrar posts de una categoría específica"""
    categoria = get_object_or_404(Categoria, nombre__iexact=categoria_slug)
    posts = Post.objects.filter(categoria=categoria, estado='publicado')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categoria': categoria,
        'page_obj': page_obj,
    }
    return render(request, 'blog/posts_por_categoria.html', context)

def posts_por_autor(request, username):
    """Vista para mostrar posts de un autor específico"""
    from django.contrib.auth.models import User
    autor = get_object_or_404(User, username=username)
    posts = Post.objects.filter(autor=autor, estado='publicado')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'autor': autor,
        'page_obj': page_obj,
    }
    return render(request, 'blog/posts_por_autor.html', context)
