from django.urls import path

from testcase import views

urlpatterns = [
    path(r'^upload/$', views.init_upload_page, name="upload"),
    path(r'^list/$', views.init_case_list, name="list"),
    path(r'^detail/$', views.case_data, name="detail"),
    path(r'^caseDetail/$', views.init_case_detail, name="caseDetail"),
]
