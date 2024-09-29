from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm

# Create blog
def create_blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

# Get a single blog
def single_blog_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/single_blog.html', {'blog': blog})

# Get all blogs
def all_blogs_view(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/all_blogs.html', {'blogs': blogs})

# Update a blog
def update_blog_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('single_blog', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/update_blog.html', {'form': form})

# Delete a blog
def delete_blog_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('all_blogs')
    return render(request, 'blog/delete_blog.html', {'blog': blog})