from django.apps import apps
from django import forms
from django_comments.forms import CommentForm as BaseCommentForm
from captcha.fields import CaptchaField

Comment = apps.get_registered_model('xcomments', 'XComment')

class CommentForm(BaseCommentForm):
    captcha = CaptchaField()

    def get_comment_create_data(self):
        data = super(CommentForm, self).get_comment_create_data()
        data['is_public'] = False
        return data
