from django.urls import path

from user import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('.', views.login, name="login"),
    path("home/", views.init_home, name="home")
]
