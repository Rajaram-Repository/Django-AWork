from django.db import models
from django.conf import settings 

class Post(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    json_data = models.JSONField()
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)

class Like(models.Model):
    Like = 'Like'
    Dislike = 'Dislike'

    INTERACTION_CHOICES = [
        (Like, 'Like'),
        (Dislike, 'Dislike'),
    ]
    DEFAULT_TYPE=Like
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=10, choices=INTERACTION_CHOICES, default=DEFAULT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        if self.type == Like.Like:
            self.post.like_count += 1
        elif self.type == Like.Dislike:
            self.post.dislike_count += 1
        self.post.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


