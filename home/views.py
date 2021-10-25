from django.db.models import query
from django.db.models.query_utils import PathInfo
from django.shortcuts import render, redirect
from django.contrib import messages
from home.forms import ContactForm
from articles.models import Post, Category
from home.models import newslater

# Importing modules for pagination
from django.core.paginator import Paginator


# cyberblog home page view
def home_view(request):
    context = {}
    # Last post to display
    last_post = Post.objects.all().last()
    context['last'] = last_post

    # Featured post to display
    featured = Post.objects.all().order_by('-pub_date')[1:3]
    context['featured'] = featured

    # Post by category name
    posts = []
    catposts = Post.objects.values('category', 'id')
    cats = {item['category'] for item in catposts}
    for cat in cats:
        pos = Post.objects.filter(category=cat).order_by('-pub_date')[:3]
        posts.append(pos)
    context['allposts'] = posts

    return render(request, 'home/index.html', context)



# contact us views
def contact_view(request):
    context = {}
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your query has been submitted successfully. Thank You!')
            return redirect('home:contact_us')
            
    context['form'] = form
    return render(request, 'home/contact.html', context)


# Join Newslater views
def newslater_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        customer_email = newslater(email=email)
        customer_email.save()
        messages.success(request, "Thank you for joining our newslater!")
        return redirect('home:home_page')


# verifying searched query and redirecting to the search_view
def search_query_view(request):
    query = request.GET['query']
    return redirect('home:search', query=query)



# creating search view
def search_view(request, query):
    allposts= Post.objects.filter(title__icontains=query).order_by('-pub_date')

    # code for pagination of 5 post per page
    pagin = Paginator(allposts, 5)
    page = request.GET.get('page')
    allposts = pagin.get_page(page)

    # Retriving data for sidebar
    allcategory = Category.objects.all().order_by('-id')[:5]
    last_five = Post.objects.all().order_by('-id')[:5]

    params={'allposts': allposts, 'allcategory': allcategory, 'latast': last_five, 'query': query}
    return render(request, 'home/search.html', params)