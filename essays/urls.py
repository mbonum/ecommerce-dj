from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = "essays"

urlpatterns = [
    path("", views.essays, name="list"),
    path("<slug:slug>/", views.detail, name="detail"),
    path("<slug:slug>/<int:pk>/like/", views.like_view, name="like"),
    path("pdf/<slug:slug>/", views.GenerateEssayPDF.as_view(), name="pdf"),
    path(_("author/<slug:slug>/"), views.author_view, name="author"),
]
