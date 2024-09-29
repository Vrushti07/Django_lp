from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
    
    
    from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})



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


from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'category']