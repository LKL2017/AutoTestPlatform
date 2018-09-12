from django.urls import path

from product import views

urlpatterns = [
    path(r'info/', views.init_product_info, name="info"),
    path(r'^detail/<str:name>$', views.product_detail, name="detail")
]
