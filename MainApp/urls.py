from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('', views.indexPageView, name="index"),
  path('test-page', views.testPageView, name="test"),
]