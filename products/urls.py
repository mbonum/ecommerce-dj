from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    path("<slug:slug>/", views.ProductDetailSlugView.as_view(), name="detail"),
    path("<slug:slug>/<int:pk>/", views.ProductDownloadView.as_view(), name="download"),
    # url('^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView
    # path('<int:pk>/', ProductDetailView.as_view())
]
