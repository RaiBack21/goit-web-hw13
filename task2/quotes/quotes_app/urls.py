from django.urls import include, path

from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/<str:author_name>/', views.author_detail, name='author_detail'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag_name>/', views.search_by_tag, name="search_by_tag"),
    path('parse_data/', views.parse_data, name="parse_data"),
]