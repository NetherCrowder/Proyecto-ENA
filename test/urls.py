from django.urls import path
from . import views

app_name = 'test'

urlpatterns = [
    path("1/", views.index1, name="index1"),
    path("2/", views.index2, name="index2"),
    path("3/", views.index3, name="index3"),
    path("test/<int:id>/", views.index_detail, name="index_details"),
    path("<int:id>/test/", views.index_detail2, name="index_detail2"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    #path("<int:question_id>/vote/", views.vote, name="vote"),
]