from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    pet_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='profile_pics/', max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=280, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to='category_pics/', max_length=200, blank=True, null=True)
    category_description = models.CharField(max_length=300)
    
    def __str__(self):
        return self.category_name

class Post(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    image = models.ImageField(upload_to='post_images/', max_length=200)
    caption = models.CharField(max_length=300, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return f"Post by {self.user.username} on {self.date_created}"

class Comment(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} commented: {self.comment_text[:30]}..."

class Like(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} liked {self.post}"

class Follow(models.Model):
    follower = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('follower', 'followed')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Help(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='help_questions')
    date_created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=500)
    answer = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='help_images/', max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Help by {self.user.username}: {self.question[:50]}..."

class FavoriteCategory(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='favorite_categories')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='favorited_by')
    
    class Meta:
        unique_together = ('user', 'category')
    
    def __str__(self):
        return f"{self.user.username} favorited {self.category.category_name}"

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    likes = models.ManyToManyField('auth.User', related_name='liked_pets', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name