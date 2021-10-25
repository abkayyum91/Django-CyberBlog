from django.contrib import messages
from django.contrib.auth.models import User
from django.core import paginator
from django.shortcuts import redirect, render
from articles.models import Post, Category, postComment
from articles.forms import postCommentForm, createPostForm
from articles.templatetags import articles_extras

# importing modules for pagination
from django.core.paginator import Paginator



# cyberblog homepage view
def article_list_view(request):
    allposts = Post.objects.all().order_by('-pub_date')

    # code for pagination of 5 post per page
    pagin = Paginator(allposts, 5)
    page = request.GET.get('page')
    allposts = pagin.get_page(page)

    # Retriving data for sidebar
    allcategory = Category.objects.all().order_by('-id')[:5]
    last_five = Post.objects.all().order_by('-id')[:5]

    context = {'allposts': allposts, 'allcategory': allcategory, 'latast': last_five}
    return render(request, 'articles/article_list.html', context)


# cyberblog single post view
def post_view(request, the_slug):
    context = {}
    form = postCommentForm()
    context['form'] = form
    post = Post.objects.get(slug=the_slug)
    context['post'] = post

    # Retreiving comments 
    comments = postComment.objects.filter(post=post, parent=None).order_by('-timestamp')
    replies = postComment.objects.filter(post=post).exclude(parent=None).order_by('-timestamp')
    context['comments'] = comments

    replyDict={}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)
    
    context['replyDict'] = replyDict

    # Retrieving category
    allcategory = Category.objects.all().order_by('-id')[:5]
    context['allcategory'] = allcategory
    # Retriving last five post (For Latast Post) by id from model
    latast_post = Post.objects.all().order_by('-id')[:5]
    context['latast'] = latast_post

    if request.method == 'POST':
        form = postCommentForm(request.POST)
        if form.is_valid():
            instanse = form.save(commit=False)
            instanse.user = request.user
            instanse.post = Post.objects.get(slug=the_slug)
            parentId = request.POST.get('parentId')
            if parentId:
                instanse.parent = postComment.objects.get(id=parentId)
                instanse.save()
                messages.success(request, 'Your reply is submitted!')
                return redirect('articles:post', the_slug)
            else:
                instanse.save()
                messages.success(request, 'Your Comment is published successfully!')
        else:
            context['form'] = form
            messages.error(request, 'Please write some useful comments?')
    
    return render(request, 'articles/post.html', context)



# Post by category views
def category_post_view(request, ctg):
    cat = Category.objects.get(id=ctg)
    allposts = cat.post_set.all().order_by('-pub_date')
    
    pagin = Paginator(allposts, 5)
    page = request.GET.get('page')
    allposts = pagin.get_page(page)

    # Retriving data for sidebar
    allcategory = Category.objects.all().order_by('-id')[:5]
    last_five = Post.objects.all().order_by('-id')[:5]

    context = {'allposts': allposts, 'allcategory': allcategory, 'latast': last_five, 'catname':cat}
    return render(request, 'articles/post_by_category.html', context)


# Post by category views
def author_post_view(request, pk):
    author = User.objects.get(username=pk)
    allposts = author.post_set.all().order_by('-pub_date')
    pagin = Paginator(allposts, 5)
    page = request.GET.get('page')
    allposts = pagin.get_page(page)

    # Retriving data for sidebar
    allcategory = Category.objects.all().order_by('-id')[:5]
    last_five = Post.objects.all().order_by('-id')[:5]

    context = {'allposts': allposts, 'allcategory': allcategory, 'latast': last_five, 'author':author}
    return render(request, 'articles/post_by_author.html', context)



# Create new post views
def create_new_post_view(request):
    context = {}
    form = createPostForm()
    if request.method == 'POST':
        form = createPostForm(request.POST, request.FILES)
        print('working')


    context['form'] = form
    return render(request, 'articles/create_post.html', context)

