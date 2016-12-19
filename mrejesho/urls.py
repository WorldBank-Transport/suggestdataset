from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.FeedbackCreate.as_view(), name='feedback-create'),
    url(r'^thanks/$', views.FeedbackThanks.as_view(), name='feedback-thanks'),
]
