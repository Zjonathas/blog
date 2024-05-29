from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListViewHome.as_view(), name='home'),
    path('post/<int:pk>/', views.DetailPost.as_view(), name='detail_post'),
    path('search/', views.PostListViewSearch.as_view(), name='search'),
]
