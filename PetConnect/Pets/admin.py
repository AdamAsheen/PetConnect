from django.contrib import admin
from pets.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('date_joined',)

    fieldsets = (
        ("Basic Info", {
            "fields": ("username", "email", "password")
        }),
        ("Profile Info", {
            "fields": ("profile_pic",),
            "classes": ("collapse",)
        }),
    )

# Allows editing of comments and likes inside the post page
class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'caption', 'date_created')
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

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = 'Likes'

    list_display = ('user', 'category', 'caption', 'date_created', 'like_count')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_text', 'date_created')
    search_fields = ('user__username', 'post__caption')
    list_filter = ('date_created',)
    readonly_fields = ('date_created',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')
    search_fields = ('follower__username', 'followed__username')

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner')
    search_fields = ('name', 'breed', 'owner__username')
    list_filter = ('breed',)

# Register your models here.

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Forum)
admin.site.register(Pet, PetAdmin)

admin.site.site_header = "PetConnect Admin"
admin.site.site_title = "PetConnect Admin Portal"
admin.site.index_title = "Welcome to PetConnect Management"