from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    # path("contact/", views.contact, name="contact"),
    # path("contact/", views.ContactView.as_view(), name="contact"),
    path("<str:room>/", views.room, name="room"),

]
