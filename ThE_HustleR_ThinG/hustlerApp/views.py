from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from .models import *


def userSignUp(request):
    if request.method=='POST':
        form=userForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data.get('username')
            userProfile.objects.create(user=new_user,FirstName=username)
            messages.success(request,username+ "is successfully registered")
            return redirect('userLogin')  
    else:       
        form=userForm()
    context={'form':form}
    return render(request,'hustlerApp/signUp.html',context)


def userLogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'username or password in incorrect !')
    return render(request,'hustlerApp/login.html')


def logoutPage(request):
    logout(request)
    return redirect('userLogin')


def home(request):
    #return HttpResponse("this is a place for item to be displayed ")
    return render(request,'hustlerApp/home.html')



def news(request):
    all_news=newsReport.objects.filter(Status=True)
    newsPerPage=3
    paginator=Paginator(all_news,newsPerPage)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'all_news':all_news,'paginator':paginator,'page':page_obj}
    return render(request,'hustlerApp/news.html',context)


def readmore(request,news_id):
    news=newsReport.objects.get(id=news_id)
    news_view, created = newsViews.objects.get_or_create(users=request.user,news=news)
    views_count=newsViews.objects.filter(news=news).count()
    likes_count=newsLikes.objects.filter(news=news).count()
    context={'news':news,'views':views_count,'likes':likes_count}
    return render(request,'hustlerApp/readmore.html',context)


def likeNews(request,news_id):
    news=newsReport.objects.get(id=news_id)
    # to remove the dislike 
    newsDisLikes.objects.filter(users=request.user,news=news)
    like_news,created=newsLikes.objects.get_or_create(users=request.user,news=news)
    likes_count=newsLikes.objects.filter(news=news).count()
    views_count=newsViews.objects.filter(news=news).count()

    context={'news':news,'views':views_count,'likes':likes_count}
    return render(request,'hustlerApp/readmore.html',context)

def disLikeNews(request,news_id):
    news=newsReport.objects.get(id=news_id)
    # to delete like record if user has already liked
    newsLikes.objects.filter(users=request.user,news=news).delete()
    report_news,created= newsDisLikes.objects.get_or_create(users=request.user,news=news)
    return redirect('news')
    





