from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from user.form import LoginForm
from user.models import Users, Privileges


def open_login_page(request):
    return render(request, "login.html")


def login(request):
    request.encoding = "utf-8"
    login_info = request.POST
    f = LoginForm(login_info)
    if f.is_valid():
        name = f.cleaned_data["username"]
        pwd = f.cleaned_data["userpass"]
        user = Users.objects.filter(name=name)[0]
        if not user:
            if user.password == pwd:
                return
    return False
