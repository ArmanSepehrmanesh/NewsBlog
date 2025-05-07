from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


class Post(models.Model):

    status_choice = [
        ('DF','Draft'),
        ('PB', 'Published'),
        ('RJ', 'Rejected'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts') 
    #data fields
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    #date field
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #choice
    status = models.CharField(max_length=250, choices = status_choice, default= 'DF' )
    #add custome manager object
    objects = models.Manager()  
    published = PublishedManager() 

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name='پست'
        verbose_name_plural = 'پست ها'
        
    def __str__(self):
            return self.title
    
    def get_absolute_url(self): 
         return reverse('blog:post_detail', args=[self.id])
    

#form ticket

class Ticket(models.Model):
     
     message = models.TextField(max_length=250,verbose_name='پیام')
     name = models.CharField(max_length=200, verbose_name='نام')
     email = models.EmailField(verbose_name='ایمیل')
     phone = models.CharField(max_length=11,verbose_name='شماره تماس')
     subject = models.CharField(verbose_name='موضوع', max_length=100)

     class Meta:
          verbose_name='تیکت'
          verbose_name_plural = 'تیکت ها'

     def __str__(self):
            return self.name
     
#comment form

class Comment(models.Model):
     post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comment', verbose_name='پست')
     name = models.CharField(max_length=200, verbose_name='نام')
     body = models.TextField(max_length=250,verbose_name='متن کامنت')
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     active = models.BooleanField(default=False)

     class Meta:
          ordering = ['created']
          indexes = [
            models.Index(fields=['created'])
        ]
          verbose_name='کامنت'
          verbose_name_plural = 'کامنت ها'

     def __str__(self):
            return f"{self.name}: {self.post}"