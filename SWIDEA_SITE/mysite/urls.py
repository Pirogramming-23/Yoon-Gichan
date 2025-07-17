from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 아이디어 관련
    path('', views.idea_list, name='idea_list'),
    path('idea/register/', views.idea_register, name='idea_register'),
    path('idea/<int:id>/', views.idea_detail, name='idea_detail'),
    path('idea/<int:id>/update/', views.idea_update, name='idea_update'),
    path('idea/<int:id>/delete/', views.idea_delete, name='idea_delete'),
    path('idea/<int:id>/toggle_star/', views.toggle_star, name='toggle_star'),
    path('idea/<int:id>/adjust_interest/', views.adjust_interest, name='adjust_interest'),
    path('idea/<int:id>/toggle_star_ajax/', views.toggle_star_ajax, name='toggle_star_ajax'),
    path('idea/<int:id>/adjust_interest_ajax/', views.adjust_interest_ajax, name='adjust_interest_ajax'),

    # 개발툴 관련
    path('devtool/', views.devtool_list, name='devtool_list'),
    path('devtool/register/', views.devtool_register, name='devtool_register'),
    path('devtool/<int:id>/', views.devtool_detail, name='devtool_detail'),
    path('devtool/<int:id>/update/', views.devtool_update, name='devtool_update'),
    path('devtool/<int:id>/delete/', views.devtool_delete, name='devtool_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)