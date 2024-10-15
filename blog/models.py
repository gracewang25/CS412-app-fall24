# blog/models.py
# Define data models (objects) for use in the blog application
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data for a blog Article by some author.'''

    # data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) ## new field

    def __str__(self):
        '''Return a string representation of this Article.'''
        return f"{self.title} by {self.author}"
    
    def get_comments(self):
        '''Retreive all comments for this article'''

        # use ORM to filter comments where this object is the foreign key
        # instance of Article is the FK
        comments = Comment.objects.filter(article=self)
        return comments

class Comment(models.Model):
    '''encapsulate a comment on a model'''

    # one to many between articles and comments
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' string presentation of this object'''
        return f"{self.text}"
