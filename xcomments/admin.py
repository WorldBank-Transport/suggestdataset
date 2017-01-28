from django.contrib import admin
from django_comments.admin import CommentsAdmin
from .models import XComment


admin.site.register(XComment, CommentsAdmin)
