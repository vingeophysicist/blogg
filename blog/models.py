from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce import models as tinymce_models
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from taggit.managers import TaggableManager



# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=250)
    category_slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('blog:category_detail_views', kwargs = {'slug': self.category_slug})



class Post(models.Model):
    title = models.CharField(max_length=400)
    body = tinymce_models.HTMLField()
    meta_description = models.CharField(max_length=800, null=True, blank=True)
    slug = models.SlugField(max_length=400, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    roll_out = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    read_time = models.IntegerField(default=0)
    featured_post = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    tags = TaggableManager()
    image_medium = ImageSpecField(source='image',
                                  processors=[Thumbnail(750, 500)],
                                  format='JPEG',
                                  options={'quality': 60})
    image_small = ImageSpecField(source='image',
                                 processors=[Thumbnail(90, 60)],
                                 format='JPEG',
                                 options={'quality': 60})
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
        

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    

    def __str__(self):
        return self.name
    
    

class about(models.Model):
    message = models.TextField()

    def __str__(self): 
        return self.message

    

    

    
