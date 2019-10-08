
from django.contrib import admin
from django.urls import path, include, re_path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import SearchResultsView


urlpatterns = [
    path('admin/', admin.site.urls),
    #Defined NameSpace and view for website
    path('',views.home, name='home'),
    path('blog/', include('blog.urls', namespace='blog')),

    #View for API 
    path(r'post-api', views.PostAPIView.as_view(), name='post-list'),

    #View for CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', SearchResultsView.as_view(), name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
