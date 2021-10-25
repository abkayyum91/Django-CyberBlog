from django.urls import path
from home import views


app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('search-query/', views.search_query_view, name="search_query"),
    path('search/<str:query>', views.search_view, name="search"),
    path('contact/', views.contact_view, name='contact_us'),
    path('newslater/', views.newslater_view, name='newslater'),
]