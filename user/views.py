# Create your views here.


from django.shortcuts import redirect
from django.shortcuts import render

from user.form import LoginForm
from user.models import User
import utils.decorators as dec


def login(request):
    print(request.method)
    if request.method == "GET":
        try:
            user = request.session.get("user", None)
            print(user)
        except AttributeError:
            return render(request, "login.html")
        else:
            if user:
                return render(request, "home.html")
        return render(request, "login.html")

    if request.method == "POST":
        request.encoding = "utf-8"
        login_info = request.POST
        f = LoginForm(login_info)
        if f.is_valid():
            name = f.cleaned_data["username"]
            pwd = f.cleaned_data["userpass"]
            remember = f.cleaned_data["remember"]
            res_set = User.objects.filter(name=name)
            if len(res_set) == 0:
                return render(request, "login.html", {"error_msg": "用户名或者密码错误，请重新输入！"})
            user = res_set[0]
            if str(user.password) == pwd:
                request.session["user"] = user.name
                if remember:
                    pass
                # TODO 需要添加记住我功能
                return redirect(init_home)
            elif str(user.password) != pwd:
                return render(request, "login.html", {"error_msg": "用户名或者密码错误，请重新输入！"})
        return render(request, "login.html", {"obj": f.errors})


@dec.dec_is_login
def logout(request):
    del request.session["user"]
    return redirect(login)



def init_home(request):
    """初始化home页面"""
    return render(request, "home.html")
