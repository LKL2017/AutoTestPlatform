from django.urls import path

from script import views

urlpatterns = [
    path('upload/', views.init_upload_page, name="upload"),
]
