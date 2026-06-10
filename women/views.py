from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Women, Category, TagPost
from .forms import AddPostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]

def index(request):
    posts = Women.published.all()
    context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=context)
def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'cat_selected': 0})
@permission_required('women.add_women', raise_exception=True)
@login_required
def addpage(request):
    ...

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug, is_published=Women.Status.PUBLISHED)
    context = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 0,
    }
    return render(request, 'women/post.html', context=context)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(category=category)
    context = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=context)
def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.posts.filter(is_published=Women.Status.PUBLISHED)
    context = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=context)