## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"), 
    path(r'', views.RandomArticleView.as_view(), name="random"), 
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), 
    # path(r'create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment')
   
]

 