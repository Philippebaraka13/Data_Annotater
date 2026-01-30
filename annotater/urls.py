from django.urls import path
from . import views

app_name = "annotater"

urlpatterns = [
    path("", views.pending_list, name="pending_list"),
    path("upload/", views.upload_csv, name="upload_csv"),
    path("row/<int:pk>/edit/", views.edit_row, name="edit_row"),
]
