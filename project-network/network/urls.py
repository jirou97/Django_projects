
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("post",views.compose_post, name="post"),
    path("posts/<int:post_id>", views.put_somestuff, name="put_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("del_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("del_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("user/<int:user_id>", views.user, name="user_view"),
    path("follow", views.follow, name="follow_view"),
    path("unfollow", views.unfollow, name="unfollow_view"),
]
