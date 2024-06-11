from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('create/post/', views.DashboardPost.as_view(), name='create_post'),
    path(
        'edit/post/<int:id>/',
        views.DashboardPost.as_view(),
        name='edit_post'
        ),
    path(
        'dashboard/',
        views.DashboardAuthorIsPublished.as_view(),
        name='dashboard_author_is_published'
        ),
]
