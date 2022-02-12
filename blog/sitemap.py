from django.contrib.sitemaps import Sitemap
from blog.models import Post, Category, Contact
from django.urls import reverse






class PostSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(roll_out=True)
    
    def lastmod(self, obj):
       return obj.updated







