from django.shortcuts import render


# Create your views here.

def init_product_info(request):
    if request.method == "GET":
        return render(request, "pages/tables.html")
    if request.method == "POST":
        return render(request, "pages/tables.html")
