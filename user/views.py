# Create your views here.


from django.shortcuts import redirect
from django.shortcuts import render

from user.form import LoginForm
from user.models import User


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        request.encoding = "utf-8"
        login_info = request.POST
        f = LoginForm(login_info)
        if f.is_valid():
            name = f.cleaned_data["username"]
            pwd = f.cleaned_data["userpass"]
            stay_login = f.cleaned_data["stay_login"]
            res_set = User.objects.filter(name=name)
            if len(res_set) == 0:
                return render(request, "login.html", {"error_msg", "无此用户,请重新输入！"})
            user = res_set[0]
            if str(user.password) == pwd:

                return redirect("/home")
        return render(request, "login.html", {"obj": f.errors})


def init_home(request):
    """初始化home页面"""
    return render(request, "home.html")
