from django.db import models
from django.contrib.auth.models import User


class userProfile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50,null=True,blank=True)
    Age=models.IntegerField(blank=True,null=True)
    PurposeOfLife=models.CharField(max_length=100,blank=True,null=True)
    Hobbies=models.CharField(max_length=50,blank=True,null=True)


class volunteerProfile(models.Model):
    volunteer=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50,blank=True,null=True)
    Image=models.ImageField(default='volunteer.png',upload_to='volunteer_pics')
    Date_created=models.DateField(auto_now_add=True)
    Introduction=models.CharField(max_length=200,blank=True,null=True)
    Profession=models.CharField(max_length=50,blank=True,null=True)
    Experience=models.CharField(max_length=30,blank=True,null=True)
    PurposeOfLife=models.CharField(max_length=100,blank=True,null=True)
    Hobbies=models.CharField(max_length=50,blank=True,null=True)
    Phone:models.CharField(max_length=15)
    HideContactDetail=models.BooleanField(default=True)


class newsReport(models.Model):
    tag_choice=(
        ('academics','academics'),
        ('sports','sports'),
        ('entertainment','entertainment'),
        ('carrier','carrier'),
        ('business','business'),
        ('other','other'),
    )
    Title=models.CharField(verbose_name='title here',max_length=200)
    Image=models.ImageField(default='good-news.jpg',upload_to='news_pics')
    Date_created=models.DateField(auto_now_add=True)
    Description=models.TextField(max_length=1000)
    Place=models.CharField(max_length=100)
    Tag=models.CharField(max_length=50,choices=tag_choice)
    Status=models.BooleanField(default=False)
    Views=models.IntegerField(default=0)

class newsLikes(models.Model):
    news=models.ForeignKey(newsReport,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE)

class newsViews(models.Model):
    news=models.ForeignKey(newsReport,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE)

class newsDisLikes(models.Model):
    news=models.ForeignKey(newsReport,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE)





