from django.urls import path

from testcase import views

urlpatterns = [
    path(r'^upload/$', views.init_upload_page, name="upload")

]
