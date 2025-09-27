from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm, PostForm, CategoriaForm

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

# ========== CRUD PARA POSTS ==========

@login_required
def admin_posts(request):
    """Panel de administración de posts"""
    posts = Post.objects.filter(autor=request.user).order_by('-fecha_creacion')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query)
        )
    
    # Filtro por estado
    estado = request.GET.get('estado')
    if estado:
        posts = posts.filter(estado=estado)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_actual': estado,
    }
    return render(request, 'blog/admin/posts.html', context)

@login_required
def crear_post(request):
    """Crear nuevo post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, 'Post creado exitosamente.')
            return redirect('blog:admin_posts')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Post'
    }
    return render(request, 'blog/admin/form_post.html', context)

@login_required
def editar_post(request, pk):
    """Editar post existente"""
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post actualizado exitosamente.')
            return redirect('blog:admin_posts')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'titulo': 'Editar Post'
    }
    return render(request, 'blog/admin/form_post.html', context)

@login_required
def eliminar_post(request, pk):
    """Eliminar post"""
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado exitosamente.')
        return redirect('blog:admin_posts')
    
    context = {
        'post': post
    }
    return render(request, 'blog/admin/eliminar_post.html', context)

@login_required
def detalle_post_admin(request, pk):
    """Detalle del post para administración"""
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    
    context = {
        'post': post
    }
    return render(request, 'blog/admin/detalle_post.html', context)

# ========== CRUD PARA CATEGORÍAS ==========

@login_required
def admin_categorias(request):
    """Panel de administración de categorías"""
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        categorias = categorias.filter(nombre__icontains=query)
    
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blog/admin/categorias.html', context)

@login_required
def crear_categoria(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('blog:admin_categorias')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Categoría'
    }
    return render(request, 'blog/admin/form_categoria.html', context)

@login_required
def editar_categoria(request, pk):
    """Editar categoría existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('blog:admin_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': 'Editar Categoría'
    }
    return render(request, 'blog/admin/form_categoria.html', context)

@login_required
def eliminar_categoria(request, pk):
    """Eliminar categoría"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    # Verificar si hay posts usando esta categoría
    posts_count = Post.objects.filter(categoria=categoria).count()
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('blog:admin_categorias')
    
    context = {
        'categoria': categoria,
        'posts_count': posts_count
    }
    return render(request, 'blog/admin/eliminar_categoria.html', context)

# ========== DASHBOARD ==========

@login_required
def dashboard(request):
    """Dashboard principal del administrador"""
    # Estadísticas
    total_posts = Post.objects.filter(autor=request.user).count()
    posts_publicados = Post.objects.filter(autor=request.user, estado='publicado').count()
    posts_borrador = Post.objects.filter(autor=request.user, estado='borrador').count()
    total_categorias = Categoria.objects.count()
    total_comentarios = Comentario.objects.filter(post__autor=request.user).count()
    
    # Posts recientes
    posts_recientes = Post.objects.filter(autor=request.user).order_by('-fecha_creacion')[:5]
    
    # Posts más visitados
    posts_populares = Post.objects.filter(autor=request.user, estado='publicado').order_by('-visitas')[:5]
    
    context = {
        'total_posts': total_posts,
        'posts_publicados': posts_publicados,
        'posts_borrador': posts_borrador,
        'total_categorias': total_categorias,
        'total_comentarios': total_comentarios,
        'posts_recientes': posts_recientes,
        'posts_populares': posts_populares,
    }
    return render(request, 'blog/admin/dashboard.html', context)
