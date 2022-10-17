from django.urls import path

from . import views 

app_name = "education"

urlpatterns = [
    path("", views.ReadListView.as_view(), name="list"),
    # ReadDetailSlugView.as_view()
    path("<slug:slug>/", views.detail, name="booknotes"),
]
