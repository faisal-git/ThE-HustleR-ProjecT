from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.views import View
from django.urls import reverse
import os
from .forms import *
from .models import *


def userSignUp(request):
    if request.method=='POST':
        form=userForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            new_user.is_active=False
            new_user.save()
            current_site = get_current_site(request)
            email_body = {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            }

            link = reverse('activate', kwargs={
                            'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+new_user.username + \
                ',Please the link below to activate your account \n'+activate_url,
                'noreply@semycolon.com',
                [new_user.email],
            )
            #print(new_user.email,new_user.username)
            email.send(fail_silently=False)
            username=form.cleaned_data.get('username')
            userProfile.objects.create(user=new_user,FirstName=username)
            messages.success(request,username+ "is successfully registered")
            return redirect('userLogin')  
    else:       
        form=userForm()
    context={'form':form}
    return render(request,'hustlerApp/signUp.html',context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('userLogin'+'?message='+'User already activated')

            if user.is_active:
                return redirect('userLogin')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('userLogin')

        except Exception as ex:
            pass

        return redirect('userLogin')
        
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
    





