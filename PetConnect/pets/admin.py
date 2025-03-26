from django.contrib import admin

from django.contrib import admin
from pets.models import *

# Allows editing of comments and likes inside the post page
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'category', 'caption', 'date_created')
    list_display_links = ('user', 'caption')
    search_fields = ('user__username', 'caption')
    list_filter = ('category', 'date_created')
    inlines = [CommentInline, LikeInline]
    ordering = ('-date_created',)
    list_per_page = 20

    #Check that Post model has a status field for this to work
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected posts have been approved.")

    approve_posts.short_description = "Approve selected posts"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_text', 'date_created')
    search_fields = ('user__username', 'post__caption')
    list_filter = ('date_created',)
    readonly_fields = ('date_created',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')
    search_fields = ('follower__username', 'followed__username')

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Follow)

admin.site.site_header = "PetConnect Admin"
admin.site.site_title = "PetConnect Admin Portal"
admin.site.index_title = "Welcome to PetConnect Management"