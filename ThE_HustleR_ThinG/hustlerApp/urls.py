from django.urls import path
from . import views
from .views import VerificationView

urlpatterns=[
    path('',views.home,name="home"),
    path('signUp/',views.userSignUp,name='signUp'),
    path('userLogin/',views.userLogin,name="userLogin"),
    path('logoutPage/',views.logoutPage,name="logoutPage"),
    path('news/',views.news,name="news"),
    path('readmore/<str:news_id>/',views.readmore,name="readmore"),
    path('likeNews/<str:news_id>/',views.likeNews,name="likeNews"),
    path('disLikeNews/<str:news_id>/',views.disLikeNews,name="disLikeNews"),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
]