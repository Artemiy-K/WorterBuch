from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('start_test', views.start_test, name="start_test"),
    path('get_answer', views.get_answer, name="get_answer"),
    path('wort_in_words', views.wort_in_words, name="wort_in_words"),
    path('verification', views.verification, name="verification")

]