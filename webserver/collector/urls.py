from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.accounts, name="accounts"),
    path("consumers/", views.consumers, name="consumers"),
    path("upload", views.upload, name="upload"),
]
