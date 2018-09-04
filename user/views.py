from django.shortcuts import render

# Create your views here.


from django.shortcuts import render


def open_login_page(request):
    return render(request, "login.html")
