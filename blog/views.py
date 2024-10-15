# blog/views.py
# views to show the blog application
from typing import Any
from django.shortcuts import render

from . models import * 
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

import random


# class-based view
class ShowAllView(ListView):
    '''A view to show all Articles.'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class RandomArticleView(DetailView):
    '''show one article selected at random'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        '''return a random instance of the article to show'''

        #get all articles
        all_articles = Article.objects.all()#select all 
        #pick one at random
        return random.choice(all_articles)

class ArticleView(DetailView):
    '''show one article selected at random'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class CreateCommentView(CreateView):
    '''a view to show the create comment form
        GET: sends back the form
        POST: reads the form data, create an instance of COmment; save to db??
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # what to do after form submission?
    def get_success_url(self) -> str:
        '''return url to redirect to after success'''
        # return "/blog/show_all"
        return reverse("article", kwargs=self.kwargs)
    
    def form_valid(self, form):
        '''executes after form submission'''
        print(f'CreateCommentView.form_valid(): form={form}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with th eok from the url
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attatch article to the new comment
        form.instance.article = article
        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build the dict of key-values parts that become
        context variables within the template'''

        # grab existing context variables
        context = super().get_context_data(**kwargs)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # add the article to the context data
        context['article'] = article

        return 