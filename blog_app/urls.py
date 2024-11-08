from django.urls import path
from .views import UserSignupView, LoginView, PostCreateView, PostListView, PostPublishView, LikePostView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('posts/list/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<uuid:pk>/publish/', PostPublishView.as_view(), name='post-publish'),
    path('posts/<uuid:pk>/like/', LikePostView.as_view(), name='post-like'),
]
