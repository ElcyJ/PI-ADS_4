from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Adress(models.Model):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profiles_user',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    adress = models.ForeignKey(Adress, related_name='profile',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    userId = models.ForeignKey(Profile, related_name='posts',
                               on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='posts_owner',
                              on_delete=models.CASCADE)


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    postId = models.ForeignKey(Post, related_name='comments',
                               on_delete=models.CASCADE)