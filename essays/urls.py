from django.urls import path
from . import views  # CommentView author_view GenerateEssayPDF


app_name = "essays"


urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.details, name="detail"),
    path("<slug:slug>/<int:pk>/like/", views.like_view, name="like"),
    # path('<slug:slug>/post/', CommentView.as_view(), name='post')
    # path('author/<slug:slug>/', author_view, name='bio')
    # path('essay-pdf/<slug:slug>/', GenerateEssayPDF.as_view(), name='pdf'),
]
