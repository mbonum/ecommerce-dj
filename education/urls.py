from django.urls import path

from . import views  # ReadDetailSlugView,

app_name = "education"

urlpatterns = [
    path("", views.ReadListView.as_view(), name="booklist"),
    # path('', index, name='booklist'),ReadDetailSlugView.as_view()
    path("<slug:slug>/", views.details, name="booknotes"),
]
