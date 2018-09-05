from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from user.form import LoginForm
from user.models import User, Privilege
from django.shortcuts import redirect


def open_login_page(request):
    return render(request, "login.html")


def login(request):
    request.encoding = "utf-8"
    login_info = request.POST
    f = LoginForm(login_info)
    if f.is_valid():
        name = f.cleaned_data["username"]
        pwd = f.cleaned_data["userpass"]
        stay_login = f.cleaned_data["stay_login"]
        res_set = User.objects.filter(name=name)
        if len(res_set) == 0:
            return redirect(open_login_page)
        user = res_set[0]
        if str(user.password) == pwd:
            return redirect("/home")
    print(f.errors())
    return redirect(open_login_page, {"obj": f.errors()})


def init_home(request):
    """初始化home页面"""
    return render(request, "home.html")
