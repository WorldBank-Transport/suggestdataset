from django.apps import apps
from django import forms
from django_comments.forms import CommentForm as BaseCommentForm

Comment = apps.get_registered_model('xcomments', 'XComment')

class CommentForm(BaseCommentForm):

    def get_comment_create_data(self):
        data = super(CommentForm, self).get_comment_create_data()
        data['is_public'] = False
        return data
