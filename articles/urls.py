from django.urls import path
from articles import views


app_name = 'articles'

urlpatterns = [
    path('', views.article_list_view, name="article_list"),
    path('create_new_post', views.create_new_post_view, name="create_new_post"),
    path('post/<slug:the_slug>', views.post_view, name="post"),
    path('category/<int:ctg>', views.category_post_view, name="post_by_category"),
    path('author/<str:pk>', views.author_post_view, name="post_by_author"),
]