from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.DatasetSuggestions.as_view(), name='dataset-suggestions'),
    url(r'^ratings/$', views.DatasetList.as_view(), name='dataset-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view(), name='dataset-detail'),
    url(r'^like/(?P<pk>[0-9]+)/$', views.DatasetLikeCreate.as_view(), name='datasetlike-create'),
    url(r'suggestions/add/$', views.DatasetSuggest.as_view(), name='dataset-suggest'),
]
