from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^go/(?P<pk>[\w\d-]+)/$', views.RedirectView.as_view(), name="redirect"),
]
