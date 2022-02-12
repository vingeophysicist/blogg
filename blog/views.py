from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Category, Post, about
from django.db.models import Count 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.contrib import messages
from django.conf import settings
from taggit.models import Tag
from blog.forms import PostForm, ContactForm




# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID







# Create your views here.

        




def index(request):
    posts = Post.objects.filter(roll_out=True).order_by('-publish')
    category = Category.objects.all().annotate(posts_count=Count('post'))
    common_tags = Post.tags.most_common()[:4]
    
    usage = subscription(request)
    
    
   
   

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)  # 6 post per page
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    


    context = {
               'category':category, 
               'page_obj':page_obj,
               'common_tags':common_tags, 
               'posts':posts}
     
    return render(request, "blog/index.html", context)




def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                                   roll_out=True,
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    post_related = post.tags.similar_objects()
    
    paginator = Paginator(post_related, 5)  # 5 post per page
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    usage = subscription(request)


    context = {
        'post': post, 
        #'post_related': post_related 
        'page_obj':page_obj
        }


    return render(request, 'blog/post_detail.html', context)


def category_detail_views(request, category_slug):
    category = get_object_or_404(Category, category_slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-publish')
    
    paginator = Paginator(posts, 5)  # 5 post per page
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {'category':category, 
               'posts':posts, 
               'page_obj':page_obj,
               }
    return render(request, 'blog/category.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    


    paginator = Paginator(posts, 5)  # 6 post per page
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'posts':posts, 
               'tag':tag, 
               'page_obj':page_obj,
               }
    
    return render(request, "blog/taggit.html", context)


def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        
        
        
def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe(email)                    # function to access mailchimp
        messages.success(request, "Email received. thank You! ") # message

    return HttpResponse("/")



def contact(request):
    form = ContactForm()
    #if request.method == 'POST':
    #    form = ContactForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('contact')
    if request.is_ajax():
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'msg':'success'
                
            })


    context = { 'form':form }

    return render(request, 'blog/contact.html', context) 



def aboutme(request):
    about_me = about.objects.all()
    return render(request, 'blog/about.html', {'about_me': about_me})



