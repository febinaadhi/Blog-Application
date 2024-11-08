from django.contrib import admin
from .models import CustomUser, Post

# Custom admin for CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'is_staff', 'is_active')
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'email', 'mobile', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    search_fields = ('username', 'email', 'mobile')
    ordering = ('username',)

# Custom admin for Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'likes_count', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'author')
    fieldsets = (
        ('Content Information', {
            'fields': ('title', 'description', 'tags')
        }),
        ('Publication Details', {
            'fields': ('is_published', 'author', 'created_at')  # Excluding 'updated_at' field
        }),
    )
    search_fields = ('title', 'tags', 'author__username')
    ordering = ('-created_at',)
    exclude = ('updated_at',)  # Exclude updated_at as it's auto-updated by Django

    # Adding a custom method to show the number of likes
    def likes_count(self, obj):
        return obj.likes.count()  # Displays the count of likes on the post
    likes_count.short_description = 'Likes'  # Label in the admin panel

# Registering models with custom admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
