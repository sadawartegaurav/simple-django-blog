from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    #post views
    path('', views.post_list, name='post_list'),
    path('<slug:post>/',views.post_detail, name='post_detail'),
    re_path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    ]