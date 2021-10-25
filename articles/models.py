from typing import Match
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from ckeditor.fields import RichTextField


# category modal
class Category(models.Model):
    name = models.CharField(max_length=100, default='Uncategorized')

    def __str__(self):
        return self.name


# Article post modal
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    content = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    poster = models.ImageField(default='post.png', upload_to='PostThumbnails')
    pub_date = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        img = Image.open(self.poster.path)
        if img.height > 710 or img.width > 350:
            output_size = (710, 350)
            img.thumbnail(output_size)
            img.save(self.poster.path)

    def __str__(self):
        return self.title[:40] + '...' + ' by- ' + self.author.username




# Comments model
class postComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:12] + "...." + "by: " + self.user.username
    
