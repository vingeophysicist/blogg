from django.urls import path
from django.urls import path, include, re_path
from . import views





app_name = 'blog'





urlpatterns = [
    path('', views.index, name ='indexpage'),
    path("", views.subscription, name="subscription"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
       views.post_detail,
       name ='post_detail'),
    path('<slug:category_slug>/', views.category_detail_views, name = 'category_detail_views'),
    path('tag/<slug:slug>/', views.tagged, name = 'tagged'),
    path('contact.html/', views.contact, name = 'contact'),
    path('about.html/', views.aboutme, name = 'aboutme'),
]
