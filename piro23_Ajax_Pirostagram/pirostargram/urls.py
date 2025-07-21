from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
]