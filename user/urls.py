from django.urls import path

from user import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'^$', views.login, name="login"),
    path(r"^login/$", views.login, name="login"),
    path(r'^logout$', views.logout, name="logout")
]
