from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    # Specify related_name for 'groups' and 'user_permissions' to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Set unique related_name here
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Set unique related_name here
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    class Meta:
        db_table = 'models_customuser'
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')
        ordering = ('username',)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255)  # Optionally change to ManyToMany if needed
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    class Meta:
        db_table = 'models_post'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
