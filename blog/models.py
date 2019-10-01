from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

#Third party plugins
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from meta.models import ModelMeta

#Generated token f664b0c166c6cb370f23168f3e4783e1a08e3f8b for user gaurav

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(ModelMeta, models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    
    title = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')

    #https://stackoverflow.com/questions/13960612/django-blog-post-image
    coverimage = models.ImageField(upload_to='uploads/%Y/%m/%d', default='')

    #https://djangopy.org/package-of-week/categories-with-django-mptt/
    category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True)

    body = RichTextUploadingField(blank=True, null=True, default='')
    video = RichTextUploadingField(blank=True, null=True, config_name='special',external_plugin_resources=[('youtube','/static/blog/vendor/ckeditor_plugins/youtube/youtube/','plugin.js',)],)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects = models.Manager()
    published = PublishedManager()

    _metadata = {
        'title': 'title',
        'description': 'body',
        'image': 'get_image',
        'url': 'slug',
        'video': 'video',
    }

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    #https://github.com/djangopy-org/django_mptt_categories/blob/master/src/blog/models.py
    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]

        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
    def get_image(self):
        return self.coverimage.url

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]

        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name